from collections.abc import Sequence
from typing import TypedDict, Callable
import sys
import asyncio
import csv
from io import StringIO
import decimal
from enum import Enum
from datetime import date, datetime
from urllib.request import urlopen

from ariadne import SubscriptionType
from graphql import GraphQLError, GraphQLResolveInfo, GraphQLObjectType, GraphQLEnumType,\
    get_named_type, is_scalar_type, is_wrapping_type
from pyparsing import ParseException

from .database import DBInterface
from .filter_parser import number_filter_parser, date_filter_parser, datetime_filter_parser, boolean_filter_parser
from .graphql_app import check_permission, HideResult
from . import models_functions as f
from .models_utils import BaseModel, ValueEnum
from .querybuilder import Select, Column, Function, Cast, Exists, Unnest, Like, PositionalParameter, Term, Descending
from .request_utils import get_db


class FieldFilter(TypedDict):
    field_name: str
    value: str


class FileUpload(TypedDict):
    data_url: str | None
    filename: str


class ColumnOrder(TypedDict):
    name: str
    descending: bool

class TableControls(TypedDict):
    filters: list[FieldFilter]
    limit: int | None
    offset: int | None
    descending: bool
    order_by: list[Column | Descending] | None


def process_controls(model: type[BaseModel], controls: dict) -> TableControls:
    res: TableControls = {
        'filters': controls.get('filters', []),
        'limit': controls.get('limit'),
        'offset': controls.get('offset'),
        'descending': controls.get('descending', False),
        'order_by': None
    }
    order_by_raw: list[ColumnOrder] | None = controls.get('order_by')
    if order_by_raw is not None:
        new_order_by = []
        for col_order in order_by_raw:
            try:
                new_col = getattr(model, col_order['name'])
                if not isinstance(new_col, Column):
                    raise AttributeError
            except AttributeError:
                raise GraphQLError(f"Model {model.__name__} does not have column {col_order['name']}")
            new_order_by.append(Descending(new_col) if col_order['descending'] else new_col)
        res['order_by'] = new_order_by
    return res


def data_url_to_bytes(file: FileUpload) -> bytes:
    with urlopen(file['data_url']) as response:
        return response.read()


def get_csv_line_reader(file_upload: FileUpload):
    file = StringIO(data_url_to_bytes(file_upload).decode('utf-8'))
    return csv.reader(file)


def get_csv_dict_reader(file_upload: FileUpload) -> csv.DictReader:
    file = StringIO(data_url_to_bytes(file_upload).decode('utf-8'))
    return csv.DictReader(file)


# Resolver Tools

async def get_or_gql_error[T: BaseModel](db: DBInterface, model: type[T], **primary_keys) -> T:
    """ Primary keys need to be real values """
    row = await f.get(db, model, **primary_keys)
    if row is None:
        raise GraphQLError(f"Could not get {model.__name__} with keys {', '.join(f'{pk[0]}={pk[1]}' for pk in primary_keys.items())}")
    return row


def separate_filters(filters: list[FieldFilter], field_names_to_separate: list[str]):
    """ When some filters are automatically handled, and others you need to write custom SQLAlchemy queries """
    newfilters = []
    separated = []
    for filt in filters:
        if filt['field_name'] in field_names_to_separate:
            separated.append(filt)
        else:
            newfilters.append(filt)
    return newfilters, separated


def _unwrap_gql_type(type_):
    temp_type = type_
    while is_wrapping_type(temp_type):
        temp_type = temp_type.of_type
    return temp_type


# Complete Resolvers

def resolve_type_inspector_factory(model_list: list[BaseModel]):
    models_dict = {model.__name__: model for model in model_list}

    def resolve_type_inspector(_, info: GraphQLResolveInfo, type_name: str):
        gqltype = info.schema.get_type(type_name)
        if gqltype is None or not isinstance(gqltype, GraphQLObjectType):
            return None

        # Primary Keys. Raise error when using directive and model not found, else ignore
        model_name = getattr(gqltype, '__modelname__', type_name)
        model: type[BaseModel] | None = models_dict.get(model_name)
        if model is not None:
            primary_keys = model.__metadata__.primary_keys
        elif hasattr(gqltype, '__modelname__'):
            raise GraphQLError(f"Could not find model with name {model_name}")
        else:
            primary_keys = None

        all_filter = hasattr(gqltype, '__all_filter__')
        field_details = []
        for field_name, field in gqltype.fields.items():
            caption = getattr(field, '__caption__', field_name.title().replace('_', ' '))
            dataclass_field = model.__metadata__.dataclass_fields.get(field_name) if model is not None else None
            is_database = dataclass_field is not None
            is_scalar = is_scalar_type(_unwrap_gql_type(field.type))

            # Handle filter type
            field_filter_type = None
            if getattr(field, '__filter__', is_database or all_filter):  # If has filter
                if is_database:
                    field_type = f.extract_main_type(dataclass_field.type)
                    if field_type is str or issubclass(field_type, ValueEnum) or issubclass(field_type, Enum):
                        field_filter_type = 'STRING'
                    elif field_type in [int, float, decimal.Decimal]:
                        field_filter_type = 'NUMBER'
                    elif field_type is date:
                        field_filter_type = 'DATE'
                    elif field_type is datetime:
                        field_filter_type = 'DATE'
                    elif field_type is bool:
                        field_filter_type = 'BOOLEAN'
                    else:
                        raise GraphQLError(f"Cannot filter on column type {field_type}")
                else:  # Deducing filter type from GraphQL type
                    field_type = get_named_type(field.type)
                    if field_type is None:
                        raise Exception('Can only filter on Named Types')

                    if field_type.name == 'String':
                        field_filter_type = 'STRING'
                    elif field_type.name in ['Int', 'Float']:
                        field_filter_type = 'NUMBER'
                    elif field_type.name in ['Date', 'DateTime']:
                        field_filter_type = 'DATE'
                    elif field_type.name == 'Boolean':
                        field_filter_type = 'BOOLEAN'
                    elif isinstance(field_type, GraphQLEnumType):
                        field_filter_type = 'STRING'  # Consider Enum as strings
                    else:
                        raise GraphQLError(f'Type {field_type.name} cannot support filtering on field {field_name}')

            field_details.append({
                'field_name': field_name,
                'caption': caption,
                'is_database': is_database,
                'is_scalar': is_scalar,
                'filter_type': field_filter_type,
                'editable': False  # Todo: implement
            })

        return {'field_details': field_details, 'primary_keys': primary_keys}
    return resolve_type_inspector


def apply_filter_to_query(q: Select, column: Column, field_type, value) -> Select:
    try:
        if field_type is str or issubclass(field_type, ValueEnum) or issubclass(field_type, Enum):
            # cast used to make Enum behave like strings.
            return q.where(Like(
                Function('LOWER', Cast(column, 'varchar')),
                PositionalParameter(value.lower()) if q.use_parameters else value.lower()
            ))
        elif field_type in [int, float, decimal.Decimal]:
            return number_filter_parser(q, column, value)
        elif field_type is date:
            return date_filter_parser(q, column, value)
        elif field_type is datetime:
            return datetime_filter_parser(q, column, value)
        elif field_type is bool:
            return boolean_filter_parser(q, column, value)
        raise GraphQLError(f"Cannot filter on column type {field_type}")
    except ParseException as e:
        raise GraphQLError(f"Cannot parse value: {value} for field {column} of type {field_type} [{e}]")


def load_from_model_query(
        model: type[BaseModel], *,
        filters: Sequence[FieldFilter] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        descending: bool | None = None,
        order_by: Sequence[Term] | None = None,  # None for primary key ordering, [] for no ordering
        init_query: Select | None = None,
        query_modifier: Callable[[Select], Select] | None = None,
) -> Select:
    # Init query
    q = Select(model).select_main_columns() if init_query is None else init_query
    # Apply filter
    filters = [] if filters is None else filters
    for filt in filters:
        full_name = filt['field_name']
        value = filt['value']

        *relation_names, col_name = full_name.split('.')
        current_model = model
        for relation_name in relation_names:
            # Join relationship, then get relation model
            q.join_relation(current_model, relation_name)
            current_model = f.get_relation_model(current_model, relation_name)

        # Deducing filter type by model column type. Contrary to resolve_type_inspector.
        column: Column = getattr(current_model, col_name)
        field_type = f.get_field_main_type(current_model, col_name)

        if f.is_field_list_type(current_model, col_name):  # Handle lists
            unnested_table = Unnest(column, alias=col_name+'_unnested', column_names=['col1'])
            q.where(Exists(apply_filter_to_query(
                    Select(unnested_table, q.db_type).select_all(),
                    unnested_table.columns[0],
                    field_type,
                    value
            )))
        else:
            apply_filter_to_query(q, column, field_type, value)

    # Apply query modifiers
    if query_modifier is not None:
        query_modifier(q)

    # Apply order by
    if order_by:
        q.order_by(*order_by)
    elif order_by is None and not q.is_ordered:
        q.order_by(*(f.table(model).columns_map[pkname] for pkname in model.__metadata__.primary_keys))

    if descending:
        q.invert_order_by()

    # Apply limit and offsets
    if limit is not None:
        q.limit(limit)
    if offset is not None:
        q.offset(offset)
    return q


def resolve_type_loader_factory(model_list: list[type[BaseModel]]):
    models_dict = {model.__name__: model for model in model_list}

    async def resolve_type_loader(_, info, type_name: str, controls: dict):
        gqltype = info.schema.get_type(type_name)
        if gqltype is None:  # Check if Type exists in GQL
            raise GraphQLError(f'Type {type_name} does not exist')
        model_name = getattr(gqltype, '__modelname__', type_name)

        try:
            model = models_dict[model_name]
        except KeyError:
            raise GraphQLError(f"Could not find {model_name} in Models")

        q = load_from_model_query(model, **process_controls(model, controls))

        recs = await (model.__metadata__.registry.db_connection_factory or get_db)(info).fetch(*q.to_sql())

        objs = f.build_all(model, recs)
        for obj in objs:
            obj.__typename = type_name
        return objs

    return resolve_type_loader


def simple_table_resolver_factory[T: BaseModel](model: type[T], query_modifier: Callable[[Select], Select] | None = None):
    async def simple_table_resolver(_, info, controls: dict) -> list[T]:
        q = load_from_model_query(model, **process_controls(model, process_controls(model, controls)), query_modifier=query_modifier)
        db = (model.__metadata__.registry.db_connection_factory or get_db)(info)
        return f.build_all(model, await db.fetch(*q.to_sql()))
    return simple_table_resolver


# Subscription tools

def subscription_permission_check(generator):
    async def new_generator(obj, info, *args, **kwargs):
        try:
            check_permission(info)
        except HideResult:
            yield None
            return

        async for res in generator(obj, info, *args, **kwargs):
            yield res

    return new_generator


# noinspection PyProtectedMember
def assign_simple_resolver(sub_object: SubscriptionType):
    def simple_resolver(val, *_, **__):
        return val

    for sub_field_name in sub_object._subscribers:
        if sub_field_name not in sub_object._resolvers:
            sub_object.set_field(sub_field_name, simple_resolver)


# External executors

async def external_module_executor(module_name, *args: str):
    proc = await asyncio.create_subprocess_exec(sys.executable, '-u', '-m', f'scripts.{module_name}', *args,
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        data = await proc.stdout.readline()
        yield data.decode().rstrip()

    error = await proc.stderr.read()
    if error:
        raise GraphQLError(error.decode().rstrip())


async def external_script_executor(script_name, *args: str):
    proc = await asyncio.create_subprocess_exec(script_name, *args,
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while not proc.stdout.at_eof():
        data = await proc.stdout.readline()
        yield data.decode().rstrip()

    error = await proc.stderr.read()
    if error:
        raise GraphQLError(error.decode().rstrip())
