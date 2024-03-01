class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int


    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        return self.quantity >= quantity

    def buy(self, quantity):
        if self.check_quantity(quantity):  # проверяем что продукта достаточно
            self.quantity -= quantity  # уменьшаем его на количестко quantity
        else:
            raise ValueError('Недостаточно товаров в корзине')

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Инициализация корзины.
    Продукты хранятся в словаре, где ключами являются объекты типа Product,
    а значениями - количество каждого продукта в корзине.
    """
    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if remove_count is None or self.products[product] <= remove_count:
                del self.products[product]
            else:
                self.products[product] -= remove_count


    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total_price = 0
        for product, quantity in self.products.items(): #где product - ключ словаря,
                                                        # а quantity - значение, т.е. количество единиц
            total_price += product.price * quantity
            return total_price

    def buy(self):
        for product, quantity in self.products.items():
            if product.quantity < quantity:
                raise ValueError('Недостаточно продукта')
            else:
                product.buy(quantity)
        """
            Метод покупки.
           Учтите, что товаров может не хватать на складе.
           В этом случае нужно выбросить исключение ValueError
        """