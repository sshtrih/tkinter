from pymongo import MongoClient
from bson.dbref import DBRef


class User:
    def __init__(self, username, password, database='hardware_store'):
        self.user_id = None
        print(username, password, database)
        self.username = username
        CONNECTION_STRING = f'mongodb://{username}:{password}@localhost:27017/{database}'
        client = MongoClient(CONNECTION_STRING)
        self.db = client.hardware_store
        self.specifications = ['name, prise, manufacturer, category']
        self.products = None

    def get_top_sales(self):
        return self.db.top_sales.find()[0]['_id']

    def get_top_categories(self):
        return self.db.top_categories.find()[0]['name']

    def get_products(self):
        return self.db.products_with_category.find()

    def find_product(self, start_prise, end_prise, category, key_word, manuf):
        if start_prise is None:
            start_prise = 0
        if end_prise is None:
            end_prise = 1000000
        return self.db.products_with_category.aggregate([{'$match': {'name': {'$regex': f'.*{key_word}.*',
                                                                              '$options': 'ixs'}}},
                                                         {'$match': {'price': {
                                                             '$gte': start_prise,
                                                             '$lte': end_prise}}},
                                                         {'$match': {'manufacturer': {'$regex': f'.*{manuf}.*',
                                                                                      '$options': 'ixs'}}},
                                                         {'$match': {'category': {'$regex': f'.*{category}.*'}}}

                                                         ])

    def get_categories(self):
        return self.db.categories.find()

    def add_product_to_basket(self, product, quantity=1):

        product_id = self.db.products.find_one({'name': f'{product[0]}'}).get('_id')
        print(product_id)
        self.user_id = self.db.clients.find_one({'email': f'{self.username}@gmaiul.com'}).get('_id')
        basket = self.db.orders.find_one({'status': 'In the basket',
                                          'client': DBRef(collection='clients',
                                                          id=self.user_id)})
        if basket is None:
            self.db.orders.insert_one({'status': 'In the basket', 'client': DBRef(collection='clients',
                                                                                  id=self.user_id),
                                       'products': [{'serial_number': DBRef(collection='products',
                                                                            id=product_id), 'quantity': quantity}],
                                       'order_amount': product[1]})
        else:
            self.db.orders.update_one({'_id': basket.get('_id')}, {'$push': {'products': {'serial_number': DBRef(
                collection='products',
                id=product_id),
                'quantity': quantity}},
                '$inc': {'order_amount': product[1]}})
