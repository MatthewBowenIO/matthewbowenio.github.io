import requests
import json
import time
import os

from PIL import Image
from io import BytesIO

# URL of the image
def download_image(product_id):
    folder_name = 'images'
    folder_path = os.path.join(os.path.dirname(__file__), folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "{}.jpg".format(product_id))
    if os.path.exists(file_path):
        print ("Image {} already exists. Skipping.".format(file_path))
        return

    image_url = 'https://product-images.tcgplayer.com/fit-in/750x750/{}.jpg'.format(product_id)

    # HTTP request to fetch the image
    response = requests.get(image_url, headers={
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'Referer': 'https://www.tcgplayer.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'sec-ch-ua-platform': '"Windows"',
    })

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(file_path)
        print("Image {} successfully downloaded.".format(product_id))
    else:
        print(f"Error fetching image. Status code: {response.status_code}")


url = 'https://mp-search-api.tcgplayer.com/v1/search/request?q=&isList=false&mpfev=2118'
        
headers = {
    'authority': 'mp-search-api.tcgplayer.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.tcgplayer.com',
    'referer': 'https://www.tcgplayer.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}

data = {
    "algorithm": "revenue_exp_fields_experiment",
    "from": 0,
    "size": 50,
    "filters": {
        "term": {"productLineName": ["digimon-card-game"],            "setName": [
                "exceed-apocalypse"
            ]},
        "range": {},
        "match": {}
    },
    "listingSearch": {
        "context": {"cart": {}},
        "filters": {
            "term": {"sellerStatus": "Live", "channelId": 0},
            "range": {"quantity": {"gte": 1}},
            "exclude": {"channelExclusion": 0}
        }
    },
    "context": {"cart": {}, "shippingCountry": "US", "userProfile": {"productLineAffinity": None}},
    "settings": {"useFuzzySearch": True, "didYouMean": {}},
    "sort": {}
}

no_results = False

digimon = []
while not no_results:
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()

        if len(result['results'][0]['results']) == 0:
            no_results = True
            print("No results remaining")
        else:
            print("Processing batch from: {}".format(data['from']))
            # Process the results as needed
            folder_name = 'json'
            folder_path = os.path.join(os.path.dirname(__file__), folder_name)
            os.makedirs(folder_path, exist_ok=True)
 
            for key, value in result["results"][0]["aggregations"].items():
                    file_path = os.path.join(folder_path, "{}.json".format(key))
                    if not os.path.exists(file_path):
                        with open(file_path , 'w') as file:
                            json.dump(value, file, indent=2)
            
            for product in result["results"][0]["results"]:
                download_image(int(product["productId"]))

            digimon.extend(result["results"][0]["results"])
            file_path = os.path.join(folder_path, "digimon.json")
            with open(file_path, 'w') as file:
                json.dump(digimon, file, indent=2)

            # Update the "from" value for the next iteration
            data["from"] += 50
    else:
        print(f"Error: {response.status_code}")
        break
    
    # Introduce a delay of 1 second
    time.sleep(1)

print("Done")
