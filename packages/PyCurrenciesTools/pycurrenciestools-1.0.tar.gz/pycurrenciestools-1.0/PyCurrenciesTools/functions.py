from re import search
from PyWebRequests.functions import find_web_element, get_html
#
#
#
#
def get_exchange_rate(exchanging_currency_tag: str, converted_currency_tag: str):
    return float(
            search(
                    r"\d+\s+%s\s+=\s+(\d+(?:\.\d+)?)\s+%s" % (exchanging_currency_tag.upper(), converted_currency_tag.upper()),
                    find_web_element(
                            get_html(
                                    f"https://currencylive.com/exchange-rate/1000-{exchanging_currency_tag.lower()}-to-{converted_currency_tag.lower()}-exchange-rate-today/"
                            ),
                            "//div[@class=\"rate-info\"]/p[@class=\"text-bold\"]/text()"
                    )
            ).group(1)
    )
#
#
#
#
def exchange_currency(
        exchanging_currency_amount: float,
        exchanging_currency_tag: str,
        converted_currency_tag: str
):
    return exchanging_currency_amount * get_exchange_rate(exchanging_currency_tag, converted_currency_tag)
