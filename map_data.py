import json

def get_release_id(number):
    # Normalize the input by ensuring two digits after prefix
    if number.startswith('EX') or number.startswith('BT') or number.startswith('RB') or number.startswith('ST'):
        # Get the prefix (EX or BT)
        prefix = number[:2]
        # Remove prefix, strip any leading zeros, then pad to 2 digits
        num = number[2:].lstrip('0')
        if num:  # Check if there's a number after prefix
            number = f'{prefix}{int(num):02d}'

    if number.startswith('P'):
        number = 'P'
    
    if number.startswith('LM'):
        number = 'LM'
    
    mapping = {
        'BT01': 1, 'BT02': 2, 'BT03': 3, 'BT04': 4, 'BT05': 5,
        'BT06': 6, 'BT07': 7, 'BT08': 8, 'BT09': 9, 'BT10': 10,
        'BT11': 11, 'BT12': 12, 'BT13': 13, 'BT14': 14, 'BT15': 15,
        'BT16': 16, 'BT17': 17, 'BT18': 18, 'BT19': 19, 'BT20': 20,
        'BT21': 21, 'BT22': 22, 'BT23': 23, 'BT24': 24, 'BT25': 25,
        'BT26': 26, 'BT27': 27, 'BT28': 28, 'BT29': 29, 'BT30': 30,
        'EX01': 31, 'EX02': 32, 'EX03': 33, 'EX04': 34, 'EX05': 35,
        'EX06': 36, 'EX07': 37, 'EX08': 38, 'EX09': 39, 'EX10': 40,
        'EX11': 41, 'EX12': 42, 'EX13': 43, 'EX14': 44, 'EX15': 45,
        'EX16': 46, 'EX17': 47, 'EX18': 48, 'EX19': 49, 'EX20': 50,
        'EX21': 51, 'EX22': 52, 'EX23': 53, 'EX24': 54, 'EX25': 55,
        'EX26': 56, 'EX27': 57, 'EX28': 58, 'EX29': 59, 'EX30': 60,
        'ST01': 61, 'ST02': 62, 'ST03': 63, 'ST04': 64, 'ST05': 65,
        'ST06': 66, 'ST07': 67, 'ST08': 68, 'ST09': 69, 'ST10': 70,
        'ST11': 71, 'ST12': 72, 'ST13': 73, 'ST14': 74, 'ST15': 75,
        'ST16': 76, 'ST17': 77, 'ST18': 78, 'ST19': 79, 'ST20': 80,
        'ST21': 81, 'ST22': 82, 'ST23': 83, 'ST24': 84, 'ST25': 85,
        'ST26': 86, 'ST27': 87, 'ST28': 88, 'ST29': 89, 'ST30': 90,
        'RB01': 91,
        'P': 92,
        'LM': 93
    }
    
    return mapping.get(number)

def escape_strings(data):
    if isinstance(data, str):
        return data.replace("'", "''")
    elif isinstance(data, dict):
        return {key: escape_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [escape_strings(item) for item in data]
    else:
        return data

def load_cards_from_json(file_path: str) -> list:
    with open(file_path, 'r') as file:
        cards_data = json.load(file)
    return cards_data

def generate_insert_statements(data: list) -> list:
    insert_statements = []
    for item in data:
        custom_attributes = item.get("customAttributes", {})
        if "color" not in custom_attributes:
            continue
        
        name = escape_strings(item.get("productName", ""))
        description = escape_strings(custom_attributes.get("description", ""))
        market_price = item.get("marketPrice", 0.0)
        rarity = escape_strings(item.get("rarityName", ""))
        if (custom_attributes.get("number", None) is not None):
            release_id = get_release_id(custom_attributes.get("number", "").split('-')[0])
        else:
            continue

        if (release_id is None):
            print(name)
            print(custom_attributes.get("number", ""))

        game_id = 1
        product_id = item.get("productId", "")
        product_id = int(product_id)

        affiliate_url = f"https://tcgplayer.pxf.io/Mm3R72?subId1=card-detail-buy&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F{product_id}%3Fpage%3D1"
        
        # Convert specified values to JSON string without spaces
        attributes = escape_strings({
            "digivolve2Cost": custom_attributes.get("digivolve2Cost"),
            "digivolve2Color": custom_attributes.get("digivolve2Color"),
            "digivolve1Cost": custom_attributes.get("digivolve1Cost"),
            "digivolve1Color": custom_attributes.get("digivolve1Color"),
            "color": custom_attributes.get("color"),
            "level": custom_attributes.get("levelLv"),
            "number": custom_attributes.get("number"),
            "cardType": custom_attributes.get("cardType"),
            "digimonForm": custom_attributes.get("digimonForm"),
            "inheritedEffect": escape_strings(custom_attributes.get("inheritedEffect")),
            "playCost": custom_attributes.get("playCost"),
            "securityEffect": custom_attributes.get("securityEffect"),
            "digimonAttribute": custom_attributes.get("digimonAttribute"),
            "digimonType": custom_attributes.get("digimonType"),
            "tcgPlayerId": product_id,
            "image_url" : f"https://d3pbf736sjoq1j.cloudfront.net/{product_id}.webp"
        })
        attributes_json = json.dumps(attributes, separators=(',', ':'))
        
        # Construct insert statement
        insert_statement = f"INSERT INTO card (name, description, price, rarity, release_id, game_id, affiliate_url, attributes) VALUES ('{name}', '{description}', {market_price}, '{rarity}', {release_id}, {game_id}, '{affiliate_url}', '{attributes_json}');"
        insert_statements.append(insert_statement)
    
    return insert_statements

def save_insert_statements(insert_statements: list, output_file: str):
    with open(output_file, 'w') as file:
        for statement in insert_statements:
            file.write(statement + '\n')

def main():
    # Load cards from JSON file
    cards_data = load_cards_from_json('json/digimon.json')
    print(len(cards_data))
    # Generate insert statements
    insert_statements = generate_insert_statements(cards_data)

    # Save insert statements to file
    save_insert_statements(insert_statements, 'all_cards.sql')

if __name__ == '__main__':
    main()
