from models import (
    Apartment,
    Owner,
)
from tools import total_pages
from peewee import JOIN
import settings


def _filter(search, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Apartment.unique_identifier.contains(term)) |
                (Apartment.name.contains(term)) |
                (Apartment.address.contains(term)) |
                (Apartment.city.contains(term)) |
                (Apartment.rooms.contains(term)) |
                (Apartment.apartment_area.contains(term)) |
                (Apartment.floor.contains(term)) |
                (Apartment.beds.contains(term)) |

                (Owner.first_name.contains(term)) |
                (Owner.last_name.contains(term)) |
                (Owner.phone.contains(term)) |
                (Owner.email.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)

    return queryset.distinct()

def apartment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = Apartment.select().join(Owner, JOIN.LEFT_OUTER, on=(Apartment.owner == Owner.id))
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search = final_url.split('\n')
        page = int(page)

        queryset = _filter(search, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}'

    else:
        queryset = _filter(search, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'results': [Apartment._to_dict(apartment_object) for apartment_object in queryset.order_by(Apartment.id).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_apartment(id: int) -> tuple[bool, dict | None]:
    try:
        apartment_object = Apartment.select(Apartment).where(Apartment.id==id).get()
        
        return True, Apartment._to_dict(apartment_object)

    except Apartment.DoesNotExist:
        return False, None

def create_apartment(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        owner_object = Owner.get_by_id(_data.pop('owner')['id'])

        apartment_object = Apartment.create(**_data)
        apartment_object.owner = owner_object

        apartment_object.save()

        return True, Apartment._to_dict(apartment_object)

    except Exception:
        return False, None

def update_apartment(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        id = _data.pop('id')

        owner_object = _data.pop('owner', None)
        if owner_object is not None:    
            owner_object = Owner.get_by_id(owner_object['id'])
        
        apartment_object = Apartment.get_by_id(id)
        if owner_object is not None:    
            apartment_object.owner = owner_object

        for key, value in _data.items():
            if hasattr(apartment_object, key):
                setattr(apartment_object, key, value)

        apartment_object.save()

        return True, Apartment._to_dict(apartment_object)

    except Exception:
        return False, None
