"""Inventory app pagination."""

from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class StandardResultsSetPagination(pagination.PageNumberPagination):
    """Default pagination class for inventory api."""

    page_size = 25
    max_page_size = 100

    def get_paginated_response(self, data):
        """Overwrite default pagination to include numbers for pages."""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('numbers', pagination._get_displayed_page_numbers(
                self.page.number, self.page.paginator.num_pages)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))
