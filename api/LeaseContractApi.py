from models import (
    LeaseContract,
    Tenant,
    Apartment,
)
from settings import PAGINATION_PAGE_SIZE, SEARCH_DELIMETER
from tools import total_pages
import datetime

def _filter(search, active, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (LeaseContract.start_date.contains(term)) |
                (LeaseContract.end_date.contains(term)) |
                (LeaseContract.rent_price.contains(term)) |

                (LeaseContract.tenant.first_name.contains(term)) |
                (LeaseContract.tenant.last_name.contains(term)) |
                (LeaseContract.tenant.phone.contains(term)) |
                (LeaseContract.tenant.email.contains(term)) |

                (LeaseContract.apartment.name.contains(term)) |
                (LeaseContract.apartment.address.contains(term)) |
                (LeaseContract.apartment.city.contains(term)) |
                (LeaseContract.apartment.unique_identifier.contains(term)) |

                (LeaseContract.apartment.owner.first_name.contains(term)) |
                (LeaseContract.apartment.owner.last_name.contains(term)) |
                (LeaseContract.apartment.owner.phone.contains(term)) |
                (LeaseContract.apartment.owner.email.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)
    
    if active == True:
        queryset = queryset.where(LeaseContract.end_date<=datetime.datetime.now().date())

    return queryset

def lease_contract_list(search: str = None, active: bool = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = LeaseContract.select()
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search, active = final_url.split('\n')
        page = int(page)

        if active != 'None':
            active = bool(active)

        queryset = _filter(search, active, queryset)

        pages = total_pages(len(queryset),PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{active}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{active}'

    else:
        queryset = _filter(search, active, queryset)

        if total_pages(len(queryset),PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{active}'

    True, {
        'next': next_page,
        'previous': previous_page,
        'results': queryset.paginate(page, PAGINATION_PAGE_SIZE)
    }

def get_lease_contract(id: int) -> tuple[bool, dict | None]:
    lease_contract_object = LeaseContract.get_or_none(Apartment.id==id)

    if lease_contract_object is not None:
        return True, lease_contract_object

    return False, None

def create_lease_contract(data: dict) -> bool:
    try:
        tenant_object = Tenant.get_by_id(data.pop('owner')['id'])
        apartment_object = Apartment.get_by_id(data.pop('apartment')['id'])

        lease_contract_object = LeaseContract.create(**data)
        lease_contract_object.tenant = tenant_object
        lease_contract_object.apartment = apartment_object

        lease_contract_object.save()

        return True

    except Exception:
        return False

def update_lease_contract(data: dict) -> bool:
    try:
        id = data.pop('id')

        tenant_object = Tenant.get_by_id(data.pop('owner')['id'])
        apartment_object = Apartment.get_by_id(data.pop('apartment')['id'])

        lease_contract_object = Apartment.get_by_id(id)
        lease_contract_object.tenant = tenant_object
        lease_contract_object.apartment = apartment_object

        for key, value in data.items():
            if hasattr(lease_contract_object, key):
                setattr(lease_contract_object, key, value)

        lease_contract_object.save()

        return True

    except Exception:
        return False
