import requests
import pandas as pd

api_key = '6fff097d8ca1d4052c9364f9'  # Replace with your actual API key
url = f'https://v6.exchangerate-api.com/v6/6fff097d8ca1d4052c9364f9/latest/USD/'  # Replace USD with the base currency you want
response = requests.get(url)
data = response.json()

print(data)

df = pd.DataFrame(data)
df.to_csv('elon_data.csv')