from cryptography.fernet import Fernet
import getpass
'''
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)'''
        


def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


key = load_key()
fer = Fernet(key)

MASTER_PASSWORD = "KSUIS"  


def authenticate():
    """Authenticate the user with the master password."""
    try:
        # Use getpass to hide input
        master_pwd = getpass.getpass("Enter master password: ")
    except Exception as e:
        print("Error with secure input. Falling back to visible input.")
        master_pwd = input("Enter master password (visible): ")

    if master_pwd != MASTER_PASSWORD:
        print("Invalid master password. Exiting program.")
        exit()

def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:",
                  fer.decrypt(passw.encode()).decode())


def add():
    name = input('Account Name: ')
    pwd = input("Password: ")

    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

authenticate()

while True:
    mode = input(
        "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue

