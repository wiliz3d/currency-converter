from django.shortcuts import render

# Create your views here.
# currency_converter/views.py

from django.shortcuts import render
import requests

def home(request):
    return render(request, 'currency_converter/home.html')

def convert_currency(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']

        # Call an external API to get currency exchange rates
        api_key = ' 6fff097d8ca1d4052c9364f9'  # Replace with your actual API key
        url = f'https://v6.exchangerate-api.com/v6/6fff097d8ca1d4052c9364f9/latest/USD/{from_currency}'
        response = requests.get(url)
        data = response.json()

        # Calculate the converted amount
        if to_currency in data['rates']:
            exchange_rate = data['rates'][to_currency]
            converted_amount = amount * exchange_rate
            context = {'amount': amount, 'from_currency': from_currency,
                       'to_currency': to_currency, 'converted_amount': converted_amount}
            return render(request, 'currency_converter/result.html', context)
        else:
            error_message = f"Currency code '{to_currency}' not found."
            return render(request, 'currency_converter/home.html', {'error_message': error_message})

    else:
        # If request method is not POST, redirect to the home page
        return render(request, 'currency_converter/home.html')
