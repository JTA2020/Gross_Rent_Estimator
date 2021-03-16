import streamlit as st
import pickle
import numpy as np
from bs4 import BeautifulSoup
from requests import get
import re



header = st.beta_container() 

beds = st.slider('beds',0,8)  # 👈 this is a widget
baths = st.slider('baths',0,8)  # 👈 this is a widget
sq_ft = st.slider('square footage', 400, 2500)
occupancy_rate = st.slider('occupancy rate (% nights rented in a month)', 0.4, 0.9)
guests = st.slider('max number of guests', 1, 15)

with header:
    st.title('Victoria, BC Rental Rate Predictor')



loaded_model = pickle.load(open('mvp_model_craigslist.sav', 'rb'))
result = loaded_model.predict(np.array([beds,baths,sq_ft]).reshape(1, -1))

st.markdown('### Conventional Rent Estimate (Based on Craigslist)')
st.text(int(result[0])) 

radius='25'
import requests
# https://requests.readthedocs.io/en/master/


# Get list of offers
URL = f'https://victoria.craigslist.org/search/apa?search_distance={radius}&postal=v8z5z4&min_price=600&max_price=60000&min_bedrooms={beds}&max_bedrooms={beds}&min_bathrooms={baths}&max_bathrooms={baths}&availabilityMode=0&sale_date=all+dates'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_='rows')
elems = results.find_all('li', class_='result-row')

import string

def remove_punct(text):
    text = "".join([char for char in text if char not in string.punctuation])
    return text 

#Bank of the prices
prices = []

# Parse each offer tile
for elem in elems:
    try: 
        price_elem = elem.find('span', class_='result-price')
        prices.append(int(remove_punct(price_elem.text.strip())))
        url_elem = elem.find('a', class_="result-image gallery")['href']
        title_elem = elem.find('a', class_='result-title hdrlnk')
        #print(price_elem.text.strip())
        #print(url_elem)    
        #print(title_elem.text.strip())
        #print()
        
    except:
        pass

st.markdown('### Current average (Based on Craigslist)')
st.text(int(sum(prices) / len(prices)))




loaded_model2 = pickle.load(open('mvp_model.sav', 'rb'))
 
days_rented = 365*occupancy_rate
result2 = loaded_model2.predict(np.array([beds,baths]).reshape(1, -1))
st.markdown('### Average monthly AirBnB value')
st.text(int(result[0]*days_rented/12))

st.markdown('### AirBnB.ca suggested potential')
def airbnb_price(guests):
    victoria_entire_place_prices = [6416, 1711, 1924, 2207, 2684, 3067, 3898, 4782, 5132, 5643, 6248, 6942, 7133, 7445, 9405, 9458]
    if guests<16:
        price_potential = victoria_entire_place_prices[guests]
    else:
        price_potential = "Function unavailble for more than 15 guests"
    return price_potential  
st.text(airbnb_price(guests))


