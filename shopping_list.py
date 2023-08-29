import csv
import collections

store_shopping_dict = {'General':[], 'Pharmacy':[], 'Drugstore':[], 'Construction shop':[]}
store_shopping_dict = collections.OrderedDict(store_shopping_dict)

def show_shopping_list():
    global store_shopping_dict

    shopping_list = create_shopping_list()
    print()

    index = 1
    for product in shopping_list:
        product = product.replace('[','').replace(']','').replace("'","")
        if product:
            print(str(index) + ". " + product)
            index += 1

    if len(shopping_list) == 0 or index == 1:
        print("The list is empty.")

def create_shopping_list():
    global store_shopping_dict

    shopping_list = []

    for products in store_shopping_dict.values():
        shopping_list = shopping_list + products

    return shopping_list

def show_store():
    global store_shopping_dict

    print()
    for store in store_shopping_dict.keys():
        print(store)

def show_store_menu():
    global store_shopping_dict

    while True:
        print()
        for store in store_shopping_dict.keys():
            print(store)
        print()
        print("1. Please enter a store name to view your shopping list.")
        print("2. Add store to the list.")
        print("3. Remove store from the list.")
        print("4. Rename the store.")
        print("5. Go back to the main menu.")
        print()

        user_choice = input().capitalize()

        if user_choice == '2':
            add_store(input("Enter a store name you what to add: ").capitalize())

        elif user_choice == '3':
            delete_store(input("Enter a store name you what to remove: ").capitalize())

        elif user_choice == '4':
            old_store_name = input("Enter the current store name: ").capitalize()
            new_store_name = input("Enter a new name for this store: ").capitalize()

            if old_store_name in store_shopping_dict:
                store_shopping_dict[new_store_name] = store_shopping_dict[old_store_name]
                for number, store in enumerate(store_shopping_dict):
                    if old_store_name == store:
                        if number == 0:
                            store_shopping_dict.move_to_end(new_store_name, last=False)
                    delete_store(old_store_name)
                    break
            else:
                print("There is no such store. Try again.")

        elif user_choice == '5':
            break

        else:
            index = 1
            print()
            try:
                for product in store_shopping_dict[user_choice.capitalize()]:
                    print(str(index) + ". " + product)
                    index += 1
                if len(store_shopping_dict[user_choice]) == 0:
                    print("The list is empty.")   
            except KeyError:
                print("Enter a store name or number between 2 and 4.") 

def add_product():
    global store_shopping_dict

    product = input("Enter what you want to add to the list: ")

    for store in store_shopping_dict:
        default_store = store
        break

    shopping_list = create_shopping_list()
    if product in shopping_list:
        choice = input("This product is already on the list. Do you want to add it anyway? [yes/no] ")
        if choice == 'no':
            return
        elif choice != 'no' and choice != 'yes':
            print("You have not chosen whether you want to add produkt. Try again.")
            return

    decision = input(f"Do you want to type this into a specific store (I will use {default_store} by default)? [yes/no]: ")
    if decision == "yes":
        show_store()
        print()
        store = input("WChoose store: ").capitalize()
        try:
            store_shopping_dict[store].append(product)
        except KeyError:
            print("There is no such store. Try again.")
    elif decision == 'no':
        for index, store in enumerate(store_shopping_dict):
            if index == 0:
                store_shopping_dict[store].append(product)
                break
    else:
        print()
        print("Failed to add product. Try again.")

def delete_product():
    global store_shopping_dict

    shopping_list = create_shopping_list()
    show_shopping_list()
    try:
        product_number = int(input("Enter the product number that you want to delete: "))
    except:
        print("You have to enter a natural number. Try again.")
        return

    for store in store_shopping_dict.keys():
        if product_number > len(store_shopping_dict[store]):
            product_number -= len(store_shopping_dict[store])
        elif product_number <= len(store_shopping_dict[store]) and product_number > 0:
            store_shopping_dict[store].pop(product_number-1)
            return
    
    print("You have to enter a number between 1 and " + str(len(shopping_list)) + ".")
    

def add_store(store):
    global store_shopping_dict
    store_shopping_dict[store] = []

def delete_store(store):
    global store_shopping_dict

    if len(store_shopping_dict) == 1:
        print("There is only one store left. You can not remove it.")
        return
    try:
        store_shopping_dict.pop(store)
    except KeyError:
        print("Failed to remove store from the list. Try again.")

def read_file():
    global store_shopping_dict
    
    file_name = input("""Enter a file name or write "no" if you want to use the default name. """)
    if file_name == 'no':
        file_name = 'shopping_list'
    try:
        with open(f"{file_name}.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                store, products = row
                store_shopping_dict[store] = products.split(', ')
    except FileNotFoundError:
        print("There is no such file.")

def save_file():
    global store_shopping_dict

    file_name = input("""Enter a file name or write "no" if you want to use the default name. """)
    if file_name == 'no':
        file_name = 'shopping_list'
    with open(f"{file_name}.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        for store, products in store_shopping_dict.items():
            writer.writerow([store,products])

while True:
    print()
    print("What do you want to do? (Choose a number)")
    print("1. View the entire shopping list.")
    print("2. Add product to the shopping list.")
    print("3. Delete product from the shopping list.")
    print("4. Go to the store menu.")
    print("5. Save the shopping list to a file.")
    print("6. Read the shopping list from a file.")
    print("7. Exit.")
    print()

    user_choice = input()

    if user_choice == '1':
        show_shopping_list()

    if user_choice == '2':
        add_product()

    if user_choice == '3':
        delete_product()

    if user_choice == '4':
        show_store_menu()

    if user_choice == '5':
        save_file()

    if user_choice == '6':
        read_file()

    if user_choice == '7':
        break