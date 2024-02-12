import json

def get_release_id(number):
    print(number)
    mapping = {
        'BT01': 1,
        'BT02': 2,
        'BT03': 3,
        'BT04': 4,
        'BT05': 5,
        'BT06': 6,
        'BT07': 7,
        'BT08': 8,
        'BT09': 9,
        'BT10': 10,
        'BT11': 11,
        'BT12': 12,
        'BT13': 13,
        'BT14': 14,
        'BT15': 15,
        'BT16': 16,
        'BT17': 17,
        'EX01': 18,
        'EX02': 19,
        'EX03': 20,
        'EX04': 21,
        'EX05': 22,
        'EX06': 23,
        'RB01': 24
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
        release_id = get_release_id(custom_attributes.get("number", "").split('-')[0])
        print(release_id);
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
            "tcgPlayerId": product_id
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

    # Generate insert statements
    insert_statements = generate_insert_statements(cards_data)

    # Save insert statements to file
    save_insert_statements(insert_statements, 'insert_statements_bt15.sql')

if __name__ == '__main__':
    main()
