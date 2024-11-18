from flask import Flask, render_template, request, redirect, url_for, flash
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flashing messages

def load_key():
    with open("key.key", "rb") as file:
        key = file.read()
    return key

key = load_key()
fer = Fernet(key)

MASTER_PASSWORD = "KSUIS"

def authenticate(master_pwd):
    return master_pwd == MASTER_PASSWORD

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    master_pwd = request.form['master_password']
    if authenticate(master_pwd):
        return redirect(url_for('password_manager'))
    else:
        flash("Invalid master password", "danger")
        return redirect(url_for('home'))

@app.route('/password_manager', methods=['GET', 'POST'])
def password_manager():
    if request.method == 'POST':
        mode = request.form['mode'].lower()
        if mode == 'add':
            name = request.form['account_name']
            pwd = request.form['password']
            with open('passwords.txt', 'a') as f:
                f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")
            flash('Password added successfully!', 'success')
        elif mode == 'view':
            return redirect(url_for('view_passwords'))
    return render_template('home.html')

@app.route('/view_passwords')
def view_passwords():
    passwords = []
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            decrypted_pass = fer.decrypt(passw.encode()).decode()
            passwords.append((user, decrypted_pass))
    return render_template('view_passwords.html', passwords=passwords)

if __name__ == '__main__':
    app.run(debug=True)
