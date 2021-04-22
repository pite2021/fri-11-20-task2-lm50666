import random
from dataclasses import dataclass
import logging
import time
import multiprocessing
EUR_TO_HRK_EXCHANGE_RATE = 7.57
EUR_TO_PLN_EXCHANGE_RATE = 4.56
NUMBER_OF_TRADES = 5
logging.basicConfig(filename='task2.log', level=logging.DEBUG)


class Bank:
    def __init__(self, name, city, capital=10000):
        self.name = name
        self.city = city
        self.capital = capital
        self.clients = {}

    @property
    def capital(self):
        return self.__capital

    @capital.setter
    def capital(self, capital):
        if capital < 0:
            self.__capital = 0
        else:
            self.__capital = capital

    def __str__(self):
        return "{}".format(self.name)

    @staticmethod
    def eur_to_hrk(amount):
        return amount * EUR_TO_HRK_EXCHANGE_RATE

    @staticmethod
    def eur_to_pln(amount):
        return amount * EUR_TO_PLN_EXCHANGE_RATE

    @classmethod
    def european(cls):
        return cls("European bank {}".format(random.randint(1, 20)), "Bruxelles", 999999)

    @classmethod
    def american(cls):
        return cls("American bank {}".format(random.randint(1, 20)), "New York", 12345)

    @classmethod
    def empty(cls):
        return cls("None", "None", 0)

    def register_client(self, client):
        self.clients[client.bank_number] = (client.name, client.surname)

    def list_clients(self):
        return self.clients


class Client:
    def __init__(self, name, surname, bank_number, password, bank, balance=0):
        self.name = name
        self.surname = surname
        self.bank_number = bank_number
        self.password = password
        self.bank = bank
        self.balance = balance

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if len(password) < 5:
            self.__password = "password"
        else:
            self.__password = password

    @classmethod
    def deleted(cls):
        return "None", "None", 0

    def __str__(self):
        return "Client info: Name = {}, Surname = {}, Balance = {}, Bank = {}"\
            .format(self.name, self.surname, self.balance, self.bank)

    def change_bank(self, bank):
        try:
            if self.balance < 0:
                raise ValueError('Current balance is lower than 0.')
            else:
                del self.bank.clients[self.bank_number]
                self.bank = bank
                bank.register_client(self)
        except ValueError as e:
            logging.exception(e)
            pass

    def credit(self, amount):
        try:
            if amount > self.bank.capital:
                raise ValueError("There is not enough money in bank for credit")
            else:
                self.balance += amount
                self.bank.capital -= amount
        except ValueError as e:
            logging.exception(e)
            pass

    def delete(self):
        (self.name, self.surname, self.balance) = self.deleted()
        self.bank = Bank.empty()

    def withdrawal(self, amount):
        try:
            if amount > self.balance:
                raise ValueError("There is not enough money in your account for withdrawal")
            else:
                self.balance -= amount
        except ValueError as e:
            logging.exception(e)
            pass

    def deposit(self, amount):
        self.balance += amount

    def send_money(self, client, amount):
        client.balance += amount
        self.balance -= amount


@dataclass(init=True, repr=True)
class Market:
    name: str = "Stock market"
    city: str = "New York"
    number_of_banks: int = 1
    is_working: bool = False

    def trade(self, traders):
        for i in range(NUMBER_OF_TRADES):
            trader1, trader2 = random.sample(traders, 2)
            money_transfer = random.randint(0, trader1.balance)
            trader1.send_money(trader2, money_transfer)
            logging.info("Stock market = {}, Amount= {}, Sender={},Reciever={}"
                         .format(self.city, money_transfer, trader1.bank_number, trader2.bank_number))
            time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    market1 = Market()
    market2 = Market(city="London", number_of_banks=1)
    market3 = Market(city="Krakow", number_of_banks=1)
    bank1 = Bank.american()
    bank2 = Bank.european()
    bank3 = Bank("Krakow bank", "Krakow", 5000)
    client1 = Client("Luka", "Macan", 1, "qwecwq", bank1, 1000)
    client2 = Client("Lucija", "Macan", 2, "1cwq56", bank1, 2000)
    client3 = Client("Vedrana", "Macan", 3, "123ccw456", bank1, 3000)
    client4 = Client("Miljenko", "Macan", 4, "12342236", bank1, 4000)
    client5 = Client("Zeljko", "Grgic", 5, "12345cqw6", bank2, 1000)
    client6 = Client("Irena", "Grgic", 6, "12345cqq6", bank2, 2000)
    client7 = Client("Maja", "Grgic", 7, "12345cqw6", bank2, 3000)
    client8 = Client("NIka", "Grgic", 8, "12345cqcw6", bank2, 4000)
    client9 = Client("Filip", "Grgic", 9, "12345226", bank3, 1000)
    client10 = Client("Kreso", "Grubisic", 10, "12333456", bank3, 2000)
    client11 = Client("Iva", "Grubisic", 11, "12345qqs6", bank3, 3000)
    client12 = Client("Ivor", "Grubisic", 12, "12ww3456", bank3, 4000)

    first_group = [client1, client2, client3, client4]
    second_group = [client5, client6, client7, client8]
    third_group = [client9, client10, client11, client12]

    p1 = multiprocessing.Process(target=Market.trade, args=(market1, first_group,))
    p1.start()
    p2 = multiprocessing.Process(target=Market.trade, args=(market2, second_group,))
    p2.start()
    p3 = multiprocessing.Process(target=Market.trade, args=(market3, third_group,))
    p3.start()
    p1.join()
    p2.join()
    p3.join()
