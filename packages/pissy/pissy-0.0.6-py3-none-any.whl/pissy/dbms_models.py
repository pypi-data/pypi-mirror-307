from dataclasses import dataclass
from typing import List

type Row = List[any]


@dataclass
class ColumnField(object):
    columnName: str
    sqlType: int


class MultiRows(object):
    __row_num: int = 0
    __row_list: List[Row]
    __column_list: List[ColumnField]
    __read_pos: int = 0

    def __init__(self, column_list: List[ColumnField]):
        self.__column_list = column_list
        self.__row_list = []

    def __iter__(self):
        """
        make it an iterable object
        :return:
        """
        return iter(self.__row_list)

    def __next__(self):
        """
        make it an iterable object
        :return:
        """
        __row: Row = self.__row_list[self.__read_pos]
        self.__read_pos = self.__read_pos + 1
        return __row

    def get_rows_len(self) -> int:
        """
        get row num
        :return:
        """
        return self.__row_num

    def add_row(self, row: Row):
        """
        add row
        :param row:
        :return:
        """
        # compare column size
        if len(row) != len(self.__column_list):
            raise
        self.__row_list.append(row)
        self.__row_num = self.__row_num + 1
