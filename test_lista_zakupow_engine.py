import unittest
import os
from lista_zakupow_engine import *

class UnitTests(unittest.TestCase):
    def test_create_shopping_list(self):        
        self.assertIsInstance(create_shopping_list(), list)

    def test_show_stores(self):
        stores = list(show_stores())
        self.assertIsInstance(stores, list)

    def test_create_store_list_existing_store(self):
        store = 'ogólny'
        expected_products = []
        self.assertEqual(create_store_list(store), expected_products)

    def test_create_store_list_not_existing_store(self):
        store = 'general'
        expected_products = []
        self.assertEqual(create_store_list(store), expected_products)

    def test_create_store_list_int_store(self):
        store = 25
        expected_products = []
        self.assertEqual(create_store_list(store), expected_products)

    def test_add_product_existing_shop(self):
        product = 'jabłka'
        index = 0
        add_product(product, index)
        shopping_list = create_shopping_list()
        self.assertIn(product, shopping_list)

    def test_add_product_not_existing_shop(self):
        product = 'jajka'
        index = 6
        add_product(product, index)
        shopping_list = create_shopping_list()
        self.assertNotIn(product, shopping_list) 

    def test_add_product_string_shop(self):
        product = 'mleko'
        index = "sklep"
        add_product(product, index)
        shopping_list = create_shopping_list()
        self.assertNotIn(product, shopping_list)    

    def test_delete_product_existing(self):
        product = "jabłka"
        delete_product(product)
        shopping_list = create_shopping_list()
        self.assertNotIn(product, shopping_list)

    def test_delete_product_not_existing(self):
        product = "mandarynki"
        delete_product(product)
        shopping_list = create_shopping_list()
        self.assertNotIn(product, shopping_list)

    def test_add_store(self):
        store = "Sportowy"
        add_store(store)
        stores = show_stores()
        self.assertIn(store, stores)

    def test_delete_store_existing(self):
        store = "Apteka"
        delete_store(store)
        stores = show_stores()
        self.assertNotIn(store, stores)

    def test_delete_store_not_existing(self):
        store = "pharmacy"
        delete_store(store)
        stores = show_stores()
        self.assertNotIn(store, stores)

    def test_save_file(self):
        file_name = 'test_file'
        save_file(file_name)
        self.assertTrue(os.path.exists(f"{file_name}.csv"))

    def test_read_file(self):
        file_name = 'test_file'
        expected_data = {'Ogólny': ['Jabłka', 'Chleb'], 'Drogeria': [], 'Budowlany': [], "Sportowy": []}
        read_file(file_name)
        stores = show_stores()
        shopping_list = create_store_list("Ogólny")
        self.assertEqual(stores, expected_data.keys())
        self.assertEqual(shopping_list, expected_data['Ogólny'])

if __name__ == '__main__':
    unittest.main()