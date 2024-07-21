from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("phonebook.html")

@app.route("/", methods=["POST"])
def phonebook():
    name = request.form.get("Name")
    phonenumber = request.form.get("Phonenumber")
    connection = sqlite3.connect(currentdirectory + "/phonebook.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Phonebook (Name TEXT, PhoneNumber TEXT)")
    cursor.execute("INSERT INTO Phonebook (Name, PhoneNumber) VALUES (?, ?)", (name, phonenumber))
    connection.commit()
    connection.close()
    return redirect(url_for('main'))

@app.route("/resultpage", methods=["GET"])
def resultpage():
    name = request.args.get("Name")
    connection = sqlite3.connect(currentdirectory + "/phonebook.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Phonebook (Name TEXT, PhoneNumber TEXT)")
    cursor.execute("SELECT PhoneNumber FROM Phonebook WHERE Name=?", (name,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return render_template("resultpage.html", Name=name, Phonenumber=result[0])
    else:
        return render_template("resultpage.html", Name=name, Phonenumber="")

if __name__ == "__main__":
    app.run(debug=True)