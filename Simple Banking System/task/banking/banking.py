import random
import sqlite3


conn = sqlite3.connect('card.s3db')  # Creating a connection to card.s3db
cur = conn.cursor()  # Set cursor to current connection
cur.execute('''CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);
    ''')  # If the database table doesn't exist,  
          # create a new table with (id,number,pin,balance) header
          

def is_luhn_number(card_number):
    '''Check if the card number passed Luhn's algorithm. 
       Return true if the number passed the test, otherwise return false.
       More info of Luhn algorithm is available in 
       ./Simple Banking System/Luhn algorithm/task.html'''
    card_int_number = [int(char) for char in str(card_number)]
    for i, num in enumerate(card_int_number):
        if (i + 1) % 2 != 0:
            tmp = num * 2
            card_int_number[i] = tmp if tmp <= 9 else tmp - 9 
    return sum(card_int_number) % 10 == 0


def check_card(card_number):
    '''Check if the card IIN number is 400000 and the card numbers have
       maximum length of 16. The IIN number and card numbers length are
       specified only for this program'''
    return(card_number[0:6] == "400000" 
        and len(card_number) == 16
        and is_luhn_number(card_number))


def add_balance(card_number, added_amount):
    cur.execute('UPDATE card SET balance=balance+? WHERE number = ?',
                (added_amount, card_number))
    conn.commit()


def balance(card_number):
    cur.execute('SELECT balance FROM card WHERE number = ?', (card_number,))
    current_balance, _ = cur.fetchone()
    return current_balance


class Menu:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
    
    def app(self):
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Logout\n0. Exit')
        app_input = int(input())
        if app_input == 1:
            print(balance(self.card_number))
            self.app()
        elif app_input == 2:
            added_amount = int(input('\nEnter income:\n'))
            add_balance(self.card_number, added_amount)
            print('Income was added!\n')
            self.app()
        elif app_input == 3:
            print('Transfer')
            card_target = input('Enter card number:\n').strip()
            cur.execute('SELECT number FROM card WHERE number = (?)', (card_target,))
            status = cur.fetchone()
            luhn_result = check_card(card_target)
            if card_target == self.card_number:
                print('You can"t transfer money to the same account!')
            elif luhn_result is False:
                print("Probably you made mistake in the card number. Please try again!")
                self.app()
            elif status is None:
                print('Such a card does not exist.')
                self.app()
            else:
                transfer_amount = int(input('Enter how much money you want to transfer:\n'))
                current_balance = balance(self.card_number)
                if current_balance >= transfer_amount:
                    add_balance(self.card_number, -transfer_amount)
                    add_balance(card_target, transfer_amount)
                    print('Success!')
                    self.app()
                else:
                    print('Not enough money!')
                    self.app()
        elif app_input == 4:
            cur.execute('DELETE FROM card WHERE number = (?)',
                (self.card_number,))
            conn.commit()
            print('The account has been closed!')
        elif app_input == 5:
            print('You have successfully logged out!')
            return None
        else:
            exit()


def log_in():
    card_input = str(input('Enter your card number:').strip())
    pin_input = str(input('Enter your PIN:'))
    cur.execute('''SELECT number, pin FROM card WHERE
        number =  ?
        AND pin = ? ''', (card_input, pin_input))
    row = cur.fetchone()
    if row is None:
        print('Wrong card number or PIN!')
    else:
        print('You have successfully logged in!')
        app_start = Menu(card_input, pin_input)
        app_start.app()


def create_acc():
    account_identifier = str(random.randint(000000000, 999999999))
    seeder = str(random.randint(0, 9))
    account_identifier = '0' * (9 - len(account_identifier)) + account_identifier
    card_number = '400000' + account_identifier + seeder
    if check_card(card_number) is True:
        number = card_number
        seed = int(account_identifier + seeder)
        random.seed(seed)
        pin_generator = random.sample(range(0, 9), 4)
        pin = str(pin_generator[0]) + str(pin_generator[1]) + str(pin_generator[2]) + str(pin_generator[3])
        cur.execute('INSERT INTO card (id, number, pin, balance) VALUES (0, ?, ?, 0)', (number, pin))
        conn.commit()
        print(f'\nYour card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}\n')
    else:
        create_acc()


class MainMenu:
    while True:
        A = f'1. Create an account\n2. Log into account\n0. Exit\n'
        menu = int(input(A))
        if menu == 1:
            create_acc()
        elif menu == 2:
            log_in()
        else:
            print('Bye!')
            break


MainMenu()
