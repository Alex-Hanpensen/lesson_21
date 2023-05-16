from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, capacity):
        self.__items = {}
        self.__capacity = capacity

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        self.__items = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @abstractmethod
    def add(self, name, quantity) -> None:
        """
        increases the stock of items
        Returns: None
        """
        pass

    @abstractmethod
    def remove(self, name, quantity) -> None:
        """
        reduces the stock of items
        Returns: None
        """
        pass

    @abstractmethod
    def get_free_space(self) -> None:
        """
        return the number of available seats
        Returns: None
        """
        pass

    @abstractmethod
    def get_items(self) -> None:
        """
        returns the contents of the warehouse in the dictionary {product: quantity}
        Returns:
        """

    @abstractmethod
    def get_unique_items_count(self) -> None:
        """
        returns the number of unique products
        Returns:
        """


class Store(Storage):
    def __init__(self, capacity=100):
        super().__init__(capacity)

    def add(self, name, quantity):
        if self.capacity > quantity + sum(self.items.values()):
            if name in self.items:
                self.items[name] += quantity
            else:
                self.items[name] = quantity
            return True
        return False

    def remove(self, name, quantity):
        if name in self.items and self.items[name] > quantity:
            self.items[name] -= quantity
            return True
        return False

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return '\n'.join([f'{key} : {value}' for key, value in self.items.items()])

    def get_unique_items_count(self):
        return '\n'.join([f'{key} : {value}' for key, value in self.items.items() if value == 1])


class Shop(Store, Storage):
    def __init__(self, capacity=20):
        super().__init__(capacity)

    def add(self, name, quantity):
        if self.capacity > quantity + sum(self.items.values()) and len(self.items) < 5:
            if name in self.items:
                self.items[name] += quantity
            else:
                self.items[name] = quantity
            return True
        return False


class Request:
    def __init__(self, list_objects, request):
        self.list_objects = list_objects
        self.request = request
        for i in self.request.split():
            if i.isdigit():
                self.amount = int(i)
            elif i not in ('склад', 'магазин', 'Доставить', 'забирает', 'Курьер', 'из', 'в'):
                self.product = i
            elif i == 'склад' and i == self.request.split()[-3]:
                self.get_from = i
            elif i == 'магазин' and i == self.request.split()[-1]:
                self.get_to = i


def main(obj: Request):
    print('Эмм.... сейчас гляну что у нас есть')
    print(obj.list_objects[0].get_items())
    print()
    try:
        if obj.list_objects[0].remove(obj.product, obj.amount):
            if obj.list_objects[1].add(obj.product, obj.amount):
                print('Нужное количество есть на складе')
                print(f'Курьер забрал {obj.amount} {obj.product} со {obj.get_from}')
                print(f'Курьер везет {obj.amount} {obj.product} со {obj.get_from} в {obj.get_to}')
                print(f'Курьер доставил {obj.amount} {obj.product} в {obj.get_to}')
                print()
                print('В магазин хранится:')
                print()
                print(obj.list_objects[1].get_items())
            else:
                print('В магазин недостаточно места, попобуйте что то другое')
        else:
            print('Не хватает на складе, попробуйте заказать меньше')

    except AttributeError:
        print('введите коретный запрос... Пример "Доставить 3 печеньки из склад в магазин"')


shop_mag = Shop()
stor_sklad = Store()
shop_mag.add('собачки', 10)
stor_sklad.add('печеньки', 20)

req = Request([stor_sklad, shop_mag], input('Привет что будем доставлять? ->>>  '))

if __name__ == '__main__':
    main(req)
