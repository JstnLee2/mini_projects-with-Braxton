# Password Generator and storing

import random
import string
import pandas as pd
import os

def generate_password(min_length, num, special_char):
    letters = string.ascii_letters
    numbers = string.digits
    special = string.punctuation
      
    characters = letters

    if num:
        characters += numbers
    if special_char:
        characters += special

    pwd = ""
    meet_criteria = False
    has_number = False
    has_special = False

    while not meet_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char
        if new_char in numbers:
            has_number = True
        if new_char in special:
            has_special = True
        
        meet_criteria = True
        if num:
            meet_criteria = has_number
        if special_char:
            meet_criteria = meet_criteria and has_special
        

    return pwd


def save_pwd(domain, user_name, pwd):
    file_path = "password_storage.csv"
    file_exists = os.path.isfile(file_path) 
    if not file_exists:
        headers = ['Domain', 'UserName', 'Password']
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, mode='a', index=False)          

    df = pd.read_csv(file_path)
    exists = df["Domain"].isin([domain]).any()
    if exists:
        rewrite = input("Domain is already present in Password Storage.\nWould you like to overwrite (y/n)?").lower() == 'y'
    
        if rewrite:
            df.loc[df['Domain'] == domain, ['UserName', 'Password']] = [user_name, pwd]
            df.to_csv(file_path, index=False)

        else:
            new_input = [[domain, user_name, pwd]]
            new_df = pd.DataFrame(new_input)

            new_df.to_csv(file_path, mode='a', index=False, header=False)

    else:
        new_input = [[domain, user_name, pwd]]
        new_df = pd.DataFrame(new_input)

        new_df.to_csv(file_path, mode='a', index=False, header=False)

    
    return


min_length = int(input("What is the length of the password?"))
num = input("Do you want numbers in your password (y/n)?").lower() == "y"
special_char = input("Do you want special characters in your password (y/n)?").lower() == "y"


save_password = input("Would you like to save the password to the password manager (y/n)?").lower() == "y"

if save_password:
    domain = input("What is the domain of the saved password?").lower()
    user_name = input("What username is associated with this password?")
    pwd = generate_password(min_length, num, special_char)
    saved = save_pwd(domain, user_name, pwd)
    

    print("password saved")

if not save_password:
    pwd = generate_password(min_length, num, special_char)

print(pwd)


