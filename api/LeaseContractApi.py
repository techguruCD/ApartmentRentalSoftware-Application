from models import (
    LeaseContract,
    Tenant,
    Apartment,
    Owner
)
from tools import total_pages
from peewee import JOIN
import datetime
import settings


def _filter(search, active, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (LeaseContract.rent_price.contains(term)) |
                (LeaseContract.start_date.contains(term)) |
                (LeaseContract.end_date.contains(term)) |

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
    
    if active == True:
        queryset = queryset.where(LeaseContract.end_date >= datetime.datetime.now().date())

    return queryset.distinct()

def lease_contract_list(search: str = None, active: bool = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = (LeaseContract.select()
                .join(Apartment, JOIN.LEFT_OUTER, on=(LeaseContract.apartment == Apartment.id))
                .join(Tenant, JOIN.LEFT_OUTER, on=(LeaseContract.tenant == Tenant.id))
                .join(Owner, JOIN.LEFT_OUTER, on=(Apartment.owner == Owner.id))
    )
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search, active = final_url.split('\n')
        page = int(page)

        if active != 'None':
            active = bool(active)

        queryset = _filter(search, active, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{active}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{active}'

    else:
        queryset = _filter(search, active, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{active}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'current': f'{page}\n{search}\n{active}',
        'results': [LeaseContract._to_dict(lease_contract_object) for lease_contract_object in queryset.order_by(-LeaseContract.id).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_lease_contract(id: int) -> tuple[bool, dict | None]:
    try:
        lease_contract_object = LeaseContract.select().where(LeaseContract.id==id).get()
        return True, LeaseContract._to_dict(lease_contract_object)

    except LeaseContract.DoesNotExist:
        return False, None

def create_lease_contract(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        tenant_object = Tenant.get_by_id(_data.pop('tenant')['id'])
        apartment_object = Apartment.get_by_id(_data.pop('apartment')['id'])

        lease_contract_object = LeaseContract.create(**_data)
        lease_contract_object.tenant = tenant_object
        lease_contract_object.apartment = apartment_object

        lease_contract_object.save()

        return True, LeaseContract._to_dict(lease_contract_object)

    except Exception:
        return False, None

def update_lease_contract(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        id = _data.pop('id')

        tenant_object = _data.pop('tenant', None)
        if tenant_object is not None:
            tenant_object = Tenant.get_by_id(tenant_object['id'])

        apartment_object = _data.pop('apartment', None)
        if apartment_object is not None:
            apartment_object = Apartment.get_by_id(apartment_object['id'])

        lease_contract_object = LeaseContract.get_by_id(id)
        if tenant_object is not None:
            lease_contract_object.tenant = tenant_object
        if apartment_object is not None:
            lease_contract_object.apartment = apartment_object

        for key, value in _data.items():
            if hasattr(lease_contract_object, key):
                setattr(lease_contract_object, key, value)

        lease_contract_object.save()

        return True, LeaseContract._to_dict(lease_contract_object)

    except Exception:
        return False, None
