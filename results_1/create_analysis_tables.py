import copy
import csv
import glob
import itertools
import os
from pathlib import Path
from typing import Dict, List, Tuple


#############################   Stack overflow helper code   ############################
# Taken from: https://stackoverflow.com/questions/13394140/generate-markdown-tables
# Translation dictionaries for table alignment
left_rule = {'<': ':', '^': ':', '>': '-'}
right_rule = {'<': '-', '^': ':', '>': ':'}


def evalute_field(record, field_spec):
    """
    Evalute a field of a record using the type of the field_spec as a guide.
    """
    if type(field_spec) is int:
        return str(record[field_spec])
    elif type(field_spec) is str:
        return str(getattr(record, field_spec))
    else:
        return str(field_spec(record))


def table(file, records, fields, headings, alignment = None):
    """
    Generate a Doxygen-flavor Markdown table from records.

    file -- Any object with a 'write' method that takes a single string
        parameter.
    records -- Iterable.  Rows will be generated from this.
    fields -- List of fields for each row.  Each entry may be an integer,
        string or a function.  If the entry is an integer, it is assumed to be
        an index of each record.  If the entry is a string, it is assumed to be
        a field of each record.  If the entry is a function, it is called with
        the record and its return value is taken as the value of the field.
    headings -- List of column headings.
    alignment - List of pairs alignment characters.  The first of the pair
        specifies the alignment of the header, (Doxygen won't respect this, but
        it might look good, the second specifies the alignment of the cells in
        the column.

        Possible alignment characters are:
            '<' = Left align (default for cells)
            '>' = Right align
            '^' = Center (default for column headings)
    """

    num_columns = len(fields)
    assert len(headings) == num_columns

    # Compute the table cell data
    columns = [[] for i in range(num_columns)]
    for record in records:
        for i, field in enumerate(fields):
            columns[i].append(evalute_field(record, field))

    # Fill out any missing alignment characters.
    extended_align = alignment if alignment != None else []
    if len(extended_align) > num_columns:
        extended_align = extended_align[0:num_columns]
    elif len(extended_align) < num_columns:
        extended_align += [('^', '<')
                           for i in range[num_columns-len(extended_align)]]

    heading_align, cell_align = [x for x in zip(*extended_align)]

    field_widths = [len(max(column, key=len)) if len(column) > 0 else 0
                    for column in columns]
    heading_widths = [max(len(head), 2) for head in headings]
    column_widths = [max(x) for x in zip(field_widths, heading_widths)]

    _ = ' | '.join(['{:' + a + str(w) + '}'
                    for a, w in zip(heading_align, column_widths)])
    heading_template = '| ' + _ + ' |'
    _ = ' | '.join(['{:' + a + str(w) + '}'
                    for a, w in zip(cell_align, column_widths)])
    row_template = '| ' + _ + ' |'

    _ = ' | '.join([left_rule[a] + '-'*(w-2) + right_rule[a]
                    for a, w in zip(cell_align, column_widths)])
    ruling = '| ' + _ + ' |'

    file.write(heading_template.format(*headings).rstrip() + '\n')
    file.write(ruling.rstrip() + '\n')
    for row in zip(*columns):
        file.write(row_template.format(*row).rstrip() + '\n')

###########################   Stack overflow helper code end  ###########################


DIR_PATH = os.path.dirname(__file__)
SIMPLE_OVERVIEW_TABLE_PATH = os.path.join(DIR_PATH, "simple_overview_table.md")
DETAILED_OVERVIEW_TABLE_PATH = os.path.join(DIR_PATH, "detailed_overview_table.md")

MOST_EXTREME_SHORT_SQUEEZES_MCAP_1000_TABLE_PATH = os.path.join(DIR_PATH, "most_extreme_short_squeezes_min_1000.md")
MOST_EXTREME_SHORT_MCAP_1000_SQUEEZES_PATTERN = os.path.join(DIR_PATH, "*_min_1000_multi_5_days_5.csv")
MOST_EXTREME_SHORT_SQUEEZES_MCAP_10_TABLE_PATH = os.path.join(DIR_PATH, "most_extreme_short_squeezes_min_10.md")
MOST_EXTREME_SHORT_MCAP_10_SQUEEZES_PATTERN = os.path.join(DIR_PATH, "*_min_10_multi_5_days_5.csv")

UNFILTERED_TICKER_COUNTS_CSV_PATH = os.path.join(DIR_PATH, "unfiltered_ticker_counts.csv")
FILTER_FILES_NAME_PATTERN = os.path.join(DIR_PATH, "*_min_*_multi_*_days_*.csv")


def file_paths(file_pattern: str) -> List[str]:
    return sorted(path for path in glob.glob(file_pattern))


def filter_values_from_file_path(file_path) -> List[str]:
    tokens = Path(file_path).stem.split("_")
    return [tokens[0], tokens[2], tokens[4], tokens[6]]


def read_filter_file(file_path: str) -> List[List[str]]:
    with open(file_path) as fd:
        reader = csv.reader(fd)
        return [row for i, row in enumerate(reader) if i != 0]


def read_unfiltered_ticket_counts() -> Dict[str, Dict[str, str]]:
    with open(UNFILTERED_TICKER_COUNTS_CSV_PATH) as fd:
        reader = csv.reader(fd)
        rows = [row for i, row in enumerate(reader) if i != 0]

    result = dict()
    for key1, key2, value in rows:
        result.setdefault(key1, {}).update({key2: value})
    return result


def generate_overview_table_data(file_pattern: str) -> Tuple[List[List[str]], List[List[str]]]:
    unfiltered_ticker_counts = read_unfiltered_ticket_counts()

    detailed_overview_data = []
    for path in file_paths(file_pattern):
        filter_values = filter_values_from_file_path(path)
        exchange = filter_values[0]
        min_mcap = filter_values[1]
        file_lines = read_filter_file(path)  # headers are already removed
        ticker_count = len(file_lines)
        unfiltered_count = unfiltered_ticker_counts[exchange][min_mcap]
        relative_to_unfiltered_count_in_percent = (100 * float(ticker_count) /
                                                   float(unfiltered_count))
        record = filter_values + [ticker_count, f"{relative_to_unfiltered_count_in_percent:.2f}%"]
        detailed_overview_data.append(record)

    simple_overview_data = copy.deepcopy(detailed_overview_data)
    # Filter only 2 or 5 times price increase:
    simple_overview_data = [row for row in simple_overview_data if row[2] in ["2", "5"]]
    # Filter only 5 days:
    simple_overview_data = [row for row in simple_overview_data if row[3] in ["5"]]
    # Remove exchange column:
    simple_overview_data = [row[1:] for row in simple_overview_data if row[3] in ["5"]]
    # Aggregate across duplicates:
    simple_overview_data = sorted(simple_overview_data, key=lambda r: (r[0], r[1], r[2]), reverse=True)
    simple_overview_data = [[r1[0], r1[1], r1[2], r1[3] + r2[3] + r3[3]] for r1, r2, r3
                            in itertools.zip_longest(simple_overview_data[::3],
                                                     simple_overview_data[1::3],
                                                     simple_overview_data[2::3],
                                                     fillvalue=[None, None, None, 0])
                            ]  # Aggregate from three exchanges
    # Add `relative to unfiltered count` again:
    for row in simple_overview_data:
        min_mcap = row[0]  # At this point row[0] is the min market cap (we removed exchanges)
        ticker_count = row[3]  # We previously removed the relative count
        unfiltered_count = sum(int(v[min_mcap]) for v in unfiltered_ticker_counts.values())
        relative_to_unfiltered_count_in_percent = (100 * float(ticker_count) /
                                                   float(unfiltered_count))
        row.append(f"{relative_to_unfiltered_count_in_percent:.2f}%")

    return detailed_overview_data, simple_overview_data


def create_simple_table_file(table_data, file_path):
    headings = ['Min Market Cap',
                'Price increase multiplier (2 = 100% increase, 3 = 200%, 5=400%)',
                'Consecutive days', 'Stock count',
                'Relative to all stocks from exchange with min market cap']
    fields = [0, 1, 2, 3, 4]
    align = [('^', '<'), ('^', '^'), ('^', '<'), ('^', '<'), ('^', '>')]

    with open(file_path, mode="w") as fd:
        table(fd, table_data, fields, headings, align)


def create_detailed_table_file(table_data, file_path):
    headings = ['Exchange', 'Min Market Cap',
                'Price increase multiplier (2 = 100% increase, 3 = 200%, 5=400%)',
                'Consecutive days', 'Stock count',
                'Relative to all stocks from exchange with min market cap']
    fields = [0, 1, 2, 3, 4, 5]
    align = [('^', '<'), ('^', '^'), ('^', '<'), ('^', '<'), ('^', '>'), ('^', '>')]

    with open(file_path, mode="w") as fd:
        table(fd, table_data, fields, headings, align)


def generate_most_extreme_short_squeeze_data(file_pattern: str) -> List[List[str]]:
    table_data = []
    for path in file_paths(file_pattern):
        file_lines = read_filter_file(path)  # headers are already removed
        table_data.extend(file_lines)
    # Sort by ticker name:
    return sorted(table_data, key=lambda r: (r[0]))


def create_most_extreme_short_squeezes_table(table_data, file_path):
    headings = ['Ticker', 'Date (the increase was observed)',
                'Adjusted Close Price (at given date)',
                'Price increase (between lowest price of the previous 5 trading days and price at given date)']
    fields = [0, 1, 2, 3]
    align = [('^', '^'), ('^', '^'), ('^', '^'), ('^', '^')]

    with open(file_path, mode="w") as fd:
        table(fd, table_data, fields, headings, align)


# Code entry point
# Create overview tables
(detailed_data,
 simple_data) = generate_overview_table_data(FILTER_FILES_NAME_PATTERN)
create_simple_table_file(simple_data, SIMPLE_OVERVIEW_TABLE_PATH)
create_detailed_table_file(detailed_data, DETAILED_OVERVIEW_TABLE_PATH)

# Create extreme short squeeze ticker tables
mcap_1000_data = generate_most_extreme_short_squeeze_data(MOST_EXTREME_SHORT_MCAP_1000_SQUEEZES_PATTERN)
create_most_extreme_short_squeezes_table(mcap_1000_data, MOST_EXTREME_SHORT_SQUEEZES_MCAP_1000_TABLE_PATH)

mcap_10_data = generate_most_extreme_short_squeeze_data(MOST_EXTREME_SHORT_MCAP_10_SQUEEZES_PATTERN)
create_most_extreme_short_squeezes_table(mcap_10_data, MOST_EXTREME_SHORT_SQUEEZES_MCAP_10_TABLE_PATH)
