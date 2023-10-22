"""
    DATABASE MODELS.
"""
from peewee import *
import uuid

database = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = database

class Tenant(BaseModel):
    id = IntegerField(primary_key=True)

    first_name = CharField(max_length=255, null=False)
    last_name = CharField(max_length=255, null=False)

    phone = CharField(max_length=11, null=False)
    email = CharField(max_length=255, unique=True, null=False)

    parents_address = CharField(max_length=255, null=False, default='')
    parents_phone = CharField(max_length=11, null=False, default='')

    note = TextField(null=False, default='')

class Owner(BaseModel):
    id = IntegerField(primary_key=True)

    first_name = CharField(max_length=255, null=False)
    last_name = CharField(max_length=255, null=False)

    phone = CharField(max_length=11, null=False)
    email = CharField(max_length=255, unique=True, null=False)

    note = TextField(null=False, default='')

class Apartment(BaseModel):
    id = IntegerField(primary_key=True)
    unique_identifier = UUIDField(default=uuid.uuid4)

    name = CharField(max_length=255, null=False, default='')
    address = CharField(max_length=255, null=False)
    city = CharField(max_length=255, null=False, default='')

    rooms = IntegerField(default=0, null=False)
    apartment_area = FloatField(default=0.0, null=False)
    floor = IntegerField(default=0, null=False)
    beds = IntegerField(null=False)

    note = TextField(null=False, default='')

    owner = ForeignKeyField(Owner, backref='apartments', null=True, on_delete='SET_NULL')

class LeaseContract(BaseModel):
    id = IntegerField(primary_key=True)

    start_date = DateField(null=False)
    end_date = DateField(null=False)

    rent_price = FloatField(null=False)
    utilities_included = BooleanField(null=False)
    tax = FloatField(null=False)

    note = TextField(null=False, default='')

    tenant = ForeignKeyField(Tenant, backref='lease_contracts', null=False, on_delete='CASCADE')
    apartment = ForeignKeyField(Apartment, backref='lease_contracts', null=False, on_delete='CASCADE')

class UtilityBills(BaseModel):
    id = IntegerField(primary_key=True)

    water = FloatField(default=0.0, null=False)
    electricity = FloatField(default=0.0, null=False)
    tax = FloatField(default=0.0, null=False)

class Transaction(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    transaction_type = CharField(max_length=7, null=False)
    amount = IntegerField(null=False)
    category = CharField(max_length=30, null=False)

    paid = BooleanField(null=False)

    description = TextField(null=False, default='')

    lease_contract = ForeignKeyField(LeaseContract, backref='transactions', null=False, on_delete='CASCADE')
    utility_bills = ForeignKeyField(UtilityBills, backref='transaction', null=True, on_delete='SET_NULL')

class NamedDate(BaseModel):
    id = IntegerField(primary_key=True)

    name = CharField(max_length=255, default='', null=False)
    date = DateTimeField(null=False)

class CellAction(BaseModel):
    id = IntegerField(primary_key=True)

    done = BooleanField(default=False)
    action = CharField(max_length=255, default='', null=False)

class Reminder(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    notify_owner = BooleanField(default=True, null=False)
    text = CharField(max_length=255, default='', null=False)
    email_subject = CharField(max_length=255, default='', null=False)

    lease_contract = ForeignKeyField(LeaseContract, backref='reminders', null=False, on_delete='CASCADE')
    # dates = ManyToManyField(NamedDate, backref='included_in_reminders', null=True)
    dates = ManyToManyField(NamedDate, backref='included_in_reminders')

class Task(BaseModel):
    id = IntegerField(primary_key=True)

    date = DateField(null=False)
    notify_owner = BooleanField(default=True, null=False)
    text = CharField(max_length=255, default='', null=False)
    email_subject = CharField(max_length=255, default='', null=False)

    note = TextField(null=False, default='')

    lease_contract = ForeignKeyField(LeaseContract, backref='tasks', null=False, on_delete='CASCADE')
    # dates = ManyToManyField(NamedDate, backref='included_in_tasks', null=True)
    # actions = ManyToManyField(CellAction, backref='included_in_tasks', null=True)
    dates = ManyToManyField(NamedDate, backref='included_in_tasks')
    actions = ManyToManyField(CellAction, backref='included_in_tasks')

def create_tables():
    with database:
        database.create_tables([Tenant,
                                Owner,
                                Apartment,
                                LeaseContract,
                                UtilityBills,
                                Transaction,
                                NamedDate,
                                CellAction,
                                Reminder,
                                Task])
