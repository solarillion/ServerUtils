# Author: Nanda H Krishna (https://github.com/nandahkrishna)

import os
from Crypto.Cipher import AES
from flask import Flask, redirect, render_template, request, session, url_for
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

db_file = str(os.environ["DB_FILE_PATH"])

def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if "logged_in" not in session:
			return redirect(url_for("login"))
		return f(*args, **kwargs)
	return wrapper

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
	if "logged_in" in session:
		return redirect(url_for("home"))
	error = None
	if request.method == "POST":
		if request.form.get("info") == "Info":
			return redirect(url_for("info"))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		c.execute("SELECT * FROM login WHERE username=?", (request.form.get("username"),))
		result = c.fetchone()
		if result is None or result[1] != request.form.get("password"):
			error = "Invalid credentials. Please try again."
		else:
			session["logged_in"] = True
			session["username"] = request.form.get("username")
			return redirect(url_for("home"))
	return render_template("login.html", error=error)

@app.route("/info", methods=["GET", "POST"])
def info():
	if request.method == "POST":
		if request.form.get("home") == "Home":
			return redirect(url_for("home"))
		if request.form.get("account") == "Account":
			return redirect(url_for("account"))
		if request.form.get("login") == "Login":
			return redirect(url_for("login"))
		if request.form.get("logout") == "Logout":
			return redirect(url_for("logout"))
	return render_template("info.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
	if request.method == "POST":
		if request.form.get("account") == "Account":
			return redirect(url_for("account"))
		if request.form.get("info") == "Info":
			return redirect(url_for("info"))
		if request.form.get("logout") == "Logout":
			return redirect(url_for("logout"))
	return render_template("home.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
	if request.method == "POST":
		if request.form.get("home") == "Home":
			return redirect(url_for("home"))
		if request.form.get("info") == "Info":
			return redirect(url_for("info"))
		if request.form.get("logout") == "Logout":
			return redirect(url_for("logout"))
	return render_template("account.html")

@app.route("/logout")
@login_required
def logout():
	session.clear()
	redirect_url = url_for("login")
	return render_template("logout.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="7277")
