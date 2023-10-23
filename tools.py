from math import ceil
import datetime
from models import (
    Transaction,
    UtilityBills,
    LeaseContract,
    TRANSACTION_CATEGORIES,
    TRANSACTION_TYPES
)

def get_utc_offset():
    utc_now = datetime.datetime.utcnow()
    now = datetime.datetime.now()

    delta = now - utc_now

    hours, remainder = divmod(abs(delta.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)

    sign = '+' if delta >= datetime.timedelta(0) else '-'

    return f'{sign}{int(hours):02}:{int(minutes):02}'

def calculate_date_with_offset(date: str):
    if date.endswith('Z'):
        date = datetime.datetime.fromisoformat(date)
        offset = get_utc_offset()

        sign = 1 if offset[0] == '+' else -1
        hours = int(offset[1:3])
        minutes = int(offset[4:6])

        return (date + datetime.timedelta(hours=sign*hours, minutes=sign*minutes)).strftime('%Y-%m-%dT%H:%M:00') + offset
    
    return date

def total_pages(total_rows: int, rows_per_page: int) -> int:
    return ceil(total_rows / rows_per_page)

def generate_rental_month_transactions():
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)

    transaction_query = (
        (Transaction.date >= start_date) &
        (Transaction.date <= end_date) &
        (Transaction.category == TRANSACTION_CATEGORIES.rent_payment)
    )
    transaction_queryset = Transaction.select().where(transaction_query).distinct()

    lease_contract_query = (
        (LeaseContract.end_date > today)
    )
    lease_contract_queryset = LeaseContract.select().where(lease_contract_query).distinct()

    if transaction_queryset.count() < lease_contract_queryset.count():
        transaction_lease_contracts = [Transaction._to_dict(transaction_object)['lease_contract'] for transaction_object in transaction_queryset]
        lease_contracts = [LeaseContract._to_dict(lease_contract_object) for lease_contract_object in lease_contract_queryset]

        for lease_contract in lease_contracts:
            if lease_contract not in transaction_lease_contracts:
                transaction = {
                    'date': today,
                    'transaction_type': TRANSACTION_TYPES.income,
                    'amount': lease_contract['rent_price'],
                    'category': TRANSACTION_CATEGORIES.rent_payment,
                    'paid': False,
                }

                lease_contract_object = LeaseContract.get_by_id(lease_contract['id'])
                transaction_object = Transaction.create(**transaction)
                transaction_object.lease_contract = lease_contract_object
                transaction_object.save()

def generate_utility_bills_month_transactions() -> bool:
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)

    transaction_query = (
        (Transaction.date >= start_date) &
        (Transaction.date <= end_date) &
        (Transaction.category == TRANSACTION_CATEGORIES.utility_bills_payment)
    )
    transaction_queryset = Transaction.select().where(transaction_query).distinct()

    lease_contract_query = (
        (LeaseContract.end_date > today) &
        (LeaseContract.utilities_included == False)
    )
    lease_contract_queryset = LeaseContract.select().where(lease_contract_query).distinct()

    if transaction_queryset.count() < lease_contract_queryset.count():
        transaction_lease_contracts = [Transaction._to_dict(transaction_object)['lease_contract'] for transaction_object in transaction_queryset]
        lease_contracts = [LeaseContract._to_dict(lease_contract_object) for lease_contract_object in lease_contract_queryset]

        for lease_contract in lease_contracts:
            if lease_contract not in transaction_lease_contracts:
                transaction = {
                    'date': today,
                    'transaction_type': TRANSACTION_TYPES['income'],
                    'amount': lease_contract['tax'] / 12,
                    'category': TRANSACTION_CATEGORIES.utility_bills_payment,
                    'paid': False,
                }

                utility_bills_object = UtilityBills.create(**{'tax':lease_contract['tax'] / 12,})
                lease_contract_object = LeaseContract.get_by_id(lease_contract['id'])
                transaction_object = Transaction.create(**transaction)
                transaction_object.lease_contract = lease_contract_object
                transaction_object.utility_bills = utility_bills_object
                transaction_object.save()
