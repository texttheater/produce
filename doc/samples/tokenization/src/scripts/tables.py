"""Library for pretty-printing tables."""

import util

from util import out, nl

def print_table(table, rowsortkey=None, columnsortkey=None, defaultvalue=''):
    # Get the row and column heads:
    row_heads = list(table.keys())
    column_heads = util.list_union(map(lambda x: x.keys(), table.values()))
    if rowsortkey:
        row_heads.sort(key=rowsortkey)
    if columnsortkey:
        column_heads.sort(key=columnsortkey)
    # Determine the width of each column:
    column_widths = {}
    for column_head in column_heads:
        column_widths[column_head] = max(len(str(column_head)),
                len(str(defaultvalue)))
        for row_head, row in table.items():
            if column_head in row:
                column_widths[column_head] = max(column_widths[column_head],
                        len(str(row[column_head])))
    # Determine the width of the head column:
    head_column_width = max(map(len, map(str, row_heads)))
    # Print the table:
    print_head_row(column_heads, head_column_width, column_widths)
    for row_head in row_heads:
        print_row(row_head, table[row_head], head_column_width, column_heads,
                column_widths, defaultvalue)

def print_head_row(column_heads, head_column_width, column_widths):
    out(' ' * head_column_width)
    for column_head in column_heads:
        width = column_widths[column_head]
        print_cell(column_head, width)
    print

def print_row(row_head, row, head_column_width, column_heads, column_widths,
           defaultvalue):
    print_cell(row_head, head_column_width, leftmargin=0)
    for column_head in column_heads:
        try:
            content = row[column_head]
        except KeyError:
            content = defaultvalue
        print_cell(content, column_widths[column_head])
    nl()

def print_cell(content, width, leftmargin=1):
    out(' ' * leftmargin)
    string = str(content)
    pad = (width - len(string)) * ' '
    if util.isnumber(content):
        out(pad + string)
    else:
        out(string + pad)
