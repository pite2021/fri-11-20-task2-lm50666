class Bank:
  clients=[]
  def __init__(self,name):
    self.name=name

  def register_client(self,client):
    self.clients.append(client)

  def show_clients(self):
    for client in self.clients:
      print(client)
  
  #def update_bank(client,balance):
   # client.set_money(balance)

class Client:

  def __init__(self,name,surname,amount_of_money=0):
    self.name=name
    self.surname=surname
    self.amount_of_money=amount_of_money

  def __str__(self):
    return "Name: {} Surname: {} Balance: {}".format(self.name,self.surname,self.amount_of_money)

  def input_money(self,amount):
    self.amount_of_money+=amount
  
  def withdraw_money(self,amount):
    self.amount_of_money-=amount

  def send_money(self,client,amount):
    client.amount_of_money+=amount
    self.amount_of_money-=amount

  #def set_money(self,balance):
   # self.amount_of_money=balance

if __name__ == "__main__":
  bank=Bank("Krakow Bank")
  client1=Client("Luka","Macan",100)
  client2=Client("Ivica","Ivic",200)
  bank.register_client(client1)
  bank.register_client(client2)
  bank.show_clients()
  client1.withdraw_money(6)
  bank.show_clients()

  client2.input_money(100)
  bank.show_clients()
  client2.send_money(client1,100)
  bank.show_clients()
  
  