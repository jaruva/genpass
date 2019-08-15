# -*- coding: utf-8 -*-
import pickle
import smtplib

mail = smtplib.SMTP('smtp.gmail.com', 587)

class Entry:
    def __init__(self, website, creds):
        if type(creds) != dict:
            raise Exception("The 'creds' variable must be a dictionary with the keys being the username, and the values being the passwords to those usernames.")
        self.website = website
        self.creds = creds
        
def genpass(length, omit='', include=''):
    '''Length: length of the desired password
       Omit: create a string of characters that you want to omit
       Include: create a string of characters that you want to include'''
    import string
    import random
    
    if len(include) > length:
        raise Exception('Number of included characters cannot be greater than Length\n\n')
    if length > 30 or length < 0:
        raise Exception('Length cannot be greater than 30, or lower than 0\n\n')
    if type(length) != int:
        raise Exception('Length must be a number, dumbass\n\n')
    if ' ' in include:
        raise Exception("No spaces are allowed increds include, it must be a continous string\n\n")
    
    ascii = string.printable[:94]
    gen = ''
    bak = {}
    for i in range(length):
        char = random.choice(ascii)
        while True:
            if char not in omit:
                break
            char = random.choice(ascii)
        if char not in bak.keys():
            bak[char] = 0
        elif  bak[char] == 2:
            ascii = ascii.replace(char, '')
        else:
            bak[char] += 1
        gen = gen + char
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
    
def authenticate(password):
    pass
        
def decision_dialog():
    #put a secure login system here with hashes and shit   
    choice = input('''    
Welcome to the  Password Manager, please enter the number for one of the following options:
    
1) View/Edit stored passwords
2) Add a new password
3) Submit an idea for a feature\n\n''')
    while True:
        if choice not in ['1','2','3']:
            print("Please enter either '1', '2', or '3'.\n\n")
            choice = input()
        else:
            break
                
    if choice == '1':
        pass #do this later
        
    if choice == '2':
        website = input("Please enter the name of the website you would like to save this password for (ex. www.website.com)\n\n")
        user = input("Please enter your username for this website\n\n")
        fail = None
        while True:
            if fail != True:
                choice = input("Would you like to generate a new password for this website (y), or enter your own? (n)\n\n")
            if choice == 'y':
                while True:
                    omit = input("Please enter the characters that need to be omitted to comply with the website's requirements (Hit Enter if none)\n\n")
                    include = input("Please enter the characters that have to be included to comply with the complexity requirements (Hit Enter if none)\n\n")
                    length = input("Please enter the length of the password (Max 30)\n\n")
                    try:
                        passw = genpass(int(length), omit=omit, include=include)
                        break
                    except Exception as e:
                        print(e)
                break
            elif choice == 'n':
                passw = input("Please enter your own password\n\n")
                break
            else:
                choice = input("Please enter a (y) or an (n).\n\n")
                fail = True
        creds = {user:passw}
        e1 = Entry(website, creds)
        #make the file storage and encryption here
        
    if choice == '3':
        message = input("Please enter your idea/message below\n\n")
        #put some mail shit down here
    
decision_dialog()    
        
        