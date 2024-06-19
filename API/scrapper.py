from outscraper import ApiClient
import json
import webbrowser
import pandas as pd
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

api_client = ApiClient(api_key=os.getenv('SCRAPPER_KEY'))
file_path = 'dataIpStream.json'

def scrape(location, lim):
    results = api_client.google_maps_search(location, limit=lim)
    with open('dataIpStream.json', 'w') as file:
        json.dump(results, file, indent=4)

def clean():
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    extracted_data = []
    for entry in data:
        for item in entry:
            extracted_item = {
                "lead_name": item.get("name"),
                "lead_contacts": item.get("phone"),
                "website": item.get("site"),
                "price_range": item.get("range"),
                "location": item.get("full_address"),
                "reviews": item.get("reviews_per_score"),
                "link": item.get("location_link"),
                "photo_count": item.get("photos_count"),
            }
            extracted_data.append(extracted_item)
    return extracted_data

def open_link(lead_name_search):
    extracted_data = clean()

    for i in extracted_data:
        if i['lead_name'] == lead_name_search:
            link = i['link']
            break

    if not link:
        return None

    webbrowser.open(link)

def get_reviews(lead_name_search):
  extracted_data = clean()

  for i in extracted_data:
    if i['lead_name'] == lead_name_search:
      data = i['reviews']
    #   print(i['reviews'])
      break

  if not data:  
    return None  

  return get_min_max(data)


def get_min_max(data):
    # print(data) 
    max_key = max(data, key=lambda k: data[k])
    max_value = data[max_key]
    
    min_key = min(data, key=lambda k: data[k])
    min_value = data[min_key]
    return max_key, max_value, min_key, min_value
    

def export_excel():
   output_dir = "outputData"
   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
    
   timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
   filename = f"{output_dir}/dataOutStream_{timestamp}.xlsx"

   data = clean()
   df = pd.DataFrame(data)
   df.to_excel(filename, index=False)
   os.startfile(f"C:/Users/Adithyakarthik/OneDrive/Documents/work/Lead-Gen-Tool/outputData/dataOutStream_{timestamp}.xlsx")

