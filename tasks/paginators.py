from rest_framework.pagination import PageNumberPagination


class TaskPaginator(PageNumberPagination):
    """
        Пагинатор для курсов.

        Attributes:
            page_size (int): Количество элементов на странице по умолчанию.
            page_size_query_param (str): Название параметра запроса для указания размера страницы.
            max_page_size (int): Максимальное количество элементов на странице.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
