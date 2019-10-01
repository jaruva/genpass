# -*- coding: utf-8 -*-
import pickle
import pyAesCrypt
import os
import clipboard
from getpass import getpass


# TODO add functionality

# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024

if not os.path.exists(os.path.expanduser('~/genpass')):
    os.mkdir(os.path.expanduser('~/genpass'))
os.chdir(os.path.expanduser('~/genpass'))

cwd = os.getcwd()

# path of the unencrypted data
datapath = cwd + '/data.txt'
encpath = cwd + '/data.dat'


class Entry:
    def __init__(self, website, username, password):
        self.website = website
        self.username = username
        self.password = password


def genpass(length, omit='', include=''):
    """Creates a secure password with the given arguments that complies with most websites security requirements. omit and include are optional arguments.
       Length: length of the desired password
       Omit: a string of characters that you want to omit, generally for special characters defined by the websites password requirements
       Include: a string of characters that need to be included"""
    import string
    import random

    # initial variables
    special = "!@#$%^&*?"
    numbers = "1234567890"
    ascii = string.printable[:62] + special
    gen = ''
    bak = {}

    # force includes one character from both special and numbers
    include = include + random.choice(special) + random.choice(numbers)

    for i in range(length):
        char = random.choice(ascii)
        # this checks to see if the character is in omit, and then picks a new character until it has one that's allowed
        while True:
            if char not in omit:
                break
            char = random.choice(ascii)
        # this if statement will reduce repetition in the final output, it checks if the current letter in char has been used 3 times, if it has then it removes the letter in the ascii string
        if char not in bak.keys():
            bak[char] = 0
        elif bak[char] == 2:
            ascii = ascii.replace(char, '')
        else:
            bak[char] += 1
        # concatenation
        gen = gen + char

    # this replaces current characters in the completed password string with the force included characters
    if ' ' in include:
        include.replace(' ', '')
    ind = list(range(len(gen)))
    gen = list(gen)
    for i in include:
        x = random.choice(ind)
        del ind[ind.index(x)]
        gen[x] = i
    y = ''
    for i in gen:
        y = y + i

    return y

#Below is the dialog

# new user protocols
if not os.path.exists(datapath):
    x = open('data.txt', 'wb')
    pickle.dump({}, x)
    x.close()
    while True:
        ini = input("Please create a password: ")
        conf = input("Please enter the password again: ")
        if ini != conf:
            print("\nERROR: Passwords do not match, try again\n")
        else:
            break

    pyAesCrypt.encryptFile('data.txt', 'data.dat', conf, bufferSize)
    print(
        '!!! Warning! !!!\n\n If you lose this password then all your stored passwords will be lost, keep it safe.\n\n')
# login
while True:
    encpass = getpass()
    try:
        pyAesCrypt.decryptFile(encpath, datapath, encpass, bufferSize)
        break
    except ValueError:
        print("\nERROR: Incorrect password, try again\n")
x = open('data.txt','rb')
data = pickle.load(x)
x.close()
pyAesCrypt.encryptFile(datapath, encpath, encpass, bufferSize)

# options
while True:
    choice = input('''    
Welcome to GenPass, please enter the number for one of the following options:

1) View/Edit stored passwords
2) Add a new password
3) Exit\n\n>''')

    if choice == '1':
        websites = list(data.keys())
        if len(websites) == 0:
            print("\n\nERROR: You don't have any passwords yet")
            continue
        sorted(websites, key=str.lower)
        print("WEBSITES:\n")
        for i in websites:
            print(i)
        while True:
            website = input("\nType the associated website of an entry in order to view it. To stop type 'exit'\n\n>")
            if website in websites:
                e = data[website]
                while True:
                    print("URL: " + website + "\nUsername: " + e.username + "\nPassword: " + e.password + '\n')
                    choice = input("1) Edit\n2) Delete\n3) Copy password to clipboard\n4) Exit\n\n>")
                    choice = str(choice)
                    if choice == '1':
                        while True:
                            choice = input("What would you like to edit?\n\n1)URL\n2)Username\n3)Password\n4)Exit\n\n>")
                            choice = str(choice)
                            if choice == '1':
                                print("Current entry: " + website)
                                new_website = input("Please enter the new value for this entry: ")
                                username = e.username
                                password = e.password
                                del data[website]
                                data[new_website] = Entry(new_website, username, password)
                                break
                            elif choice == '2':
                                print("Current entry: " + e.username)
                                e.username = input("Please enter the new value for this entry: ")
                                data[website].username = e.username
                                break
                            elif choice == '3':
                                print("Current entry: " + e.password)
                                e.password = input("Please enter the new value for this entry: ")
                                data[website].password = e.password
                                break
                            elif choice == '4':
                                break
                            else:
                                print("\n\nERROR: Please enter either a 1, 2, 3, or 4\n\n")

                    elif choice == '2':
                        del data[website]
                        print("\nData Deleted\n.")
                    elif choice == '3':
                        clipboard.copy(e.password)
                    elif choice == '4':
                        break
                    else:
                        print("\n\nERROR: Please enter a valid option'\n\n")
                break
            elif website == 'exit':
                break
            else:
                print(website)
                print("\n\nERROR: Please enter a valid option")

    elif choice == '2':
        website = input("Please enter the URL of the website this password belongs to.\n\n")
        user = input("Please enter your username for this website\n\n")
        while True:
            choice = input("Would you like to generate a new password for this website (y), or enter your own? (n)\n\n")
            if choice == 'y':
                while True:
                    choice = input("Are there any characters that need to be omitted from the password? (y/n): ")
                    if choice == 'y':
                        omit = input("Please enter the characters you want to omit: ")
                        break
                    elif choice == 'n':
                        omit = ''
                        break
                    else:
                        print('''\nERROR: Please enter either a "y" or an "n"\n''')

                while True:
                    choice = input("Are there characters that need to be included in the password? (y/n): ")
                    if choice == 'y':
                        include = input("Please enter the characters you want to include: ")
                        break
                    elif choice == "n":
                        include = ''
                        break
                    else:
                        print('''\nERROR: Please enter either a "y" or an "n"\n''')

                while True:
                    length = input("Please enter the length of the password (Must be between 10 and 30): ")
                    length = str(length)
                    if length > '30' or length < '10':
                        print("\nERROR: Please enter a number between 10 and 30\n")
                    else:
                        break

                passw = genpass(int(length), omit=omit, include=include)
                break

            elif choice == 'n':
                while True:
                    passw = input("Please enter the password: ")
                    conf = input("Please enter the password again: ")
                    if passw != conf:
                        print("\nERROR: Passwords do not match, try again\n")
                    else:
                        break
                break
            else:
                print('''\nERROR: Please enter either a "y" or an "n"\n''')

        e1 = Entry(website, user, passw)
        data[e1.website] = e1
        pyAesCrypt.decryptFile(encpath, datapath, encpass, bufferSize)
        x = open(datapath, 'wb')
        pickle.dump(data, x)
        x.close()
        pyAesCrypt.encryptFile(datapath, encpath, encpass, bufferSize)

    elif choice == '3':
        pyAesCrypt.decryptFile(encpath, datapath, encpass, bufferSize)
        x = open('data.txt', 'wb')
        pickle.dump(data, x)
        x.close()
        pyAesCrypt.encryptFile(datapath, encpath, encpass, bufferSize)
        break
    else:
        print("\n\nERROR: Please enter a valid option\n\n")
