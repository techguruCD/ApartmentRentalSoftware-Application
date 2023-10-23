from models import (
    Transaction,
    LeaseContract,
    UtilityBills,
    Apartment,
    Owner,
    Tenant,
)
from tools import total_pages
from peewee import JOIN
import settings


def _filter(search, transaction_type, category, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Transaction.date.contains(term)) |
                (Transaction.amount.contains(term)) |
                (Transaction.category.contains(term)) |

                (LeaseContract.start_date.contains(term)) |
                (LeaseContract.end_date.contains(term)) |
                (LeaseContract.rent_price.contains(term)) |

                (Tenant.first_name.contains(term)) |
                (Tenant.last_name.contains(term)) |
                (Tenant.phone.contains(term)) |
                (Tenant.email.contains(term)) |

                (Apartment.name.contains(term)) |
                (Apartment.address.contains(term)) |
                (Apartment.city.contains(term)) |
                (Apartment.unique_identifier.contains(term)) |

                (Owner.first_name.contains(term)) |
                (Owner.last_name.contains(term)) |
                (Owner.phone.contains(term)) |
                (Owner.email.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)

    if transaction_type != 'All':
        queryset = queryset.where(Transaction.transaction_type == transaction_type)

    if category not in (None, 'None'):
        queryset = queryset.where(Transaction.category == category)

    return queryset.distinct()

def transaction_list(search: str = None, transaction_type: str = 'All', category: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = (Transaction.select()
                .join(LeaseContract, JOIN.LEFT_OUTER, on=(Transaction.lease_contract == LeaseContract.id))
                .join(UtilityBills, JOIN.LEFT_OUTER, on=(Transaction.utility_bills == UtilityBills.id))
                .join(Apartment, JOIN.LEFT_OUTER, on=(LeaseContract.apartment == Apartment.id))
                .join(Tenant, JOIN.LEFT_OUTER, on=(LeaseContract.tenant == Tenant.id))
                .join(Owner, JOIN.LEFT_OUTER, on=(Apartment.owner == Owner.id))
    )
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search, transaction_type, category = final_url.split('\n')
        page = int(page)

        queryset = _filter(search, transaction_type, category, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{transaction_type}\n{category}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{transaction_type}\n{category}'

    else:
        queryset = _filter(search, transaction_type, category, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{transaction_type}\n{category}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'results': [Transaction._to_dict(transaction_object) for transaction_object in queryset.order_by(-Transaction.id).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_transaction(id: int) -> tuple[bool, dict | None]:
    try:
        transaction_object = Transaction.select().where(Transaction.id == id).get()
        return True, Transaction._to_dict(transaction_object)

    except Transaction.DoesNotExist:
        return False, None

def create_transaction(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        lease_contract_object = LeaseContract.get_by_id(_data.pop('lease_contract')['id'])
        utility_bills_object = _data.pop('utility_bills', None)

        if utility_bills_object is not None:
            utility_bills_object, _ = UtilityBills.get_or_create(**utility_bills_object)

        transaction_object = Transaction.create(**_data)
        transaction_object.lease_contract = lease_contract_object
        if utility_bills_object is not None:
            transaction_object.utility_bills = utility_bills_object

        transaction_object.save()

        return True, Transaction._to_dict(transaction_object)

    except Exception:
        return False, None

def update_transaction(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        id = _data.pop('id')

        lease_contract_object = _data.pop('lease_contract', None)
        if lease_contract_object is not None:    
            lease_contract_object = LeaseContract.get_by_id(lease_contract_object['id'])

        utility_bills_object = _data.pop('utility_bills', None)

        if utility_bills_object is not None:
            utility_bills_object, _ = UtilityBills.get_or_create(**utility_bills_object)

        transaction_object = Transaction.get_by_id(id)
        if lease_contract_object is not None:
            transaction_object.lease_contract = lease_contract_object
        if utility_bills_object is not None:
            transaction_object.utility_bills = utility_bills_object

        for key, value in _data.items():
            if hasattr(transaction_object, key):
                setattr(transaction_object, key, value)

        transaction_object.save()

        return True, Transaction._to_dict(transaction_object)

    except Exception:
        return False, None
