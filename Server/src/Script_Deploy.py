from bs4 import BeautifulSoup
from requests import get
import re

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})


#Input the listing you want from realtor.ca 

realtorURL = "https://www.realtor.ca/real-estate/22912752/n215-1105-pandora-ave-victoria-downtown"
response = get(realtorURL, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
price = re.findall('price: \'(\d+\.\d+)\'', response.text)
price = float(price[0])
beds = re.findall('bedrooms: \'(\d+)\'', response.text)
beds = beds[0]
baths = re.findall('bathrooms: \'(\d+)\'', response.text)
baths = baths[0]
postal_code = soup.find("h1", id="listingAddress")
postal_code = postal_code.text[-6:]


radius='5'


import requests
# https://requests.readthedocs.io/en/master/


# Get list of offers
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

# load the model from disk
import pickle
import numpy as np
filename = 'mvp_model.sav'

loaded_model = pickle.load(open(filename, 'rb'))
 
occupancy_rate = 0.6
days_rented = 365*occupancy_rate
result = loaded_model.predict(np.array([beds,baths]).reshape(1, -1))
print("The average monthly AirBnB value for this listing is in the ballpark of: ", result[0]*days_rented/12)