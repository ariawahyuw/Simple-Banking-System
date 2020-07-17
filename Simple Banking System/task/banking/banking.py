import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);
    ''')


def luhn(card_number):
    account_identifier = ""
    for i in range(6, 15):
        account_identifier += card_number[i]
    seeder = card_number[15]
    first_number = int(card_number[0])
    temp = 0
    luhn_number = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(account_identifier)):
        if i % 2 == 0:
            luhn_number[i] = int(account_identifier[i]) * 2
            if int(account_identifier[i]) * 2 > 9:
                luhn_number[i] = luhn_number[i] - 9
        else:
            luhn_number[i] = int(account_identifier[i])
    for k in luhn_number:
        temp += int(k)
    if (temp + first_number * 2 + int(seeder)) % 10 == 0:
        return True


class Menu:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin

    def balance(self):
        print()
        print(cur.execute('SELECT balance FROM card WHERE number = ?', self.card_number))
        print()
        Menu.app(self)

    def app(self):
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Logout\n0. Exit')
        app_input = int(input())
        if app_input == 1:
            Menu.balance(self)
        elif app_input == 2:
            add_balance = int(input('\nEnter income:\n'))
            cur.execute('UPDATE card SET balance=balance+? WHERE number = ?', (add_balance, self.card_number))
            conn.commit()
            print('Income was added!\n')
            Menu.app(self)
        elif app_input == 3:
            print('Transfer')
            card_target = str(input('Enter card number:\n'))
            cur.execute('SELECT number FROM card WHERE number = (?)', (card_target,))
            status = cur.fetchone()
            luhn_result = luhn(card_target)

            if card_target == self.card_number:
                print('You can"t transfer money to the same account!')
            elif luhn_result is None:
                print("Probably you made mistake in the card number. Please try again!")
                print()
                Menu.app(self)
            elif status is None:
                print('Such a card does not exist.')
                Menu.app(self)
            else:
                transfer_amount = int(input('Enter how much money you want to transfer:\n'))
                cur.execute('SELECT balance FROM card WHERE number = (?)', (self.card_number,))
                balance = cur.fetchone()
                balance = int(balance[0])
                if balance >= transfer_amount:
                    cur.execute('UPDATE card SET balance=balance-? WHERE number = ?', (transfer_amount, self.card_number))
                    cur.execute('UPDATE card SET balance=balance+? WHERE number = ?', (transfer_amount, card_target))
                    conn.commit()
                    print('Success!')
                    Menu.app(self)
                else:
                    print('Not enough money!')
                    Menu.app(self)
        elif app_input == 4:
            cur.execute('DELETE FROM card WHERE number = (?)', (self.card_number,))
            conn.commit()
            print()
            print('The account has been closed!')
            print()
        elif app_input == 5:
            print()
            print('You have successfully logged out!')
            print()
            return None
        else:
            exit()


def log_in():
    card_input = str(input('Enter your card number:'))
    pin_input = str(input('Enter your PIN:'))
    cur.execute('''SELECT number, pin FROM card WHERE
        number =  ?
        AND pin = ? ''', (card_input, pin_input))
    row = cur.fetchone()
    if row is None:
        print()
        print('Wrong card number or PIN!')
        print()
    else:
        print()
        print('You have successfully logged in!')
        print()
        app_start = Menu(card_input, pin_input)
        app_start.app()


def create_acc():  # Don't  change or the program will don't work!
    account_identifier = str(random.randint(000000000, 999999999))
    seeder = str(random.randint(0, 9))
    account_identifier = '0' * (9 - len(account_identifier)) + account_identifier
    card_number = '400000' + account_identifier + seeder
    if luhn(card_number) is True:
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
            print()
            print('Bye!')
            break


MainMenu()
