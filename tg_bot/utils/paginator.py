from math import ceil


class PaginatorError(Exception):
    """Ошибка пагинации списка"""


class Paginator:

    ELLIPSIS = "..."

    def __init__(self, object_list, page_size):
        self.object_list = object_list
        self.page_size = page_size

    @property
    def page_counter(self):
        if len(self.object_list) == 0:
            return 0

        return ceil(self.count/self.page_size)

    @property
    def count(self):
        return len(self.object_list)

    @property
    def get_pages(self):
        return range(1, self.page_counter+1)

    def page(self, num):
        if num < 1:
            raise PaginatorError("Не удалось получить страницу с задачами")
        bottom = (num-1) * self.page_size
        top = bottom+self.page_size
        return self.page_builder(self.object_list[bottom:top], num, self)

    def page_builder(self, *args, **kwargs):
        return Page(*args, **kwargs)

    def get_pages_markup(self, number=1, on_each_side=2, on_ends=2):
        if self.page_counter <= (on_each_side+on_ends):
            yield from self.get_pages
            return

        if number > (1+on_each_side + on_ends)+1:
            yield from range(1, on_ends+1)
            yield self.ELLIPSIS
            yield from range(number-on_each_side, number+1)
        else:
            yield from range(1, number+1)

        if number < (self.page_counter-on_each_side - on_ends)-1:
            yield from range(number+1, number+on_each_side+1)
            yield self.ELLIPSIS
            yield from range(self.page_counter-on_ends, self.page_counter+1)
        else:
            yield from range(number + 1, self.num_pages + 1)


class Page:
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __iter__(self):
        for elem in self.object_list:
            yield elem

    def has_prev(self):
        return self.number > 1

    def has_next(self):
        return self.number+1 < self.paginator.page_counter
