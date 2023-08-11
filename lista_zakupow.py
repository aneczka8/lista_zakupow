import csv
import collections

store_shopping_dict = {'Ogólny':[], 'Apteka':[], 'Drogeria':[], 'Budowlany':[]}
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
        print("Lista jest pusta.")

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
        print("1. Podaj nazwę sklepu, aby wyświetlić listę zakupów.")
        print("2. Dodaj sklep do listy.")
        print("3. Usuń sklep z listy.")
        print("4. Zmień nazwę sklepu.")
        print("5. Wróć do głównego menu.")
        print()

        user_choice = input().capitalize()

        if user_choice == '2':
            add_store(input("Podaj nazwę sklepu, który chcesz dodać: ").capitalize())

        elif user_choice == '3':
            delete_store(input("Podaj nazwę sklepu, który chcesz usunąć: ").capitalize())

        elif user_choice == '4':
            old_store_name = input("Podaj aktualną nazwę sklepu: ").capitalize()
            new_store_name = input("Podaj nową nazwę dla tego sklepu: ").capitalize()

            if old_store_name in store_shopping_dict:
                store_shopping_dict[new_store_name] = store_shopping_dict[old_store_name]
                for number, store in enumerate(store_shopping_dict):
                    if old_store_name == store:
                        if number == 0:
                            store_shopping_dict.move_to_end(new_store_name, last=False)
                    delete_store(old_store_name)
                    break
            else:
                print("Nie ma takiego sklepu. Spróbuj jeszcze raz.")

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
                    print("Lista jest pusta.")   
            except KeyError:
                print("Podaj nazwę sklepu lub liczbę od 2 do 4.") 

def add_product():
    global store_shopping_dict

    product = input("Podaj co chcesz dodać do listy: ")

    for store in store_shopping_dict:
        default_store = store
        break

    shopping_list = create_shopping_list()
    if product in shopping_list:
        choice = input("Ten produkt jest już na liście. Czy mimo to chcesz go dodać? [tak/nie] ")
        if choice == 'nie':
            return
        elif choice != 'nie' and choice != 'tak':
            print("Nie wybrałeś(aś) czy chcesz dodać produkt. Spróbuj jeszcze raz.")
            return

    decision = input(f"Czy chcesz wpisać to do konkretnego sklepu (domyślnie użyję sklepu {default_store})? [tak/nie]: ")
    if decision == "tak":
        show_store()
        print()
        store = input("Wybierz sklep: ").capitalize()
        try:
            store_shopping_dict[store].append(product)
        except KeyError:
            print("Nie ma takiego sklepu. Spróbuj jeszcze raz.")
    elif decision == 'nie':
        for index, store in enumerate(store_shopping_dict):
            if index == 0:
                store_shopping_dict[store].append(product)
                break
    else:
        print()
        print("Nie udało się dodać produktu. Spróbuj jeszcze raz.")

def delete_product():
    global store_shopping_dict

    shopping_list = create_shopping_list()
    show_shopping_list()
    try:
        product_number = int(input("Podaj numer produktu, który chcesz usunąć: "))
    except:
        print("Musisz podać liczbę naturalną. Spróbuj jeszcze raz.")
        return

    for store in store_shopping_dict.keys():
        if product_number > len(store_shopping_dict[store]):
            product_number -= len(store_shopping_dict[store])
        elif product_number <= len(store_shopping_dict[store]) and product_number > 0:
            store_shopping_dict[store].pop(product_number-1)
            return
    
    print("Musisz podać liczbę od 1 do " + str(len(shopping_list)) + ".")
    

def add_store(store):
    global store_shopping_dict
    store_shopping_dict[store] = []

def delete_store(store):
    global store_shopping_dict

    if len(store_shopping_dict) == 1:
        print("Został tylko jeden sklep. Nie możesz go usunąć.")
        return
    try:
        store_shopping_dict.pop(store)
    except KeyError:
        print("Nie udało się usunąć sklepu z listy. Spróbuj jeszcze raz.")

def read_file():
    global store_shopping_dict
    
    file_name = input("""Podaj nazwę pliku lub napisz "nie" jeśli chcesz użyć nazwy domyślnej. """)
    if file_name == 'nie':
        file_name = 'lista_zakupów'
    try:
        with open(f"{file_name}.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                store, products = row
                store_shopping_dict[store] = products.split(', ')
    except FileNotFoundError:
        print("Nie ma takiego pliku.")

def save_file():
    global store_shopping_dict

    file_name = input("""Podaj nazwę pliku lub napisz "nie" jeśli chcesz użyć nazwy domyślnej. """)
    if file_name == 'nie':
        file_name = 'lista_zakupów'
    with open(f"{file_name}.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        for store, products in store_shopping_dict.items():
            writer.writerow([store,products])

while True:
    print()
    print("Co chcesz zrobić? (Wybierz numer)")
    print("1. Wyświetl całą listę zakupów.")
    print("2. Dodaj produkt do listy zakupów.")
    print("3. Usuń produkt z listy zakupów.")
    print("4. Przejdź do poszczególnych sklepów.")
    print("5. Zapisz listę do pliku.")
    print("6. Wczytaj listę z pliku.")
    print("7. Wyjdź.")
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