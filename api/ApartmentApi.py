from models import (
    Apartment,
    Owner,
)
from settings import PAGINATION_PAGE_SIZE, SEARCH_DELIMETER
from tools import total_pages

def _filter(search, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(SEARCH_DELIMETER)]
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

                (Apartment.owner.first_name.contains(term)) |
                (Apartment.owner.last_name.contains(term)) |
                (Apartment.owner.phone.contains(term)) |
                (Apartment.owner.email.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)

    return queryset

def apartment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = Apartment.select()
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search = final_url.split('\n')
        page = int(page)

        queryset = _filter(search, queryset)

        pages = total_pages(len(queryset),PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}'

    else:
        queryset = _filter(search, queryset)

        if total_pages(len(queryset),PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}'

    True, {
        'next': next_page,
        'previous': previous_page,
        'results': queryset.paginate(page, PAGINATION_PAGE_SIZE)
    }

def get_apartment(id: int) -> tuple[bool, dict | None]:
    apartment_object = Apartment.get_or_none(Apartment.id==id)

    if apartment_object is not None:
        return True, apartment_object

    return False, None

def create_apartment(data: dict) -> bool:
    try:
        owner_object = Owner.get_by_id(data.pop('owner')['id'])

        apartment_object = Apartment.create(**data)
        apartment_object.owner = owner_object

        apartment_object.save()

        return True

    except Exception:
        return False

def update_apartment(data: dict) -> bool:
    try:
        id = data.pop('id')

        owner_object = Owner.get_by_id(data.pop('owner')['id'])
        
        apartment_object = Apartment.get_by_id(id)
        apartment_object.owner = owner_object

        for key, value in data.items():
            if hasattr(apartment_object, key):
                setattr(apartment_object, key, value)

        apartment_object.save()

        return True

    except Exception:
        return False
