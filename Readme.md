# Paymentop test task

## General
This tool is designed to calculate payment amounts including internal currency conversion.

## Prerequisites
Customer wallet balance stores currency values according to task as constant:
CUSTOMMER_BALANCE = {'USD': 30, 'GBP': 37, 'AUD': 2, 'CHF': 0.2, 'EUR': 18}

Used currency exchange rates(missing exchange rates are calculated through intermediate currencies):
EXCHANGE_RATE = {'USD/EUR': 0.921624, 'EUR/USD': 1.08504, 'USD/GBP': 0.807053, 'GBP/USD': 1.23908, 'USD/CHF': 0.920560, 'CHF/USD': 1.08630,
                'USD/AUD': 1.43612, 'AUD/USD': 0.69632, 'GBP/CHF': 1.14064, 'CHF/GBP': 0.876698, 'GBP/AUD': 1.77946, 'AUD/GBP': 0.561970,
                'EUR/GBP': 0.87568, 'GBP:EUR': 1.14197, 'CHF/AUD': 1.56013, 'AUD/CHF': 0.640971, 'CHF/EUR': 1.00128, 'EUR/CHF': 0.998717,
                'EUR/AUD': 1.55813, 'AUD/EUR': 0.64179}

## Usage
Input item price (int, float) and currency from list USD, EUR, GBP, CHF, AUD (Lowercase and uppercase are both allowed)

## Results
Output data contains: 
1. User balance for each currency after successful payment
2. Total amount of company fee in EUR
3. Total amount of customer payment in payment currency