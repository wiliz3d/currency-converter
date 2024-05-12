from django.shortcuts import render
import requests
import logging

def home(request):
    # New currency API URL and key
    currency_api_url ='https://currency-exchange.p.rapidapi.com/listquotes'
    api_key = 'fca_live_3YsQSyNMvJT0JBCT4jEH1MRVbWh6TGkYKYljjRSr'

    try:
        response = requests.get(f'{currency_api_url}?apikey={api_key}')
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        print(data)  # Print the API response data
        currency_options = list(data.get('rates', {}).keys())  # Extract currency codes from API response
        error_message = None  # No error message when everything is successful
    except requests.RequestException as e:
        logging.error(f"Error fetching currency options from API: {e}")
        error_message = "Failed to fetch currency options. Please try again later."
        currency_options = ['USD', 'EUR', 'GBP'] 

    # Return the rendered template outside of the except block
    return render(request, 'home.html', {'currency_options': currency_options, 'error_message': error_message})



def convert_currency(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']

        # New currency API URL and key
        currency_api_url = 'https://api.freecurrencyapi.com/v1/latest'
        api_key = 'fca_live_3YsQSyNMvJT0JBCT4jEH1MRVbWh6TGkYKYljjRSr'
        
        
        try:
            # Fetch exchange rates from the new API
            response = requests.get(f'{currency_api_url}?apikey={api_key}')
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            rates = data.get('rates', {})

            if to_currency in rates:
                exchange_rate = rates[to_currency]
                converted_amount = amount * exchange_rate
                context = {
                    'amount': amount,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'converted_amount': converted_amount
                }
                return render(request, 'result.html', context)
            else:
                error_message = f"Currency code '{to_currency}' not found."
        except requests.RequestException as e:
            logging.error(f"Error fetching exchange rates from API: {e}")
            error_message = "Failed to fetch exchange rates. Please try again later."

        return render(request, 'home.html', {'error_message': error_message})

    else:
        # If request method is not POST, redirect to the home page
        return render(request, 'home.html')
