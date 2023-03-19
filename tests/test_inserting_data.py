import pytest
from bson import DBRef
from pymongo import MongoClient
from pymongo.errors import WriteError

from inserting import *


@pytest.mark.parametrize('data', [{'name': 'PC'}, {'name': 'Phone'}])
def test_insert_in_categories(data):
    assert insert_category(db.categories, data)


@pytest.mark.parametrize('expected_exception, data',
                         [(WriteError, {'title': 'Phone'})])
def test_division_with_error(expected_exception, data):
    with pytest.raises(expected_exception):
        assert insert_category(db.categories, data)


@pytest.mark.parametrize('data', [{'name': 'IPhone 13 Pro', 'serial_number': 'DFHHD324F234HDD', 'price': 70000,
                                   'manufacturer': 'Apple', 'amount': 1, 'category': DBRef(collection='products',
                                                                                           id='641712c3af679be2da7f694e'
                                                                                           )}])
def test_insert_in_categories_good(data):
    assert insert_product(db.products, data)


@pytest.mark.parametrize('expected_exception, data', [(WriteError, {'name': 'IPhone 13 Pro',
                                                                    'serial_number': 'DFHHD324F234HDD',
                                                                    'price': 70000, 'manufacturer': 'Apple',
                                                                    'amount': 1})])
def test_insert_in_categories_with_error(expected_exception, data):
    with pytest.raises(expected_exception):
        assert insert_product(db.products, data)


@pytest.mark.parametrize('data', [{'order_amount': 70000, 'status': 'In the basket',
                                   'client': DBRef(collection='clients', id='63f8dbaaee46808712aa5866'), 'products':
                                       [{'serial_number': DBRef(collection='products', id='641712c3af679be2da7f694e'),
                                         'quantity': 1}]
                                   }])
def test_insert_in_orders_good(data):
    assert insert_order(db.orders, data)


@pytest.mark.parametrize('expected_exception, data', [(WriteError, {'order_amount': 70000, 'status': 'In the basket',
                                                                    'client': DBRef(collection='clients',
                                                                                    id='63f8dbaaee46808712aa5866'),
                                                                    'products':
                                                                        [{'serial_number':
                                                                              DBRef(collection='products',
                                                                                    id='641712c3af679be2da7f694e'),
                                                                          }]
                                                                    })])
def test_insert_in_orders_with_error(expected_exception, data):
    with pytest.raises(expected_exception):
        assert insert_order(db.orders, data)


@pytest.mark.parametrize('data', [{'full_name': 'Игорев Игорь Игоревич', 'email': 'iigorev.gmaiul.com',
                                   'post': 'Менеджер'}])
def test_insert_in_employees_good(data):
    assert insert_employee(db.employees, data)


@pytest.mark.parametrize('expected_exception, data', [(WriteError, {'full_name': 'Игорев Игорь Игоревич',
                                                                    'email': 'iigorev.gmaiul.com'})])
def test_insert_in_employees_with_error(expected_exception, data):
    with pytest.raises(expected_exception):
        assert insert_employee(db.employees, data)


@pytest.mark.parametrize('data', [{'name': "Викторов Виктор Викторович",
                                   'phone': "89016786756", 'email': "vvictorov@gmaiul.com", 'organization':
                                       {'title': "CROC", 'inn': "6456575676", 'email': "croc.ru"}}])
def test_insert_in_clients_good(data):
    assert insert_clients(db.clients, data)


@pytest.mark.parametrize('expected_exception, data', [(WriteError, {'name': "Викторов Виктор Викторович",
                                                                    'phone': "89016786756",
                                                                    'email': "vvictorov@gmaiul.com", })])
def test_insert_in_clients_with_error(expected_exception, data):
    with pytest.raises(expected_exception):
        assert insert_clients(db.clients, data)


CONNECTION_STRING = f'mongodb://sshtrih:200330020550@localhost:27017/admin'
client = MongoClient(CONNECTION_STRING)
db = client.hardware_store
