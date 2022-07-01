import pandas as pd

from constants_ust import *
from utility import get_page_df


def merge_pdf_auction(pdf_file):
    full_table = format_ust_auction_df(pdf_file[0])
    column_name = list(full_table.columns)

    for page in pdf_file[1:]:
        full_table = pd.concat((full_table, format_ust_auction_df(page)))

    full_table = full_table.drop_duplicates(subset=full_table.columns[0], keep="first")
    full_table[ISSUE_YEAR_COLUMN] = full_table[column_name[0]].apply(
        lambda security_type: int(re.search(ISSUE_YEAR_REGEX, security_type).group(1)))
    full_table = full_table.set_index(ISSUE_YEAR_COLUMN)

    return full_table


def format_ust_auction_df(ust_df):
    table = ust_df.drop(ust_df.columns[2], axis=1)
    column_name = list(table.iloc[0])
    column_name[1] = REOPEN_COLUMN
    table.columns = column_name
    table = table.drop(0)

    for column in column_name[2:]:
        table[column] = pd.to_datetime(table[column], format=DATE_FORMAT)
    table = table[table[column_name[0]].str.contains('|'.join(SECURITY_FILTER_LIST))]
    table = table[table[column_name[-2]] >= TODAY_DATE]

    return table


if __name__ == "__main__":
    ust_schedule_url = "https://home.treasury.gov/system/files/221/Tentative-Auction-Schedule.pdf"
    status, response = get_page_df(ust_schedule_url)

    auction_df = merge_pdf_auction(response)
    print(auction_df)
