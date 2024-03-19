import requests
import json
import time

base_url = "https://api.etl.energysecurity.gov.uk"
api_key = "PRIVATE_API_KEY"

# Write a function that makes a query to the ETL API and returns the data and stores it in a json file
def get_data(page):
    query = f"/api/v1/products?listingStatus=current&page={page}&size=200"
    url = base_url + query
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    filename = f"etl_data_{page}.json"
    with open(filename, 'w') as file:
        json.dump(data, file)
        
def get_all_data():
    for page in range(1, 41):
        # Wait for 1 second to complete the request
        time.sleep(1)
        print(f"Getting data for page {page}")
        get_data(page)
        
get_all_data()       