import json

def extract_products():
    # Read the data from the file
    with open('../../full_energy_technology_list.json', 'r') as file:
        data = json.load(file)
    return data.get("products")

def process_product(product):
    id = product.get("id")
    text = ""
    product_vals = ["name", "modelNumber"]
    manufacturer_vals = ["name", "telNumber", "website", "address", "postcode", "country", "emailAddress"]
    feature_vals = ["name", "value", "unit"]
    
    for val in product_vals:
        if product.get(val):
            text += product.get(val, "") + " "
        
    for val in manufacturer_vals:
        if product.get("manufacturer", {}).get(val):
            text += val + ": " +product.get("manufacturer", {}).get(val, "") + " "
        
    features = product.get("features", [])  
    for feature in features:
        for val in feature_vals:
            if feature.get(val):
                text += val + ": " + feature.get(val, "") + " "
          
    classification = product.get("uniclassCodes", [])
    for code in classification:
        text += "Classification: " + code.get("classification", "") + " "
    
    images = product.get("images", [])
    for image in images:
        text += "Images: " + image.get("url", "") + " "
    
    
    return {
        "id": str(id),
        "text": text,
    }