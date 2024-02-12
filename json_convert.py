import json
import os

# Load JSON data from file

current_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_directory, 'json/digimon.json'), 'r') as file:
    data = json.load(file)

# Remove records without customAttributes.cardType
data = [item for item in data if 'cardType' in item.get('customAttributes', {})]

# Flatten customAttributes onto the root object
for item in data:
    item.update(item.pop('customAttributes', {}))

# Remove listings property and properties related to shipping
for item in data:
    item.pop('listings', None)  # Remove listings property
    item.pop('shippingCategoryId', None)
    item.pop('lowestPriceWithShipping', None)
    item.pop('sellerListable', None)
    item.pop('maxFulfillableQuantity', None)
    item.pop('totalListings', None)

print(len(data))		

# Save the modified data to a new JSON file
with open('digimon_updated.json', 'w') as file:
    json.dump(data, file)
