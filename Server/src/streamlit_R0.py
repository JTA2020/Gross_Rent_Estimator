import streamlit as st
import pickle
import numpy as np
from bs4 import BeautifulSoup
import requests
from requests import get
import re


header = st.beta_container() 
with header:
    st.title('Victoria, BC Rental Rate Predictor')

path = st.text_input('ENTER LISTING URL HERE')



headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "dnt": "1",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
    }

response = get(path, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser') 
price = re.findall('priceForHDP..:(\d+)', response.text)
price = int(price[0])
beds = re.findall('Bedrooms: <!--.*?-->(\d+)', response.text)
beds = int(beds[0])
baths = re.findall('Bathrooms: <!--.*?-->(\d+)', response.text)
baths = int(baths[0])
postal_code = re.findall('zipcode..:..(V\d[A-Z]\d[A-Z]\d)', response.text)
postal_code = postal_code[0]
lon = re.findall('longitude..:(.\d+.\d+)', response.text)
#float(lon[0])
lat = re.findall('latitude..:(\d+.\d+)', response.text)
#float(lat[0])
sq_ft = re.findall('livingArea..:(\d+)', response.text)
sq_ft = int(sq_ft[0] )

#############################################

st.markdown('## Listing:') 
st.text(price)
st.text(soup.find('title').text )
st.markdown('#### Number of Bedrooms:')
st.text(beds)
st.markdown('#### Number of Bathrooms:')
st.text(baths)

#############################################

airbnb_model = pickle.load(open('mvp_model.sav', 'rb'))
occupancy_rate = 0.6
days_rented = 365*occupancy_rate
result = airbnb_model.predict(np.array([beds,baths]).reshape(1, -1))
st.markdown('### AI-Predicted Monthly AirBnB Rental Value')
st.text(int(result[0]*(days_rented/12)))

#############################################

guests = int(beds*2+.5)
st.markdown('### AirBnB.ca suggested potential')
def airbnb_price(guests):
    victoria_entire_place_prices = [6416, 1711, 1924, 2207, 2684, 3067, 3898, 4782, 5132, 5643, 6248, 6942, 7133, 7445, 9405, 9458]
    if guests<16:
        price_potential = victoria_entire_place_prices[round(guests)]
    else:
        price_potential = "Function unavailble for more than 15 guests"
    return price_potential  
st.text(airbnb_price(guests))












##############################################################################

loaded_model = pickle.load(open('mvp_model_craigslist.sav', 'rb'))
result_2 = loaded_model.predict(np.array([beds,baths,sq_ft]).reshape(1, -1))
st.markdown('### Conventional Rent Estimate (Based on Craigslist)')
st.text(int(result_2[0])) 






#############################################




radius='25'
URL = f'https://victoria.craigslist.org/search/apa?search_distance={radius}&postal={postal_code}&min_price=600&max_price=60000&min_bedrooms={beds}&max_bedrooms={beds}&min_bathrooms={baths}&max_bathrooms={baths}&availabilityMode=0&sale_date=all+dates'
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
        print(price_elem.text.strip())
        print(url_elem)    
        print(title_elem.text.strip())
        print()
        
    except:
        pass

print("The average monthly rental for this listing is in the ballpark of: ", int(sum(prices) / len(prices))) 

st.markdown('### Craigslist Current Rates for similar listings')
st.text(int(sum(prices) / len(prices))) 




