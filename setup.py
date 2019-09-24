"""
Scripts to run to set up our database
"""
from datetime import datetime
from model import *
from passlib.hash import pbkdf2_sha256

# Create the database tables for our model
db.connect()
db.drop_tables([Donor, Donations])
db.create_tables([Donor, Donations])

#Update Donor class for all new donors
def populate_donors():
    for donor in donors:
        with db.transaction():
            new_donor = Donor.create(donor_name = donor)
#Update Donations class for all new donations
def populate_donations():
    for donation in donations:
        with db.transaction():
            new_donation = Donations.create(
            donation_name=donation[DONOR_NAME],
            donation_amount=donation[DONATION_AMOUNT])

#Update Donor Class with donations
def update_donors():
    for donor in Donor:
        don_matches = Donations.select().where(Donations.donation_name_id == donor)
        number_of_donations = don_matches.count()
        total = 0.0
        for item in don_matches.iterator():
            total += item.donation_amount
        donor.number_of_donations = number_of_donations
        donor.donation_total = total
        donor.save()
        
if __name__ == "__main__":
    #Default Donors
    donors = ['Justin Thyme',
              'Beau Andarrow',
              'Crystal Clearwater',
              'Harry Shins', 
              'Bob Zuruncle',
              'Al Kaseltzer',
              'Joe Somebody']
    
    # Default Donations
    DONOR_NAME = 0
    DONATION_AMOUNT = 1
    
    donations = [('Justin Thyme', 1), ('Justin Thyme', 1), ('Justin Thyme', 1),
                 ('Beau Andarrow', 207.12), ('Beau Andarrow', 400.32), ('Beau Andarrow', 12345),
                 ('Crystal Clearwater', 80082),
                 ('Harry Shins', 1), ('Harry Shins', 2), ('Harry Shins', 3), 
                 ('Bob Zuruncle', 0.53), ('Bob Zuruncle', 7.00),
                 ('Al Kaseltzer', 1010101), ('Al Kaseltzer', 666.00),
                 ('Joe Somebody', 25)]
    
    populate_donors()
    populate_donations()
    update_donors()