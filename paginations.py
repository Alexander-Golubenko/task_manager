from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class StandardPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 50


class StandardCursorPagination(CursorPagination):
    page_size = 6
    ordering = ('id',)
    cursor_query_param = 'cursor'