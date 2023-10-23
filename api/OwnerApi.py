from models import (
    Owner,
)
from tools import total_pages
import settings


def _filter(search, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Owner.first_name.contains(term)) |
                (Owner.last_name.contains(term)) |
                (Owner.phone.contains(term)) |
                (Owner.email.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)

    return queryset.distinct()

def owner_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = Owner.select()
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
        'results': [Owner._to_dict(owner_object) for owner_object in queryset.order_by(Owner.id).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_owner(id: int) -> tuple[bool, dict | None]:
    try:
        owner_object = Owner.select().where(Owner.id==id).get()
        return True, Owner._to_dict(owner_object)

    except Owner.DoesNotExist:
        return False, None

def create_owner(data: dict) -> tuple[bool, dict | None]:
    try:

        owner_object = Owner.create(**data)
        owner_object.save()

        return True, Owner._to_dict(owner_object)

    except Exception:
        return False, None

def update_owner(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        id = _data.pop('id')

        owner_object = Owner.get_by_id(id)

        for key, value in _data.items():
            if hasattr(owner_object, key):
                setattr(owner_object, key, value)

        owner_object.save()

        return True, Owner._to_dict(owner_object)

    except Exception:
        return False, None
