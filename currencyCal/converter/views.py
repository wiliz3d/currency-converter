from django.shortcuts import render
import requests
from django.http import JsonResponse

import logging

import logging

def home(request):
    currency_api_url = 'https://v6.exchangerate-api.com/v6/6fff097d8ca1d4052c9364f9/latest/USD'  # Example API URL

    try:
        response = requests.get(currency_api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        currency_options = list(data.get('conversion_rates', {}).keys())  # Extract currency codes from API response
        error_message = None  # No error message when everything is successful
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        error_message = "Failed to fetch currency options due to a server error. Please try again later."
        currency_options = ['USD', 'EUR', 'GBP']  # Fallback to default currency options
    except Exception as err:
        logging.error(f"Error occurred while fetching currency options: {err}")
        error_message = "Failed to fetch currency options. Please try again later."
        currency_options = ['USD', 'EUR', 'GBP']  # Fallback to default currency options

    return render(request, 'home.html', {'currency_options': currency_options, 'error_message': error_message})


# def home(request):
#     # Fetch currency options from an external API
#     currency_api_url = 'https://api.exchangerate-api.com/v4/latest/USD'  # Example API URL
#     try:
#         response = requests.get(currency_api_url)
#         if response.status_code == 200:
#             data = response.json()
#             currency_options = list(data['rates'].keys())  # Extract currency codes from API response
#         else:
#             currency_options = ['USD', 'EUR', 'GBP']  # Default currency options if API request fails
#     except Exception as e:
#         print(f"Error fetching currency options from API: {e}")
#         currency_options = ['USD', 'EUR', 'GBP']  # Default currency options if API request fails
    
#     return render(request, 'home.html', {'currency_options': currency_options})

# # Rest of your view functions...




def convert_currency(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']

        # Call an external API to get currency exchange rates
        api_key = '6fff097d8ca1d4052c9364f9'  # Replace with your actual API key
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD/{from_currency}'
        response = requests.get(url)

        # Check if response is successful (HTTP status code 200)
        if response.status_code == 200:
            try:
                # Decode response content as JSON
                data = response.json()

                # Access JSON data as a dictionary
                if 'conversion_rates' in data:
                    conversion_rates = data['conversion_rates']
                    if to_currency in conversion_rates:
                        exchange_rate = conversion_rates[to_currency]
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
                        return render(request, 'home.html', {'error_message': error_message})
                else:
                    error_message = "Conversion rates not found in response."
                    return render(request, 'home.html', {'error_message': error_message})
            except ValueError as e:
                error_message = f"Error decoding JSON: {e}"
                return render(request, 'home.html', {'error_message': error_message})
        else:
            error_message = f"Error fetching data from API: HTTP status code {response.status_code}"
            return render(request, 'home.html', {'error_message': error_message})

    else:
        # If request method is not POST, redirect to the home page
        return render(request, 'home.html')





# def convert_currency(request):
#     if request.method == 'POST':
#         amount = float(request.POST['amount'])
#         from_currency = request.POST['from_currency']
#         to_currency = request.POST['to_currency']

#         # Call an external API to get currency exchange rates
#         api_key = ' 6fff097d8ca1d4052c9364f9'  # Replace with your actual API key
#         url = f'https://v6.exchangerate-api.com/v6/6fff097d8ca1d4052c9364f9/latest/USD/{from_currency}'
#         response = requests.get(url)
#         data = response.json()

#         # Print JSON response for debugging
#         print(data)

#         # Calculate the converted amount
#         if to_currency in data['rates']:
#             exchange_rate = data['rates'][to_currency]
#             converted_amount = amount * exchange_rate
#             context = {'amount': amount, 'from_currency': from_currency,
#                        'to_currency': to_currency, 'converted_amount': converted_amount}
#             return render(request, 'result.html', context)
#         else:
#             error_message = f"Currency code '{to_currency}' not found."
#             return render(request, 'currency_converter/home.html', {'error_message': error_message})

#     else:
#         # If request method is not POST, redirect to the home page
#         return render(request, 'shome.html')
