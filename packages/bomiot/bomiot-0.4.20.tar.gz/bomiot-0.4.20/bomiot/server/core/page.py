from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.exceptions import APIException


class CorePageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 30
    page_size_query_param = "max_page"
    max_page_size = 1000
