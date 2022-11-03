from constants_jgb import *
from http import HTTPStatus
from utility import get_page_html
from datetime import timezone, timedelta
from dateutil.relativedelta import relativedelta

class JgbAuctionInfo:
    def __init__(self, tenor):
        self.tenor = tenor
        self.next_auction = datetime(9999, 12, 31).astimezone()
        self.bond_number = None
        self.announcement_link = None
        self.reopen_info = None

    def update_info(self, auction_date, bond_number, announcement_link, reopen_info):
        if self.next_auction > auction_date > TODAY_DATE:
            self.next_auction = auction_date
            self.bond_number = bond_number
            self.announcement_link = announcement_link
            self.reopen_info = reopen_info

    def __str__(self):
        return f"Tenor: {self.tenor}, Next auction: {self.next_auction.strftime('%d-%b-%Y')}, " \
               f"No: {self.bond_number}, Reopen: {self.reopen_info}"


jgb_auction_date = {
    "2-year": JgbAuctionInfo("2Y"),
    "5-year": JgbAuctionInfo("5Y"),
    "10-year": JgbAuctionInfo("10Y"),
    "20-year": JgbAuctionInfo("20Y"),
    "30-year": JgbAuctionInfo("30Y"),
    "40-year": JgbAuctionInfo("40Y"),
    "Inflation-Indexed": JgbAuctionInfo("Inflation-Indexed")
}


def get_auction_date(auction_page):
    auction_table = auction_page.table
    for entry in auction_table.find_all(TR):
        auction_date = None
        bond_number = None
        current_bond = None
        announcement_link = None
        reopen_info = None

        for idx, data in enumerate(entry.find_all(TD)):
            if idx == AUCTION_DATE:
                auction_date = data.string.replace(".", "")
                auction_date = datetime.strptime(auction_date, AUCTION_DATE_FORMAT).replace(
                    tzinfo=timezone(timedelta(hours=9)))

            elif idx == ISSUE:
                issue = re.sub(ISSUE_REGEX, "", data.text)
                if issue in jgb_auction_date.keys():
                    current_bond = jgb_auction_date[issue]
                elif JBI in issue:
                    current_bond = jgb_auction_date[JBI]
                else:
                    break

                bond_number = re.search(ISSUE_REGEX, data.text)
                if bond_number:
                    bond_number = bond_number.group(0).replace("(", "").replace(")", "")

            elif idx == AUCTION_ANNOUNCEMENT:
                if data.a:
                    announcement_link = data.a.get("href")
                    _, announcement_page = get_page_html(announcement_link)
                    reopen_info = get_reopen_info(announcement_page)

            else:
                break

        if current_bond:
            current_bond.update_info(auction_date, bond_number, announcement_link, reopen_info)


def get_reopen_info(announcement_page):
    reopen_info = announcement_page.find_all(TD)[-1].text
    reopen_status = re.search(REOPEN_REGEX, reopen_info)
    if reopen_status:
        return reopen_status.group(0)

    return reopen_status


def run():
    next_date = TODAY_DATE.replace(day=1)

    while any([bond.next_auction.year == 9999 for bond in jgb_auction_date.values()]):
        jgb_auction_url = f"https://www.mof.go.jp/english/policy/jgbs/auction/ca" \
                          f"lendar/{next_date.strftime('%y%m')}e.htm"
        status, response = get_page_html(jgb_auction_url)
        if status != HTTPStatus.OK:
            break

        get_auction_date(response)

        next_date = next_date + relativedelta(months=1)

    return jgb_auction_date


if __name__ == "__main__":
    jgb_auction_date = run()

    for bond in jgb_auction_date.values():
        print(bond.__dict__)
