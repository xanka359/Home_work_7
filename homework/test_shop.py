"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1500) is False

    def test_product_buy(self, product):
        product.buy(500)
        assert product.quantity == 500

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart():
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0  # проверяем что корзина изначально пуста
        cart.add_product(product)
        assert len(cart.products) == 1
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 3

    def test_remove_product(self, cart, product):
        cart.add_product(product, buy_count=3)
        assert cart.products[product] == 3  # проверка что в корзине изначально три позиции

        cart.remove_product(product, remove_count=1)
        assert cart.products[product] == 2

        cart.remove_product(product, remove_count=3)
        assert product not in cart.products

        cart.add_product(product)
        cart.remove_product(product, remove_count=1)
        assert product not in cart.products

        cart.add_product(product, buy_count=2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        assert product not in cart.products
        cart.clear()
        assert product not in cart.products

        cart.add_product(product)
        assert product in cart.products
        cart.clear()
        assert product not in cart.products

    def test_total_price(self, cart, product):
        assert product not in cart.products
        assert cart.get_total_price() is None

        cart.add_product(product, buy_count=5)
        ex_total_price = product.price * 5
        assert cart.get_total_price() == ex_total_price

    def test_buy(self, cart, product):
        cart.clear()
        assert product not in cart.products
        cart.buy()
        assert product.quantity == 1000

        cart.add_product(product)
        cart.buy()
        assert product.quantity == 999

        cart.add_product(product, buy_count=1000)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 999
