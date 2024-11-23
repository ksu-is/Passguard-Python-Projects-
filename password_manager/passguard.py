from flask import Flask, request, render_template_string, redirect, url_for, flash
import os
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session and flash messages

# Master password for viewing plaintext passwords
MASTER_PASSWORD = "mypassword"  # Replace with your secure master password

# In-memory password store
password_store = {}

# Control plaintext password visibility
show_plaintext = False

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Manager</title>
</head>
<body>
    <h1>Password Manager</h1>
    {% with messages = get_flashed_messages() %}
    {% if messages %}
        <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
    {% endwith %}
    <form action="/" method="POST">
        <label for="service">Service Name:</label>
        <input type="text" id="service" name="service" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <button type="submit">Save Password</button>
    </form>
    <h2>Saved Passwords</h2>
    <form action="/toggle" method="POST">
        {% if not authenticated %}
        <label for="master_password">Enter Master Password:</label>
        <input type="password" id="master_password" name="master_password" required>
        <button type="submit">Authenticate</button>
        {% else %}
        <button type="submit">{{ "Hide Plaintext Passwords" if show_plaintext else "Show Plaintext Passwords" }}</button>
        {% endif %}
    </form>
    <ul>
        {% for service, data in passwords.items() %}
        <li>
            <b>{{ service }}</b>: 
            {{ data['plaintext'] if show_plaintext else data['hashed'] }}
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global show_plaintext
    if request.method == "POST":
        service = request.form["service"]
        password = request.form["password"]
        # Hash the password and store both plaintext and hashed versions
        hashed_password = generate_password_hash(password)
        password_store[service] = {"plaintext": password, "hashed": hashed_password}
        flash(f"Password for {service} saved successfully!")
        return redirect(url_for("home"))
    return render_template_string(
        html_template, 
        passwords=password_store, 
        show_plaintext=show_plaintext, 
        authenticated=False
    )

@app.route("/toggle", methods=["POST"])
def toggle():
    global show_plaintext
    master_password = request.form.get("master_password")
    
    if master_password:
        if master_password == MASTER_PASSWORD:
            show_plaintext = not show_plaintext
            flash("Master password authenticated. Displaying plaintext passwords.")
        else:
            flash("Incorrect master password. Try again.")
    else:
        show_plaintext = False  # Default back to hiding passwords if no password is provided
    
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
