import os

from peewee import *
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///donor_database.db'))

class BaseModel(Model):
    """
    BaseModel class to inherit from
    """
    class Meta:
        database = db

class Donor(BaseModel):
    """
    Donor Class
    """
    donor_name = CharField(primary_key=True)
    number_of_donations = IntegerField(null=True)
    donation_total = FloatField(null=True)
    
    class Meta:
        database = db    

class Donations(BaseModel):
    """
    Donations Class
    """
    donation_name = ForeignKeyField(Donor, related_name='is_donated_by')
    donation_amount = FloatField()
    
    class Meta:
        database = db    
    
