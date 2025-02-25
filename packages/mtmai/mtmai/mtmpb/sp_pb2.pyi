from mtmai.mtmpb import mtm_pb2 as _mtm_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpSiteConfig(_message.Message):
    __slots__ = ("id", "inj_script", "cache_disable")
    ID_FIELD_NUMBER: _ClassVar[int]
    INJ_SCRIPT_FIELD_NUMBER: _ClassVar[int]
    CACHE_DISABLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    inj_script: str
    cache_disable: bool
    def __init__(self, id: _Optional[str] = ..., inj_script: _Optional[str] = ..., cache_disable: bool = ...) -> None: ...

class SpField(_message.Message):
    __slots__ = ("id", "sp_route_id", "name", "sel", "sel_val", "do", "value", "val_grap", "type", "value_type", "Extends", "disabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    SP_ROUTE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEL_FIELD_NUMBER: _ClassVar[int]
    SEL_VAL_FIELD_NUMBER: _ClassVar[int]
    DO_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VAL_GRAP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    id: int
    sp_route_id: int
    name: str
    sel: str
    sel_val: str
    do: str
    value: str
    val_grap: str
    type: str
    value_type: str
    Extends: str
    disabled: bool
    def __init__(self, id: _Optional[int] = ..., sp_route_id: _Optional[int] = ..., name: _Optional[str] = ..., sel: _Optional[str] = ..., sel_val: _Optional[str] = ..., do: _Optional[str] = ..., value: _Optional[str] = ..., val_grap: _Optional[str] = ..., type: _Optional[str] = ..., value_type: _Optional[str] = ..., Extends: _Optional[str] = ..., disabled: bool = ...) -> None: ...

class SpSlugsReq(_message.Message):
    __slots__ = ("host", "path")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    host: str
    path: str
    def __init__(self, host: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class SpPageHead(_message.Message):
    __slots__ = ("node_name", "attrs", "text")
    class AttrsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    attrs: _containers.ScalarMap[str, str]
    text: str
    def __init__(self, node_name: _Optional[str] = ..., attrs: _Optional[_Mapping[str, str]] = ..., text: _Optional[str] = ...) -> None: ...

class SpPage(_message.Message):
    __slots__ = ("heads", "content")
    HEADS_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    heads: _containers.RepeatedCompositeFieldContainer[SpPageHead]
    content: str
    def __init__(self, heads: _Optional[_Iterable[_Union[SpPageHead, _Mapping]]] = ..., content: _Optional[str] = ...) -> None: ...

class SpSiteEnableReq(_message.Message):
    __slots__ = ("id", "enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: str
    enabled: bool
    def __init__(self, id: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class SpContentmodi(_message.Message):
    __slots__ = ("id", "site_id", "action", "sel", "value", "description", "priority", "title")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    action: str
    sel: str
    value: str
    description: str
    priority: int
    title: str
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ..., action: _Optional[str] = ..., sel: _Optional[str] = ..., value: _Optional[str] = ..., description: _Optional[str] = ..., priority: _Optional[int] = ..., title: _Optional[str] = ...) -> None: ...

class SpContentmodiListReq(_message.Message):
    __slots__ = ("Pagination", "site_id", "q")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    site_id: int
    q: str
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., site_id: _Optional[int] = ..., q: _Optional[str] = ...) -> None: ...

class SpContentmodiListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[SpContentmodi]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SpContentmodi, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class SpContentmodiGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SpContentmodiCreateReq(_message.Message):
    __slots__ = ("id", "site_id", "action", "sel", "value", "description", "priority", "title")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    action: str
    sel: str
    value: str
    description: str
    priority: int
    title: str
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ..., action: _Optional[str] = ..., sel: _Optional[str] = ..., value: _Optional[str] = ..., description: _Optional[str] = ..., priority: _Optional[int] = ..., title: _Optional[str] = ...) -> None: ...

class SpContentmodiUpdateReq(_message.Message):
    __slots__ = ("id", "title", "site_id", "action", "sel", "value", "description", "priority")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    site_id: int
    action: str
    sel: str
    value: str
    description: str
    priority: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., site_id: _Optional[int] = ..., action: _Optional[str] = ..., sel: _Optional[str] = ..., value: _Optional[str] = ..., description: _Optional[str] = ..., priority: _Optional[int] = ...) -> None: ...

class SpiderField(_message.Message):
    __slots__ = ("name", "selector", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    selector: str
    type: str
    def __init__(self, name: _Optional[str] = ..., selector: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class SpProjectReloadReq(_message.Message):
    __slots__ = ("id", "remove_cache")
    ID_FIELD_NUMBER: _ClassVar[int]
    REMOVE_CACHE_FIELD_NUMBER: _ClassVar[int]
    id: int
    remove_cache: bool
    def __init__(self, id: _Optional[int] = ..., remove_cache: bool = ...) -> None: ...

class SpProject(_message.Message):
    __slots__ = ("id", "title", "routes")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    routes: _containers.RepeatedCompositeFieldContainer[SpRoute]
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., routes: _Optional[_Iterable[_Union[SpRoute, _Mapping]]] = ...) -> None: ...

class SpProjectGetReq(_message.Message):
    __slots__ = ("host", "id", "site_id")
    HOST_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    host: str
    id: int
    site_id: int
    def __init__(self, host: _Optional[str] = ..., id: _Optional[int] = ..., site_id: _Optional[int] = ...) -> None: ...

class SpProjectCreateReq(_message.Message):
    __slots__ = ("site_id",)
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    def __init__(self, site_id: _Optional[int] = ...) -> None: ...

class SpProjectUpdateReq(_message.Message):
    __slots__ = ("id", "title", "host", "sp_site_id", "domain_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SP_SITE_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    host: str
    sp_site_id: str
    domain_id: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., host: _Optional[str] = ..., sp_site_id: _Optional[str] = ..., domain_id: _Optional[str] = ...) -> None: ...

class SpProjectListReq(_message.Message):
    __slots__ = ("Pagination", "q", "site_id")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    q: str
    site_id: int
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., q: _Optional[str] = ..., site_id: _Optional[int] = ...) -> None: ...

class SpProjectListReply(_message.Message):
    __slots__ = ("Pagination", "Total", "items")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    Total: int
    items: _containers.RepeatedCompositeFieldContainer[SpProject]
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., Total: _Optional[int] = ..., items: _Optional[_Iterable[_Union[SpProject, _Mapping]]] = ...) -> None: ...

class SpiderProjectRunReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SpProjectBindHostnameReq(_message.Message):
    __slots__ = ("hostname", "sp_project_id")
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    SP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    sp_project_id: str
    def __init__(self, hostname: _Optional[str] = ..., sp_project_id: _Optional[str] = ...) -> None: ...

class SpiderTrace(_message.Message):
    __slots__ = ("id", "url", "ProjectId")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROJECTID_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    ProjectId: str
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., ProjectId: _Optional[str] = ...) -> None: ...

class SpiderTraceListReq(_message.Message):
    __slots__ = ("keyword", "Pagination")
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    keyword: str
    Pagination: _mtm_pb2.Paging
    def __init__(self, keyword: _Optional[str] = ..., Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ...) -> None: ...

class SpiderTraceListReply(_message.Message):
    __slots__ = ("Pagination", "items")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[SpiderTrace]
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SpiderTrace, _Mapping]]] = ...) -> None: ...

class SpiderTraceGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SpiderTraceGetReply(_message.Message):
    __slots__ = ("rawResBody",)
    RAWRESBODY_FIELD_NUMBER: _ClassVar[int]
    rawResBody: str
    def __init__(self, rawResBody: _Optional[str] = ...) -> None: ...

class SpiderTraceCreateReq(_message.Message):
    __slots__ = ("id", "url", "ProjectId")
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROJECTID_FIELD_NUMBER: _ClassVar[int]
    id: str
    url: str
    ProjectId: str
    def __init__(self, id: _Optional[str] = ..., url: _Optional[str] = ..., ProjectId: _Optional[str] = ...) -> None: ...

class SpiderProjectVisitReq(_message.Message):
    __slots__ = ("project_id", "url")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    url: str
    def __init__(self, project_id: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class SpiderResult(_message.Message):
    __slots__ = ("key", "content")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    key: str
    content: str
    def __init__(self, key: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class SpiderResultListReq(_message.Message):
    __slots__ = ("Pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ...) -> None: ...

class SpiderResultListReply(_message.Message):
    __slots__ = ("Pagination", "items")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[SpiderResult]
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SpiderResult, _Mapping]]] = ...) -> None: ...

class SpiderResultGetReq(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: str
    def __init__(self, key: _Optional[str] = ...) -> None: ...

class SpiderResultGetReply(_message.Message):
    __slots__ = ("key", "content")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    key: str
    content: str
    def __init__(self, key: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class SpRoute(_message.Message):
    __slots__ = ("id", "title", "host_pattern", "path_pattern", "enabled", "priority", "sp_project_id", "type", "value")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    HOST_PATTERN_FIELD_NUMBER: _ClassVar[int]
    PATH_PATTERN_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    host_pattern: str
    path_pattern: str
    enabled: bool
    priority: int
    sp_project_id: int
    type: str
    value: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., host_pattern: _Optional[str] = ..., path_pattern: _Optional[str] = ..., enabled: bool = ..., priority: _Optional[int] = ..., sp_project_id: _Optional[int] = ..., type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SpRouteListReq(_message.Message):
    __slots__ = ("Pagination", "sp_project_id", "site_id", "q")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SP_PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    sp_project_id: int
    site_id: int
    q: str
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., sp_project_id: _Optional[int] = ..., site_id: _Optional[int] = ..., q: _Optional[str] = ...) -> None: ...

class SpRouteListReply(_message.Message):
    __slots__ = ("Pagination", "Total", "items")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    Total: int
    items: _containers.RepeatedCompositeFieldContainer[SpRoute]
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., Total: _Optional[int] = ..., items: _Optional[_Iterable[_Union[SpRoute, _Mapping]]] = ...) -> None: ...

class SpRouteGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SpRouteCreateReq(_message.Message):
    __slots__ = ("site_id", "title", "host_pattern", "path_pattern", "type", "value")
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    HOST_PATTERN_FIELD_NUMBER: _ClassVar[int]
    PATH_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    title: str
    host_pattern: str
    path_pattern: str
    type: str
    value: str
    def __init__(self, site_id: _Optional[int] = ..., title: _Optional[str] = ..., host_pattern: _Optional[str] = ..., path_pattern: _Optional[str] = ..., type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SpRouteUpdateReq(_message.Message):
    __slots__ = ("id", "title", "host_pattern", "path_pattern", "enabled", "priority", "type", "value")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    HOST_PATTERN_FIELD_NUMBER: _ClassVar[int]
    PATH_PATTERN_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    host_pattern: str
    path_pattern: str
    enabled: bool
    priority: int
    type: str
    value: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., host_pattern: _Optional[str] = ..., path_pattern: _Optional[str] = ..., enabled: bool = ..., priority: _Optional[int] = ..., type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class SpOptionGetReq(_message.Message):
    __slots__ = ("site_id",)
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    def __init__(self, site_id: _Optional[int] = ...) -> None: ...

class SpOption(_message.Message):
    __slots__ = ("site_id", "enabled_front_script", "enabled_response_cache")
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FRONT_SCRIPT_FIELD_NUMBER: _ClassVar[int]
    ENABLED_RESPONSE_CACHE_FIELD_NUMBER: _ClassVar[int]
    site_id: int
    enabled_front_script: bool
    enabled_response_cache: bool
    def __init__(self, site_id: _Optional[int] = ..., enabled_front_script: bool = ..., enabled_response_cache: bool = ...) -> None: ...

class SpCrawler(_message.Message):
    __slots__ = ("id", "site_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ...) -> None: ...

class SpCrawlerListReq(_message.Message):
    __slots__ = ("Pagination", "site_id", "q")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    site_id: int
    q: str
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., site_id: _Optional[int] = ..., q: _Optional[str] = ...) -> None: ...

class SpCrawlerListReply(_message.Message):
    __slots__ = ("Pagination", "items", "Total")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    Pagination: _mtm_pb2.Paging
    items: _containers.RepeatedCompositeFieldContainer[SpCrawler]
    Total: int
    def __init__(self, Pagination: _Optional[_Union[_mtm_pb2.Paging, _Mapping]] = ..., items: _Optional[_Iterable[_Union[SpCrawler, _Mapping]]] = ..., Total: _Optional[int] = ...) -> None: ...

class SpCrawlerGetReq(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SpCrawlerCreateReq(_message.Message):
    __slots__ = ("id", "site_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ...) -> None: ...

class SpCrawlerUpdateReq(_message.Message):
    __slots__ = ("id", "site_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    site_id: int
    def __init__(self, id: _Optional[int] = ..., site_id: _Optional[int] = ...) -> None: ...

class SpSiteListItem(_message.Message):
    __slots__ = ("hash", "target_domain", "title", "serve_home_url")
    HASH_FIELD_NUMBER: _ClassVar[int]
    TARGET_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERVE_HOME_URL_FIELD_NUMBER: _ClassVar[int]
    hash: str
    target_domain: str
    title: str
    serve_home_url: str
    def __init__(self, hash: _Optional[str] = ..., target_domain: _Optional[str] = ..., title: _Optional[str] = ..., serve_home_url: _Optional[str] = ...) -> None: ...

class SpConfig(_message.Message):
    __slots__ = ("bind_hosts", "target_host")
    BIND_HOSTS_FIELD_NUMBER: _ClassVar[int]
    TARGET_HOST_FIELD_NUMBER: _ClassVar[int]
    bind_hosts: _containers.RepeatedScalarFieldContainer[str]
    target_host: str
    def __init__(self, bind_hosts: _Optional[_Iterable[str]] = ..., target_host: _Optional[str] = ...) -> None: ...

class Sp2FetchReq(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class Sp2FetchRes(_message.Message):
    __slots__ = ("body",)
    BODY_FIELD_NUMBER: _ClassVar[int]
    body: str
    def __init__(self, body: _Optional[str] = ...) -> None: ...
