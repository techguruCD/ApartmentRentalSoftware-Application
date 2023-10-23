from api import *
import random
import string
import datetime
from models import LeaseContract, TRANSACTION_TYPES, TRANSACTION_CATEGORIES, create_tables

numbers = [str(i) for i in range(10)]
letters = list(string.ascii_lowercase)


def generate_tenants(count: int = 10):
    for i in range(count):
        tenant = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com',
            'parents_address': ''.join([random.choice(letters) for i in range(10)]),
            'parents_phone': ''.join([random.choice(numbers) for i in range(10)]),
            'note': ''.join([random.choice(letters + ['\n']) for i in range(100)]),
        }
        TenantApi.create_tenant(tenant)

def generate_owners(count: int = 10):
    for i in range(count):
        owner = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com',
            'note': ''.join([random.choice(letters + ['\n']) for i in range(100)]),
        }
        OwnerApi.create_owner(owner)

def generate_apartments(count: int = 10):
    for i in range(count):
        _, owner = OwnerApi.get_owner(random.randint(1, 10))
        apartment = {
            'name': ''.join([random.choice(letters) for i in range(10)]),
            'address': ''.join([random.choice(letters) for i in range(10)]),
            'city': ''.join([random.choice(numbers) for i in range(10)]),
            'rooms': random.randint(0, 9),
            'apartment_area': random.randint(0, 100) * random.random(),
            'floor': random.randint(0, 9),
            'beds': random.randint(0, 9),
            'note': ''.join([random.choice(letters + ['\n']) for i in range(100)]),
            'owner': owner,
        }
        ApartmentApi.create_apartment(apartment)

def generate_lease_contracts(count: int = 10):
    for i in range(count):
        _, tenant = TenantApi.get_tenant(random.randint(1, 10))
        _, apartment = ApartmentApi.get_apartment(random.randint(1, 10))
        lease_contract = {
            'start_date': (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 100))).date().isoformat(),
            'end_date': (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 100))).date().isoformat(),
            'rent_price': random.randint(0, 1000),
            'utilities_included': True if random.random() < .5 else False,
            'tax': random.randint(0, 100) * random.random(),
            'note': ''.join([random.choice(letters + ['\n']) for i in range(100)]),
            'tenant': tenant,
            'apartment': apartment
        }
        LeaseContractApi.create_lease_contract(lease_contract)

def generate_transactions(count: int = 10):
    lease_contracts = LeaseContract.select()
    for lease_contract in lease_contracts:
        for i in range(count):
            transaction = {
                'date': (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 10))).date().isoformat(),
                'transaction_type': TRANSACTION_TYPES.income if random.random() < .5 else TRANSACTION_TYPES.expense,
                'amount': random.randint(0, 1000),
                'category': TRANSACTION_CATEGORIES.other,
                'paid': True,
                'description': ''.join([random.choice(letters + ['\n']) for i in range(100)]),
                'lease_contract': LeaseContract._to_dict(lease_contract),
            }

def fill_db(count: int = 10):
    generate_tenants(count)
    generate_owners(count)
    generate_apartments(count)
    generate_lease_contracts(count)
    generate_transactions(count)

create_tables()
fill_db(10)