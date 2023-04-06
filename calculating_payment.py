CUSTOMMER_BALANCE = {'USD': 30, 'GBP': 37, 'AUD': 2, 'CHF': 0.2, 'EUR': 18}
CONVERSION_BANK_FEE = 2
CONVERSION_COMPANY_FEE = 3
OPERATION_BANK_FEE = 3
OPERATION_COMPANY_FEE = 4
EXCHANGE_RATE = {'USD/EUR': 0.921624, 'EUR/USD': 1.08504, 'USD/GBP': 0.807053, 'GBP/USD': 1.23908, 'USD/CHF': 0.920560, 'CHF/USD': 1.08630,
                'USD/AUD': 1.43612, 'AUD/USD': 0.69632, 'GBP/CHF': 1.14064, 'CHF/GBP': 0.876698, 'GBP/AUD': 1.77946, 'AUD/GBP': 0.561970,
                'EUR/GBP': 0.87568, 'GBP:EUR': 1.14197, 'CHF/AUD': 1.56013, 'AUD/CHF': 0.640971, 'CHF/EUR': 1.00128, 'EUR/CHF': 0.998717,
                'EUR/AUD': 1.55813, 'AUD/EUR': 0.64179} # missing exchange rates are calculated through intermediate currencies

"""Return item price and payment currency from user input"""
def input_price_and_currency():
    print ('Please type item price and press enter:')
    price = input()
    while not price.isdigit():
        print ('Please type valid price value')
        price = input()
    print ('Please type currency from list (USD, EUR, GBP, CHF, AUD):')
    currency = input()
    while currency.lower() not in ['usd', 'eur', 'gbp', 'chf', 'aud']:
        print ('Please type valid currency value from list (USD, EUR, GBP, CHF, AUD)')
        currency = input()
    return float(price), currency.upper()

"""Return item price including 7% operation fee (3% bank fee and 4% company fee)"""
def calculate_price_including_operation_fee(price: float) -> tuple:
    return (price*1.07, price*OPERATION_COMPANY_FEE/100)

"""Checking if total wallet balance greater than item price including operation fee and internal currency conversion fee"""
def check_is_enough_funds(full_price: float, currency: str) -> bool:
    total_funds = 0
    for key, value in CUSTOMMER_BALANCE.items():
        if key != currency:
            total_funds += (value * EXCHANGE_RATE[f'{key}/{currency}']) * (100 - CONVERSION_BANK_FEE - CONVERSION_COMPANY_FEE) / 100
        else:
            total_funds += value
    return True if total_funds >= full_price else False

"""Checking if payment currency balance is enough to make payment including operation fee"""
def check_balance(amount: float, currency: str) -> bool:
    return True if CUSTOMMER_BALANCE[currency] >= amount else False

"""Return currency of wallet with biggest balance"""
def choose_wallet_with_biggest_amount(customer_balance: dict, currency: str) -> str:
    curr = list(customer_balance.values())
    curr.remove(customer_balance[currency])
    max_balance = max(curr)
    for key in customer_balance.keys():
        if customer_balance[key] == max_balance:
            return key

""""Converting currency and updating wallet balance"""
def calculate_conversion_amount_including_conversion_fee(
    customer_balance: dict,
    full_price: float,
    currency_sell: str,
    currency_buy: str,
    customer_payment: float
):
    to_conv_amount = full_price - customer_balance[currency_buy]
    bank_conv_fee = to_conv_amount * CONVERSION_BANK_FEE/100
    company_conv_fee = to_conv_amount * CONVERSION_COMPANY_FEE/100
    to_conv_amount_including_fee = to_conv_amount + bank_conv_fee + company_conv_fee
    if to_conv_amount_including_fee > customer_balance[currency_sell] * EXCHANGE_RATE[f'{currency_sell}/{currency_buy}']:
        converted_amount = customer_balance[currency_sell] * EXCHANGE_RATE[f'{currency_sell}/{currency_buy}']
        bank_conv_fee = converted_amount * CONVERSION_BANK_FEE/100
        company_conv_fee = converted_amount * CONVERSION_COMPANY_FEE/100
        customer_balance[currency_buy] += customer_balance[currency_sell] * EXCHANGE_RATE[f'{currency_sell}/{currency_buy}'] - bank_conv_fee - company_conv_fee
        customer_payment += customer_balance[currency_sell] * EXCHANGE_RATE[f'{currency_sell}/{currency_buy}']
        print(customer_balance[currency_sell] * EXCHANGE_RATE[f'{currency_sell}/{currency_buy}'])
        print (customer_payment)
        print()
        customer_balance[currency_sell] = 0
    else:
        customer_balance[currency_sell] -= to_conv_amount_including_fee / EXCHANGE_RATE[f'{currency_sell}/{currency_buy}']
        customer_payment += to_conv_amount_including_fee
        print(to_conv_amount_including_fee)
        print (customer_payment)
        print()
        customer_balance[currency_buy] += to_conv_amount
    return customer_balance, company_conv_fee, customer_payment

def main():
    customer_balance = CUSTOMMER_BALANCE.copy()
    item_data = input_price_and_currency()
    price, currency = item_data[0], item_data[1]
    prise_and_fee = calculate_price_including_operation_fee(price)
    full_price, company_fee = prise_and_fee[0], prise_and_fee[1]
    customer_payment = customer_balance[currency] if customer_balance[currency] <= full_price else full_price
    if not check_is_enough_funds(full_price, currency):
        print ('Operation error: insufficient funds!')
        customer_balance = CUSTOMMER_BALANCE
        print ('Customer balance:')
        for key, value in customer_balance.items():
            print(f'  {key}: {round (value, 2)}')
    else:
        while customer_balance[currency] < full_price:
            currency_sell = choose_wallet_with_biggest_amount(customer_balance, currency)
            conv_result = calculate_conversion_amount_including_conversion_fee(customer_balance, full_price, currency_sell, currency, customer_payment)
            customer_balance = conv_result[0]
            company_fee += conv_result[1]
            customer_payment = conv_result[2]
        customer_balance[currency] -= full_price
        
        company_fee *= EXCHANGE_RATE[f'EUR/{currency}']
        print ('Operation succeed!')
        print ('Customer balance:')
        for key, value in customer_balance.items():
            print(f'  {key}: {round(value, 2)}')
        print(f'Company fee: {round (company_fee, 2)} EUR')
        print(f'Total customer payment: {round (customer_payment, 2)} {currency}')

if __name__ == "__main__":
    main()
