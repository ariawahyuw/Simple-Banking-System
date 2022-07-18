# Simple Banking System

This repo is a submission for Hyperskill's Jetbrain Academy (Python Core Study Track) Simple Banking System Project.

You can find the  program that I made at:
- [**Simple Banking System**](<Simple Banking System>)
    - [**task**](<Simple Banking System/task>)
      -  [**banking**](<Simple Banking System/task/banking>)
         -  [**banking.py**](<Simple Banking System/task/banking/banking.py>)

You can run it by executing this command:

    python "./Simple Banking System/task/banking/banking.py" 

The test can only be run using Jetbrains' EduTools plugin or run it directly from their website, but both need user's authentication.

## Program Description

The program is a command-line program that replicate basic tasks or actions for simple banking system. The program uses SQLite database to store card number, PIN, and balance. There are in total 7 unique actions you can do with this program.

### 1. Create an Account
Create an account using randomly generated number for card number and PIN. The card number follows this rule:

1. The length is 16 digits,
2. The IIN number (first 6 digits) is 400000,
3. The last digit is a check digit or checksum,
4. The other digits are identification number,
5. And it follows Luhn's algorithm.
   
The card number and PIN are then stored in the database.
   
### 2. Log into Account
The program will ask for card number and PIN. If the card number and PIN are correct (they are exist in the database), the app menu will be opened. Otherwise, the program will ask for card number and PIN again.

### 3. The App Menu
The menu has 6 actions:
### 3.1. Balance
Show balance from the current account.
### 3.2. Add income
Add balance to the current account. The program will ask for the amount of money you want to add.
### 3.3. Do transfer
Transfer to a valid card number (another card from the database). The transfer is valid if:
- The money transferred to another valid card number
- There is enough money from current account
### 3.4. Close account
Delete the current account from the database and return to the main menu.
### 3.5. Log out
Log out from the current account and return to the main menu.
### 3.6. Exit
Exit the program



### 4. Exit
Exit the program.
