from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GREETER_UNSPECIFIED: _ClassVar[ErrorReason]
    USER_NOT_FOUND: _ClassVar[ErrorReason]

class ListViewLayout(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    card: _ClassVar[ListViewLayout]
    grid: _ClassVar[ListViewLayout]
    simple: _ClassVar[ListViewLayout]
    post_card: _ClassVar[ListViewLayout]

class ListViewActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    list_item_new: _ClassVar[ListViewActionType]

class PaginateType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INFINITE: _ClassVar[PaginateType]
    PAGINATE: _ClassVar[PaginateType]
GREETER_UNSPECIFIED: ErrorReason
USER_NOT_FOUND: ErrorReason
card: ListViewLayout
grid: ListViewLayout
simple: ListViewLayout
post_card: ListViewLayout
list_item_new: ListViewActionType
INFINITE: PaginateType
PAGINATE: PaginateType
SLUGS_FIELD_NUMBER: _ClassVar[int]
slugs: _descriptor.FieldDescriptor
IS_TITLE_FIELD_NUMBER: _ClassVar[int]
is_title: _descriptor.FieldDescriptor
IS_SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
is_sub_title: _descriptor.FieldDescriptor
EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
event_name: _descriptor.FieldDescriptor
SVC_LIST_FIELD_NUMBER: _ClassVar[int]
svc_list: _descriptor.FieldDescriptor

class Oauth2LoginHookRequest(_message.Message):
    __slots__ = ("type", "provider", "providerAccountId", "refresh_token", "refresh_token_expires_in", "access_token", "expires_at", "token_type", "scope", "id_token", "session_state")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PROVIDERACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SESSION_STATE_FIELD_NUMBER: _ClassVar[int]
    type: str
    provider: str
    providerAccountId: str
    refresh_token: str
    refresh_token_expires_in: int
    access_token: str
    expires_at: int
    token_type: str
    scope: str
    id_token: str
    session_state: str
    def __init__(self, type: _Optional[str] = ..., provider: _Optional[str] = ..., providerAccountId: _Optional[str] = ..., refresh_token: _Optional[str] = ..., refresh_token_expires_in: _Optional[int] = ..., access_token: _Optional[str] = ..., expires_at: _Optional[int] = ..., token_type: _Optional[str] = ..., scope: _Optional[str] = ..., id_token: _Optional[str] = ..., session_state: _Optional[str] = ...) -> None: ...

class AuthToken(_message.Message):
    __slots__ = ("id", "access_token")
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    access_token: str
    def __init__(self, id: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class UserInfo(_message.Message):
    __slots__ = ("ID", "name", "username", "image", "email", "roles")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    ID: str
    name: str
    username: str
    image: str
    email: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ID: _Optional[str] = ..., name: _Optional[str] = ..., username: _Optional[str] = ..., image: _Optional[str] = ..., email: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...

class RegisterReq(_message.Message):
    __slots__ = ("username", "email", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    email: str
    password: str
    def __init__(self, username: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegisterReply(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class LoginReq(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class MtmError(_message.Message):
    __slots__ = ("err_code", "err_message")
    ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    err_code: str
    err_message: str
    def __init__(self, err_code: _Optional[str] = ..., err_message: _Optional[str] = ...) -> None: ...

class LoginReply(_message.Message):
    __slots__ = ("access_token",)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "email", "username")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    email: str
    username: str
    def __init__(self, id: _Optional[int] = ..., email: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class UserListReq(_message.Message):
    __slots__ = ("Pagination", "q", "usename", "email")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    USENAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    q: str
    usename: str
    email: str
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., q: _Optional[str] = ..., usename: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class UserListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    items: _containers.RepeatedCompositeFieldContainer[User]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class UserGetReq(_message.Message):
    __slots__ = ("id", "host_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    host_name: str
    def __init__(self, id: _Optional[int] = ..., host_name: _Optional[str] = ...) -> None: ...

class UserCreateReq(_message.Message):
    __slots__ = ("email", "username", "password", "roles")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    email: str
    username: str
    password: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, email: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...

class UserCreateReply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UserUpdateReq(_message.Message):
    __slots__ = ("id", "title", "sp_enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    sp_enabled: bool
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., sp_enabled: bool = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ObjIdReply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ObjId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ("ok", "error", "id", "message", "rows_affected")
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROWS_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    error: str
    id: str
    message: str
    rows_affected: int
    def __init__(self, ok: bool = ..., error: _Optional[str] = ..., id: _Optional[str] = ..., message: _Optional[str] = ..., rows_affected: _Optional[int] = ...) -> None: ...

class ErrorRes(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ResCreateReply(_message.Message):
    __slots__ = ("id", "err")
    ID_FIELD_NUMBER: _ClassVar[int]
    ERR_FIELD_NUMBER: _ClassVar[int]
    id: str
    err: str
    def __init__(self, id: _Optional[str] = ..., err: _Optional[str] = ...) -> None: ...

class ResUpdateReply(_message.Message):
    __slots__ = ("err",)
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: str
    def __init__(self, err: _Optional[str] = ...) -> None: ...

class ResDeleteReply(_message.Message):
    __slots__ = ("err",)
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: str
    def __init__(self, err: _Optional[str] = ...) -> None: ...

class ResDeleteReq(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class Paging(_message.Message):
    __slots__ = ("page", "limit", "order_by", "order", "cursor", "prev_cursor")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    PREV_CURSOR_FIELD_NUMBER: _ClassVar[int]
    page: int
    limit: int
    order_by: str
    order: str
    cursor: str
    prev_cursor: str
    def __init__(self, page: _Optional[int] = ..., limit: _Optional[int] = ..., order_by: _Optional[str] = ..., order: _Optional[str] = ..., cursor: _Optional[str] = ..., prev_cursor: _Optional[str] = ...) -> None: ...

class FieldMarks(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fields: _Optional[_Iterable[str]] = ...) -> None: ...

class ListItem(_message.Message):
    __slots__ = ("common_list_item", "card_item", "post_card")
    COMMON_LIST_ITEM_FIELD_NUMBER: _ClassVar[int]
    CARD_ITEM_FIELD_NUMBER: _ClassVar[int]
    POST_CARD_FIELD_NUMBER: _ClassVar[int]
    common_list_item: CommonListItem
    card_item: CommonCardItem
    post_card: PostCardItem
    def __init__(self, common_list_item: _Optional[_Union[CommonListItem, _Mapping]] = ..., card_item: _Optional[_Union[CommonCardItem, _Mapping]] = ..., post_card: _Optional[_Union[PostCardItem, _Mapping]] = ...) -> None: ...

class CommonListItem(_message.Message):
    __slots__ = ("id", "title", "description", "actions")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    actions: ItemAction
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., actions: _Optional[_Union[ItemAction, _Mapping]] = ...) -> None: ...

class CommonCardItem(_message.Message):
    __slots__ = ("id", "title", "sub_title", "actions", "sumary")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    SUMARY_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    sub_title: str
    actions: ItemAction
    sumary: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., sub_title: _Optional[str] = ..., actions: _Optional[_Union[ItemAction, _Mapping]] = ..., sumary: _Optional[str] = ...) -> None: ...

class PostCardItem(_message.Message):
    __slots__ = ("id", "layout_variant", "title", "sub_title", "actions", "summary", "top_image", "excerpt", "category", "author", "publish_date", "slug", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_VARIANT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TOP_IMAGE_FIELD_NUMBER: _ClassVar[int]
    EXCERPT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_DATE_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    layout_variant: str
    title: str
    sub_title: str
    actions: ItemAction
    summary: str
    top_image: str
    excerpt: str
    category: str
    author: str
    publish_date: MtDate
    slug: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., layout_variant: _Optional[str] = ..., title: _Optional[str] = ..., sub_title: _Optional[str] = ..., actions: _Optional[_Union[ItemAction, _Mapping]] = ..., summary: _Optional[str] = ..., top_image: _Optional[str] = ..., excerpt: _Optional[str] = ..., category: _Optional[str] = ..., author: _Optional[str] = ..., publish_date: _Optional[_Union[MtDate, _Mapping]] = ..., slug: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class ListItemAction(_message.Message):
    __slots__ = ("id", "label", "icon", "group", "url", "is_default", "access_key", "sort", "component", "component_props", "html")
    class ComponentPropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_PROPS_FIELD_NUMBER: _ClassVar[int]
    HTML_FIELD_NUMBER: _ClassVar[int]
    id: str
    label: str
    icon: str
    group: str
    url: str
    is_default: bool
    access_key: str
    sort: int
    component: str
    component_props: _containers.ScalarMap[str, str]
    html: str
    def __init__(self, id: _Optional[str] = ..., label: _Optional[str] = ..., icon: _Optional[str] = ..., group: _Optional[str] = ..., url: _Optional[str] = ..., is_default: bool = ..., access_key: _Optional[str] = ..., sort: _Optional[int] = ..., component: _Optional[str] = ..., component_props: _Optional[_Mapping[str, str]] = ..., html: _Optional[str] = ...) -> None: ...

class ItemAction(_message.Message):
    __slots__ = ("default_action", "item_actions")
    DEFAULT_ACTION_FIELD_NUMBER: _ClassVar[int]
    ITEM_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    default_action: ListItemAction
    item_actions: _containers.RepeatedCompositeFieldContainer[ListItemAction]
    def __init__(self, default_action: _Optional[_Union[ListItemAction, _Mapping]] = ..., item_actions: _Optional[_Iterable[_Union[ListItemAction, _Mapping]]] = ...) -> None: ...

class CommontListReq(_message.Message):
    __slots__ = ("slugs", "params", "pagination", "pre_tag_limit", "cursor", "rerefer", "site_host")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PRE_TAG_LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    REREFER_FIELD_NUMBER: _ClassVar[int]
    SITE_HOST_FIELD_NUMBER: _ClassVar[int]
    slugs: str
    params: _containers.ScalarMap[str, str]
    pagination: Paging
    pre_tag_limit: int
    cursor: str
    rerefer: str
    site_host: str
    def __init__(self, slugs: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ..., pagination: _Optional[_Union[Paging, _Mapping]] = ..., pre_tag_limit: _Optional[int] = ..., cursor: _Optional[str] = ..., rerefer: _Optional[str] = ..., site_host: _Optional[str] = ...) -> None: ...

class CurdDetailReq(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class CurdDetail(_message.Message):
    __slots__ = ("title", "form")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FORM_FIELD_NUMBER: _ClassVar[int]
    title: str
    form: FormSchema
    def __init__(self, title: _Optional[str] = ..., form: _Optional[_Union[FormSchema, _Mapping]] = ...) -> None: ...

class MtDate(_message.Message):
    __slots__ = ("year", "month", "day")
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    year: int
    month: int
    day: int
    def __init__(self, year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ...) -> None: ...

class PubsubPubMsgReq(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: _any_pb2.Any
    def __init__(self, msg: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class PullLogReq(_message.Message):
    __slots__ = ("session_id", "cursor", "limit")
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    cursor: str
    limit: int
    def __init__(self, session_id: _Optional[str] = ..., cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class LogLine(_message.Message):
    __slots__ = ("no", "text")
    NO_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    no: int
    text: str
    def __init__(self, no: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class PullLogRes(_message.Message):
    __slots__ = ("lines",)
    LINES_FIELD_NUMBER: _ClassVar[int]
    lines: _containers.RepeatedCompositeFieldContainer[LogLine]
    def __init__(self, lines: _Optional[_Iterable[_Union[LogLine, _Mapping]]] = ...) -> None: ...

class MtmServerListReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MtmServer(_message.Message):
    __slots__ = ("url", "title", "type")
    URL_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    url: str
    title: str
    type: str
    def __init__(self, url: _Optional[str] = ..., title: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class MtmServerListRes(_message.Message):
    __slots__ = ("Pagination", "Total", "items")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    Total: int
    items: _containers.RepeatedCompositeFieldContainer[MtmServer]
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., Total: _Optional[int] = ..., items: _Optional[_Iterable[_Union[MtmServer, _Mapping]]] = ...) -> None: ...

class GetMetaReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MtmMeta(_message.Message):
    __slots__ = ("public_url",)
    PUBLIC_URL_FIELD_NUMBER: _ClassVar[int]
    public_url: str
    def __init__(self, public_url: _Optional[str] = ...) -> None: ...

class GetMetaRes(_message.Message):
    __slots__ = ("meta",)
    META_FIELD_NUMBER: _ClassVar[int]
    meta: MtmMeta
    def __init__(self, meta: _Optional[_Union[MtmMeta, _Mapping]] = ...) -> None: ...

class ProtoMeta(_message.Message):
    __slots__ = ("name", "full_name", "package_name", "services", "index")
    class Service(_message.Message):
        __slots__ = ("name", "full_name", "index", "methods", "options")
        class Method(_message.Message):
            __slots__ = ("name", "full_name", "index")
            NAME_FIELD_NUMBER: _ClassVar[int]
            FULL_NAME_FIELD_NUMBER: _ClassVar[int]
            INDEX_FIELD_NUMBER: _ClassVar[int]
            name: str
            full_name: str
            index: int
            def __init__(self, name: _Optional[str] = ..., full_name: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        FULL_NAME_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        METHODS_FIELD_NUMBER: _ClassVar[int]
        OPTIONS_FIELD_NUMBER: _ClassVar[int]
        name: str
        full_name: str
        index: int
        methods: _containers.RepeatedCompositeFieldContainer[ProtoMeta.Service.Method]
        options: str
        def __init__(self, name: _Optional[str] = ..., full_name: _Optional[str] = ..., index: _Optional[int] = ..., methods: _Optional[_Iterable[_Union[ProtoMeta.Service.Method, _Mapping]]] = ..., options: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    name: str
    full_name: str
    package_name: str
    services: _containers.RepeatedCompositeFieldContainer[ProtoMeta.Service]
    index: int
    def __init__(self, name: _Optional[str] = ..., full_name: _Optional[str] = ..., package_name: _Optional[str] = ..., services: _Optional[_Iterable[_Union[ProtoMeta.Service, _Mapping]]] = ..., index: _Optional[int] = ...) -> None: ...

class ServiceMetaReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ServiceMetaRes(_message.Message):
    __slots__ = ("protos",)
    PROTOS_FIELD_NUMBER: _ClassVar[int]
    protos: _containers.RepeatedCompositeFieldContainer[ProtoMeta]
    def __init__(self, protos: _Optional[_Iterable[_Union[ProtoMeta, _Mapping]]] = ...) -> None: ...

class SlugReq(_message.Message):
    __slots__ = ("data_type", "path", "searchParams", "mtm_host")
    class SearchParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SEARCHPARAMS_FIELD_NUMBER: _ClassVar[int]
    MTM_HOST_FIELD_NUMBER: _ClassVar[int]
    data_type: str
    path: str
    searchParams: _containers.ScalarMap[str, str]
    mtm_host: str
    def __init__(self, data_type: _Optional[str] = ..., path: _Optional[str] = ..., searchParams: _Optional[_Mapping[str, str]] = ..., mtm_host: _Optional[str] = ...) -> None: ...

class SlugRes(_message.Message):
    __slots__ = ("metas", "top_nav", "layout", "sider", "sections", "footer", "page", "error", "logs")
    class MetasEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METAS_FIELD_NUMBER: _ClassVar[int]
    TOP_NAV_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    SIDER_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    FOOTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    metas: _containers.ScalarMap[str, str]
    top_nav: TopNav
    layout: str
    sider: PageSider
    sections: _containers.RepeatedCompositeFieldContainer[PageContent]
    footer: PageFooter
    page: PageInfo
    error: str
    logs: _containers.RepeatedCompositeFieldContainer[LogLine]
    def __init__(self, metas: _Optional[_Mapping[str, str]] = ..., top_nav: _Optional[_Union[TopNav, _Mapping]] = ..., layout: _Optional[str] = ..., sider: _Optional[_Union[PageSider, _Mapping]] = ..., sections: _Optional[_Iterable[_Union[PageContent, _Mapping]]] = ..., footer: _Optional[_Union[PageFooter, _Mapping]] = ..., page: _Optional[_Union[PageInfo, _Mapping]] = ..., error: _Optional[str] = ..., logs: _Optional[_Iterable[_Union[LogLine, _Mapping]]] = ...) -> None: ...

class TopNavReq(_message.Message):
    __slots__ = ("data_type", "path", "searchParams", "mtm_host")
    class SearchParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SEARCHPARAMS_FIELD_NUMBER: _ClassVar[int]
    MTM_HOST_FIELD_NUMBER: _ClassVar[int]
    data_type: str
    path: str
    searchParams: _containers.ScalarMap[str, str]
    mtm_host: str
    def __init__(self, data_type: _Optional[str] = ..., path: _Optional[str] = ..., searchParams: _Optional[_Mapping[str, str]] = ..., mtm_host: _Optional[str] = ...) -> None: ...

class TopNavRes(_message.Message):
    __slots__ = ("nav",)
    NAV_FIELD_NUMBER: _ClassVar[int]
    nav: TopNav
    def __init__(self, nav: _Optional[_Union[TopNav, _Mapping]] = ...) -> None: ...

class TopNav(_message.Message):
    __slots__ = ("logo_url", "navs", "layout")
    LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    NAVS_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    logo_url: str
    navs: _containers.RepeatedCompositeFieldContainer[TopNavItem]
    layout: str
    def __init__(self, logo_url: _Optional[str] = ..., navs: _Optional[_Iterable[_Union[TopNavItem, _Mapping]]] = ..., layout: _Optional[str] = ...) -> None: ...

class TopNavItem(_message.Message):
    __slots__ = ("label", "url")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    label: str
    url: str
    def __init__(self, label: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class PageInfo(_message.Message):
    __slots__ = ("title", "logo_url")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    title: str
    logo_url: str
    def __init__(self, title: _Optional[str] = ..., logo_url: _Optional[str] = ...) -> None: ...

class PageSider(_message.Message):
    __slots__ = ("title",)
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class PageFooter(_message.Message):
    __slots__ = ("layout",)
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    layout: str
    def __init__(self, layout: _Optional[str] = ...) -> None: ...

class PageContent(_message.Message):
    __slots__ = ("raw_html", "blog_post", "article_detail", "simple_text")
    RAW_HTML_FIELD_NUMBER: _ClassVar[int]
    BLOG_POST_FIELD_NUMBER: _ClassVar[int]
    ARTICLE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    SIMPLE_TEXT_FIELD_NUMBER: _ClassVar[int]
    raw_html: RawHtmlBlock
    blog_post: BlogPost
    article_detail: ArticleDetailBlock
    simple_text: SimpleText
    def __init__(self, raw_html: _Optional[_Union[RawHtmlBlock, _Mapping]] = ..., blog_post: _Optional[_Union[BlogPost, _Mapping]] = ..., article_detail: _Optional[_Union[ArticleDetailBlock, _Mapping]] = ..., simple_text: _Optional[_Union[SimpleText, _Mapping]] = ...) -> None: ...

class SimpleText(_message.Message):
    __slots__ = ("body",)
    BODY_FIELD_NUMBER: _ClassVar[int]
    body: str
    def __init__(self, body: _Optional[str] = ...) -> None: ...

class UserNav(_message.Message):
    __slots__ = ("layout", "navs")
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    NAVS_FIELD_NUMBER: _ClassVar[int]
    layout: str
    navs: _containers.RepeatedCompositeFieldContainer[TopNavItem]
    def __init__(self, layout: _Optional[str] = ..., navs: _Optional[_Iterable[_Union[TopNavItem, _Mapping]]] = ...) -> None: ...

class UserNavItem(_message.Message):
    __slots__ = ("label", "url", "icon", "access_key")
    LABEL_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    label: str
    url: str
    icon: str
    access_key: str
    def __init__(self, label: _Optional[str] = ..., url: _Optional[str] = ..., icon: _Optional[str] = ..., access_key: _Optional[str] = ...) -> None: ...

class UserinfoRes(_message.Message):
    __slots__ = ("user_info", "navs")
    USER_INFO_FIELD_NUMBER: _ClassVar[int]
    NAVS_FIELD_NUMBER: _ClassVar[int]
    user_info: UserInfo
    navs: _containers.RepeatedCompositeFieldContainer[UserNavItem]
    def __init__(self, user_info: _Optional[_Union[UserInfo, _Mapping]] = ..., navs: _Optional[_Iterable[_Union[UserNavItem, _Mapping]]] = ...) -> None: ...

class BlogNavItem(_message.Message):
    __slots__ = ("category_id", "label", "url")
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    category_id: str
    label: str
    url: str
    def __init__(self, category_id: _Optional[str] = ..., label: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class InputSourceReq(_message.Message):
    __slots__ = ("keyword", "limit")
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    keyword: str
    limit: int
    def __init__(self, keyword: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class InputSourceReply(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[InputSourceItem]
    def __init__(self, items: _Optional[_Iterable[_Union[InputSourceItem, _Mapping]]] = ...) -> None: ...

class InputSourceItem(_message.Message):
    __slots__ = ("title", "value")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    title: str
    value: str
    def __init__(self, title: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class BlogCategorie(_message.Message):
    __slots__ = ("id", "title")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ...) -> None: ...

class BlogCategorieListReq(_message.Message):
    __slots__ = ("Pagination", "q", "site_id", "limit")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    q: str
    site_id: int
    limit: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., q: _Optional[str] = ..., site_id: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class BlogCategorieListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    items: _containers.RepeatedCompositeFieldContainer[BlogCategorie]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[BlogCategorie, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class BlogCategorieGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class BlogCategorieCreateReq(_message.Message):
    __slots__ = ("id", "title", "site_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    site_id: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., site_id: _Optional[int] = ...) -> None: ...

class BlogCategorieCreateReply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class BlogCategorieUpdateReq(_message.Message):
    __slots__ = ("id", "title", "site_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    site_id: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., site_id: _Optional[int] = ...) -> None: ...

class BlogCategorieUpdateReqply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class BlogTag(_message.Message):
    __slots__ = ("id", "title")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ...) -> None: ...

class BlogPost(_message.Message):
    __slots__ = ("id", "site_id", "blog_categorie_id", "updated_at", "title", "content", "content_type", "auth", "published", "post_name", "excerpt", "status", "comment_status", "parent", "type", "mime_type", "comment_count", "tags", "slugs", "top_image", "is_manual", "is_public", "modi_by")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BLOG_CATEGORIE_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    POST_NAME_FIELD_NUMBER: _ClassVar[int]
    EXCERPT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    TOP_IMAGE_FIELD_NUMBER: _ClassVar[int]
    IS_MANUAL_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    MODI_BY_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    blog_categorie_id: int
    updated_at: int
    title: str
    content: str
    content_type: str
    auth: str
    published: bool
    post_name: str
    excerpt: str
    status: str
    comment_status: str
    parent: str
    type: str
    mime_type: str
    comment_count: int
    tags: _containers.RepeatedCompositeFieldContainer[BlogTag]
    slugs: str
    top_image: str
    is_manual: bool
    is_public: bool
    modi_by: str
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ..., blog_categorie_id: _Optional[int] = ..., updated_at: _Optional[int] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., content_type: _Optional[str] = ..., auth: _Optional[str] = ..., published: bool = ..., post_name: _Optional[str] = ..., excerpt: _Optional[str] = ..., status: _Optional[str] = ..., comment_status: _Optional[str] = ..., parent: _Optional[str] = ..., type: _Optional[str] = ..., mime_type: _Optional[str] = ..., comment_count: _Optional[int] = ..., tags: _Optional[_Iterable[_Union[BlogTag, _Mapping]]] = ..., slugs: _Optional[str] = ..., top_image: _Optional[str] = ..., is_manual: bool = ..., is_public: bool = ..., modi_by: _Optional[str] = ...) -> None: ...

class BlogPostItem(_message.Message):
    __slots__ = ("id", "site_id", "title", "updated_at", "content", "content_type", "excerpt", "category", "top_image")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXCERPT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TOP_IMAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    title: str
    updated_at: int
    content: str
    content_type: str
    excerpt: str
    category: BlogCategorie
    top_image: str
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ..., title: _Optional[str] = ..., updated_at: _Optional[int] = ..., content: _Optional[str] = ..., content_type: _Optional[str] = ..., excerpt: _Optional[str] = ..., category: _Optional[_Union[BlogCategorie, _Mapping]] = ..., top_image: _Optional[str] = ...) -> None: ...

class BlogPostGetReq(_message.Message):
    __slots__ = ("id", "slugs")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    slugs: str
    def __init__(self, id: _Optional[int] = ..., slugs: _Optional[str] = ...) -> None: ...

class BlogPostCreateReq(_message.Message):
    __slots__ = ("title", "site_id", "blog_categorie_id", "content")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BLOG_CATEGORIE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    title: str
    site_id: int
    blog_categorie_id: int
    content: str
    def __init__(self, title: _Optional[str] = ..., site_id: _Optional[int] = ..., blog_categorie_id: _Optional[int] = ..., content: _Optional[str] = ...) -> None: ...

class BlogPostUpdateReq(_message.Message):
    __slots__ = ("id", "title", "slugs", "blog_categorie_id", "content", "site_id", "is_manual", "modi_by")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    BLOG_CATEGORIE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_MANUAL_FIELD_NUMBER: _ClassVar[int]
    MODI_BY_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    slugs: str
    blog_categorie_id: int
    content: str
    site_id: int
    is_manual: bool
    modi_by: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., slugs: _Optional[str] = ..., blog_categorie_id: _Optional[int] = ..., content: _Optional[str] = ..., site_id: _Optional[int] = ..., is_manual: bool = ..., modi_by: _Optional[str] = ...) -> None: ...

class BlogPostImportReq(_message.Message):
    __slots__ = ("url", "blog_post_id")
    URL_FIELD_NUMBER: _ClassVar[int]
    BLOG_POST_ID_FIELD_NUMBER: _ClassVar[int]
    url: str
    blog_post_id: str
    def __init__(self, url: _Optional[str] = ..., blog_post_id: _Optional[str] = ...) -> None: ...

class BlogPostListBySlugsReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    items: _containers.RepeatedCompositeFieldContainer[BlogPost]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[BlogPost, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class BlogCleanReq(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RawHtmlBlock(_message.Message):
    __slots__ = ("html",)
    HTML_FIELD_NUMBER: _ClassVar[int]
    html: str
    def __init__(self, html: _Optional[str] = ...) -> None: ...

class ArticleDetailBlock(_message.Message):
    __slots__ = ("site_id", "blog_categorie_id", "updated_at", "title", "content", "content_type", "author", "post_name", "excerpt", "status", "comment_status", "parent", "type", "mime_type", "comment_count", "tags", "slugs", "top_image", "is_manual", "is_public", "modi_by")
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BLOG_CATEGORIE_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    POST_NAME_FIELD_NUMBER: _ClassVar[int]
    EXCERPT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SLUGS_FIELD_NUMBER: _ClassVar[int]
    TOP_IMAGE_FIELD_NUMBER: _ClassVar[int]
    IS_MANUAL_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    MODI_BY_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    blog_categorie_id: int
    updated_at: int
    title: str
    content: str
    content_type: str
    author: str
    post_name: str
    excerpt: str
    status: str
    comment_status: str
    parent: str
    type: str
    mime_type: str
    comment_count: int
    tags: _containers.RepeatedCompositeFieldContainer[BlogTag]
    slugs: str
    top_image: str
    is_manual: bool
    is_public: bool
    modi_by: str
    def __init__(self, site_id: _Optional[int] = ..., blog_categorie_id: _Optional[int] = ..., updated_at: _Optional[int] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., content_type: _Optional[str] = ..., author: _Optional[str] = ..., post_name: _Optional[str] = ..., excerpt: _Optional[str] = ..., status: _Optional[str] = ..., comment_status: _Optional[str] = ..., parent: _Optional[str] = ..., type: _Optional[str] = ..., mime_type: _Optional[str] = ..., comment_count: _Optional[int] = ..., tags: _Optional[_Iterable[_Union[BlogTag, _Mapping]]] = ..., slugs: _Optional[str] = ..., top_image: _Optional[str] = ..., is_manual: bool = ..., is_public: bool = ..., modi_by: _Optional[str] = ...) -> None: ...

class Site(_message.Message):
    __slots__ = ("id", "title", "key_words", "sp_enabled", "hosts")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    KEY_WORDS_FIELD_NUMBER: _ClassVar[int]
    SP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    key_words: _containers.RepeatedScalarFieldContainer[str]
    sp_enabled: bool
    hosts: _containers.RepeatedCompositeFieldContainer[SiteHost]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., key_words: _Optional[_Iterable[str]] = ..., sp_enabled: bool = ..., hosts: _Optional[_Iterable[_Union[SiteHost, _Mapping]]] = ...) -> None: ...

class SiteListReq(_message.Message):
    __slots__ = ("Pagination", "q", "with_hosts")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    WITH_HOSTS_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    q: str
    with_hosts: bool
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., q: _Optional[str] = ..., with_hosts: bool = ...) -> None: ...

class SiteListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    items: _containers.RepeatedCompositeFieldContainer[Site]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Site, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class SiteGetReq(_message.Message):
    __slots__ = ("id", "host_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    host_name: str
    def __init__(self, id: _Optional[int] = ..., host_name: _Optional[str] = ...) -> None: ...

class SiteCreateReq(_message.Message):
    __slots__ = ("id", "title", "domain")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    domain: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...

class SiteCreateRes(_message.Message):
    __slots__ = ("id", "default_domain")
    ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    id: int
    default_domain: str
    def __init__(self, id: _Optional[int] = ..., default_domain: _Optional[str] = ...) -> None: ...

class SiteUpdateReq(_message.Message):
    __slots__ = ("id", "title", "sp_enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    sp_enabled: bool
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., sp_enabled: bool = ...) -> None: ...

class SiteHost(_message.Message):
    __slots__ = ("id", "host")
    ID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    id: int
    host: str
    def __init__(self, id: _Optional[int] = ..., host: _Optional[str] = ...) -> None: ...

class SiteHostListReq(_message.Message):
    __slots__ = ("Pagination", "q", "site_id")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    q: str
    site_id: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., q: _Optional[str] = ..., site_id: _Optional[int] = ...) -> None: ...

class SiteHostListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: Paging
    items: _containers.RepeatedCompositeFieldContainer[SiteHost]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SiteHost, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class SiteHostGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SiteHostCreateReq(_message.Message):
    __slots__ = ("id", "title", "site_id", "host")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    site_id: int
    host: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., site_id: _Optional[int] = ..., host: _Optional[str] = ...) -> None: ...

class SiteHostUpdateReq(_message.Message):
    __slots__ = ("id", "title", "site_id", "host")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    site_id: int
    host: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., site_id: _Optional[int] = ..., host: _Optional[str] = ...) -> None: ...

class SiteImportReq(_message.Message):
    __slots__ = ("text", "create_from", "title", "serve_root_domain")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CREATE_FROM_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERVE_ROOT_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    text: str
    create_from: str
    title: str
    serve_root_domain: str
    def __init__(self, text: _Optional[str] = ..., create_from: _Optional[str] = ..., title: _Optional[str] = ..., serve_root_domain: _Optional[str] = ...) -> None: ...

class DomainCollResult(_message.Message):
    __slots__ = ("root_domain", "title", "Screenshot")
    ROOT_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SCREENSHOT_FIELD_NUMBER: _ClassVar[int]
    root_domain: str
    title: str
    Screenshot: bytes
    def __init__(self, root_domain: _Optional[str] = ..., title: _Optional[str] = ..., Screenshot: _Optional[bytes] = ...) -> None: ...

class EventSpSiteVisit(_message.Message):
    __slots__ = ("hash",)
    HASH_FIELD_NUMBER: _ClassVar[int]
    hash: str
    def __init__(self, hash: _Optional[str] = ...) -> None: ...

class CmdSpSiteTakeScreenshot(_message.Message):
    __slots__ = ("hash",)
    HASH_FIELD_NUMBER: _ClassVar[int]
    hash: str
    def __init__(self, hash: _Optional[str] = ...) -> None: ...

class EventSpSiteScreenshotOk(_message.Message):
    __slots__ = ("hash",)
    HASH_FIELD_NUMBER: _ClassVar[int]
    hash: str
    def __init__(self, hash: _Optional[str] = ...) -> None: ...

class SiteSetupCftunnelReq(_message.Message):
    __slots__ = ("site_id",)
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    def __init__(self, site_id: _Optional[int] = ...) -> None: ...

class SiteSetupCftunnelReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FormSchema(_message.Message):
    __slots__ = ("title", "description", "action", "fields", "group", "layout")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    action: str
    fields: _containers.RepeatedCompositeFieldContainer[FormSchemsField]
    group: str
    layout: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., action: _Optional[str] = ..., fields: _Optional[_Iterable[_Union[FormSchemsField, _Mapping]]] = ..., group: _Optional[str] = ..., layout: _Optional[str] = ...) -> None: ...

class FormSchemsField(_message.Message):
    __slots__ = ("name", "label", "type", "defaultValue", "description", "placeholder")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULTVALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    name: str
    label: str
    type: str
    defaultValue: str
    description: str
    placeholder: str
    def __init__(self, name: _Optional[str] = ..., label: _Optional[str] = ..., type: _Optional[str] = ..., defaultValue: _Optional[str] = ..., description: _Optional[str] = ..., placeholder: _Optional[str] = ...) -> None: ...

class ArtContentClassifyReq(_message.Message):
    __slots__ = ("text", "categories")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    text: str
    categories: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, text: _Optional[str] = ..., categories: _Optional[_Iterable[str]] = ...) -> None: ...

class ArtContentClassifyReply(_message.Message):
    __slots__ = ("best_match_category",)
    BEST_MATCH_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    best_match_category: str
    def __init__(self, best_match_category: _Optional[str] = ...) -> None: ...

class ArtRewriteReq(_message.Message):
    __slots__ = ("id", "title", "content", "candidate_labels")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    content: str
    candidate_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., candidate_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class ArtRewriteReply(_message.Message):
    __slots__ = ("id", "title", "content", "best_match_label")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    BEST_MATCH_LABEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    content: str
    best_match_label: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., content: _Optional[str] = ..., best_match_label: _Optional[str] = ...) -> None: ...

class MtmghConfig(_message.Message):
    __slots__ = ("setup_command", "run_command", "project_type", "dev_init")
    SETUP_COMMAND_FIELD_NUMBER: _ClassVar[int]
    RUN_COMMAND_FIELD_NUMBER: _ClassVar[int]
    PROJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEV_INIT_FIELD_NUMBER: _ClassVar[int]
    setup_command: str
    run_command: str
    project_type: str
    dev_init: DevInitConfig
    def __init__(self, setup_command: _Optional[str] = ..., run_command: _Optional[str] = ..., project_type: _Optional[str] = ..., dev_init: _Optional[_Union[DevInitConfig, _Mapping]] = ...) -> None: ...

class DevInitConfig(_message.Message):
    __slots__ = ("sub_repo_root", "sub_projects", "init_command")
    SUB_REPO_ROOT_FIELD_NUMBER: _ClassVar[int]
    SUB_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    INIT_COMMAND_FIELD_NUMBER: _ClassVar[int]
    sub_repo_root: str
    sub_projects: _containers.RepeatedScalarFieldContainer[str]
    init_command: str
    def __init__(self, sub_repo_root: _Optional[str] = ..., sub_projects: _Optional[_Iterable[str]] = ..., init_command: _Optional[str] = ...) -> None: ...

class CmdkItem(_message.Message):
    __slots__ = ("group", "label", "url", "allowRoles")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ALLOWROLES_FIELD_NUMBER: _ClassVar[int]
    group: str
    label: str
    url: str
    allowRoles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, group: _Optional[str] = ..., label: _Optional[str] = ..., url: _Optional[str] = ..., allowRoles: _Optional[_Iterable[str]] = ...) -> None: ...

class FormGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class FormCreateReq(_message.Message):
    __slots__ = ("input",)
    INPUT_FIELD_NUMBER: _ClassVar[int]
    input: FormSchema
    def __init__(self, input: _Optional[_Union[FormSchema, _Mapping]] = ...) -> None: ...

class TaskMessage(_message.Message):
    __slots__ = ("name", "date")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    date: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class APIResourceMeta(_message.Message):
    __slots__ = ("id", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...
