import json
def run():
    count = 0
    for doc in range(1, 40):
        filename = f"etl_data_{doc}.json"
        with open(filename, 'r') as file:
            data = json.load(file)
            num_products = len(data.get("products"))
            print(f"Doc {doc} has {num_products} products")
            count += len(data.get("products"))
        
    print(count)
    
run()