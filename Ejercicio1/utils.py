from yahoofinancials import YahooFinancials

def get_currency(to_date,from_date,period,change):

    currencies = [change]
    yahoo_financials_currencies = YahooFinancials(currencies)
    
    return yahoo_financials_currencies.get_historical_price_data(to_date,from_date,period)






