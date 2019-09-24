import os

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256
from model import *

app = Flask(__name__)
app.secret_key = 'qwfh2123hf08hsd'
#os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('list_donors'))

@app.route('/home')
def list_donors():
    return render_template('home.jinja2', donors=Donor.select())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        donor_list = [donor.donor_name for donor in Donor.select()]
        name = request.form['name']
        amount = float(request.form['amount'])
        
        if name not in donor_list:
            new_donor = Donor.create(donor_name = name, number_of_donations = 0,
                                     donation_total = 0)
        donor = Donor.select().where(Donor.donor_name == name).get()           
        new_donation = Donations.create(
        donation_name = name,
        donation_amount = amount)
        donor.number_of_donations = donor.number_of_donations + 1
        donor.donation_total = donor.donation_total + amount
        donor.save()
        new_donation.save()
        
        return redirect(url_for('list_donors'))
    else:
        return render_template('create.jinja2', donors=Donor.select())

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        donor_list = [donor.donor_name for donor in Donor.select()]
        name = request.form['name']
        if name not in donor_list:
            with db.transaction():
                return redirect(url_for('list_donors'))
        with db.transaction():
            deleteme = Donor.get(donor_name = name)
            deleteme.delete_instance()
        return redirect(url_for('list_donors'))
    else:
        return render_template('delete.jinja2', donors=Donor.select())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port = port)


