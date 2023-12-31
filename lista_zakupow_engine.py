import csv
import collections

store_shopping_dict = {'Ogólny':[], 'Apteka':[], 'Drogeria':[], 'Budowlany':[]}
store_shopping_dict = collections.OrderedDict(store_shopping_dict)

def create_shopping_list():
    global store_shopping_dict

    shopping_list = []

    for products in store_shopping_dict.values():
        shopping_list = shopping_list + products

    return shopping_list

def show_stores():
    global store_shopping_dict

    return store_shopping_dict.keys()

def create_store_list(store):
    global store_shopping_dict
    if store in store_shopping_dict:
        return store_shopping_dict[store]
    else:
        return []

def add_product(product, index):
    for number, store in enumerate(store_shopping_dict):
        if number == index:
            store_shopping_dict[store].append(product)

def delete_product(product):
    global store_shopping_dict

    shopping_list = create_shopping_list()
    try:
        shopping_list.remove(product)
    except ValueError:
        return f"Nie ma: {product} na liście"
    for store_list in store_shopping_dict.values():
        if product in store_list:
            store_list.remove(product)

def add_store(store):
    global store_shopping_dict
    store_shopping_dict[store] = []

def delete_store(store):
    global store_shopping_dict
    try:
        store_shopping_dict.pop(store)
    except KeyError:
        return f"Nie ma sklepu: {store}"

def read_file(file_name):
    global store_shopping_dict
    no_file = 'Nie ma takiego pliku'
    wrong_file = 'Plik ma niewłaściwy format'
    store_shopping_dict.clear()

    try:
        with open(f"{file_name}.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                store = row[0]
                products = row[1:]
                store_shopping_dict[store] = products
    except FileNotFoundError:
        return no_file
    except ValueError:
        return wrong_file

def save_file(file_name):
    global store_shopping_dict

    with open(f"{file_name}.csv","w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for store, products in store_shopping_dict.items():
            writer.writerow([store]+products)
