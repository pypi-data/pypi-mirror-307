import os
from data_by_dorofeev import data


def main_main():
    while True:
        os.system("cls")
        choice = str(input("What do you want to do, register or log in?(R/e)"))
        if choice.lower() == "r":
            os.system("cls")
            data.registration()
        elif choice.lower() == "e":
            os.system("cls")
            data.entrance()
        else:
            os.system("cls")

def data_registration():
    data.registration()
def data_entrance():
    data.entrance()