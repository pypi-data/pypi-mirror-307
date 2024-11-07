import os
import datetime
import hashlib


def _login():
    while True:
        login_ = str(input("Enter login: "))
        while True:
            if len(login_) == 0:
                os.system("cls")
                break
            if not os.path.isfile(f"C:\\rec_users\\{login_}-pass.dat"):
                if 20 >= len(login_) > 0:
                    return login_
                    break
            else:
                os.system("cls")
                break
def _password(login):
    while True:
        password_ = str(input("Enter password: "))
        while True:
            if len(password_) < 8:
                os.system("cls")
                print("*The password must contain more than 8 characters\n")
                print(f"Enter login: {login}")
                break
            else:
                return password_
                break
        if len(password_) > 8:
            break
def _confirm_password(login, password):
    os.system("cls")
    i = 0
    confirm_password_ = ""
    while True:
        if i > 0:
            confirm_password_ = str(input("Confirm password: "))
        while True:
            if password != confirm_password_:
                os.system("cls")
                print(f"Enter login: {login}")
                print(f"Enter password: {password}")
                i += 1
                break
            else:
                break
        if len(confirm_password_) > 0 and password == confirm_password_:
            return confirm_password_
            break


def rec_data(login, password):
    if os.path.isdir("C:\\rec_users"):
        pass
    else:
        try:
            os.mkdir("C:\\rec_users")
        except FileExistsError:
            os.system("cls")
            print(print("Error:"
                        "\n\tPlease email - 'dorofeevav1149@gmail.com'"
                        "\n\tIf You see this message"
                        "\n\t\tYou need to send a description"
                        "\n\tof the problem and a screenshot"))
            os.system("pause")
            exit()
    retry_pass = ''
    i = 1
    o = 0
    while True:
        if len(password) >= i:
            a = password[o]
            retry_pass = retry_pass + str(ord(a)) + ' '
            i += 1
            o += 1
        else:
            del i, o
            break
    password = retry_pass[:-1]
    password = password.split()
    count = len(password)
    i = 0
    passwords = ""
    while i != count:
        passwords += hex(int(password[i])) + "-"
        i += 1
    passwords = passwords[:-1]
    hash_password = hashlib.sha256(passwords.encode('utf-8')).hexdigest()
    retry_data = ''
    i = 1
    o = 0
    _data_ = str(f"Create: {datetime.datetime.now()}\n")
    while True:
        if len(_data_) >= i:
            a = _data_[o]
            retry_data = retry_data + str(ord(a)) + ' '
            i += 1
            o += 1
        else:
            del i, o
            break
    data = retry_data[:-1]
    data = data.split()
    count = len(data)
    i = 0
    datas = ""
    while i != count:
        datas += hex(int(data[i])) + "-"
        i += 1
    datas = datas[:-1]
    with open(f"C:\\rec_users\\{login}-pass.dat", "w", encoding="utf-8") as file:
        file.write(hash_password)
        file.close()
    with open(f"C:\\rec_users\\{login}.dat", "w", encoding="utf-8") as file:
        file.write(datas)
        file.close()
    os.system("pause")


def registration():
    login = _login()
    password = _password(login)
    confirm_password = _confirm_password(login, password)
    rec_data(login, password)

def entrance():
    login = str(input("Enter login: "))
    password = str(input("Enter password: "))

    if os.path.isfile(f"C:\\rec_users\\{login}.dat") and os.path.isfile(f"C:\\rec_users\\{login}-pass.dat"):
        retry_pass = ''
        i = 1
        o = 0
        while True:
            if len(password) >= i:
                a = password[o]
                retry_pass = retry_pass + str(ord(a)) + ' '
                i += 1
                o += 1
            else:
                del i, o
                break
        password = retry_pass[:-1]
        password = password.split()
        count = len(password)
        i = 0
        passwords = ""
        while i != count:
            passwords += hex(int(password[i])) + "-"
            i += 1
        passwords = passwords[:-1]
        hash_password = hashlib.sha256(passwords.encode('utf-8')).hexdigest()
        with open(f"C:\\rec_users\\{login}-pass.dat", "r") as file:
            password = file.read()
            file.close()
        if hash_password == password:
            with open(f"C:\\rec_users\\{login}.dat") as file:
                data = file.read()
                file.close()
            data = data.replace("-", " ").split()
            count = len(data)
            i = 0
            datas = ""
            while i != count:
                datas += str(int(data[i], 16)) + " "
                i += 1
            datas = datas.split()
            i = 0
            data = ""
            while i != count:
                data += str(chr(int(datas[i])))
                i += 1
            os.system("cls")
            print(data)
            answer = str(input("\nDo you want to change the text?(Y/n)"))
            os.system("cls")
            print(data)
            if answer.lower() == "y":
                while True:
                    add_text = str(input("\nEnter the line(n - to cancel, d - delete the last line)\n    "))
                    if add_text.lower() == "n":
                        os.system("cls")
                        print(data)
                        break
                    elif add_text.lower() == "d":
                        os.system("cls")
                        data = data[:data.rfind('\n')]
                        print(data)
                    else:
                        data += f"\n{add_text}"
                        os.system("cls")
                        print(data)
                answer = str(input("Save the file?(Y/n)"))
                if answer.lower() == "y":
                    retry_data = ''
                    i = 1
                    o = 0
                    _data_ = str(f"Edit: {datetime.datetime.now()}\n{data}")
                    while True:
                        if len(_data_) >= i:
                            a = _data_[o]
                            retry_data = retry_data + str(ord(a)) + ' '
                            i += 1
                            o += 1
                        else:
                            del i, o
                            break
                    data = retry_data[:-1]
                    data = data.split()
                    count = len(data)
                    i = 0
                    datas = ""
                    while i != count:
                        datas += hex(int(data[i])) + "-"
                        i += 1
                    datas = datas[:-1]
                    with open(f"C:\\rec_users\\{login}-pass.dat", "w", encoding="utf-8") as file:
                        file.write(hash_password)
                        file.close()
                    with open(f"C:\\rec_users\\{login}.dat", "w", encoding="utf-8") as file:
                        file.write(datas)
                        file.close()
                    os.system("pause")
                else:
                    os.system("pause")
            else:
                os.system("pause")
        else:
            print("The wrong password was entered")
            os.system("pause")
    else:
        print("The record was not found")
        os.system("pause")

