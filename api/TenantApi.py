from models import Tenant
from settings import PAGINATION_PAGE_SIZE, SEARCH_DELIMETER
from tools import total_pages

def _filter(search, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Tenant.first_name.contains(term)) |
                (Tenant.last_name.contains(term)) |
                (Tenant.phone.contains(term)) |
                (Tenant.email.contains(term)) |
                (Tenant.parents_address.contains(term)) |
                (Tenant.parents_phone.contains(term))
            )

            combined_query = term_query if combined_query is None else combined_query | term_query

        queryset = queryset.where(combined_query)

    return queryset

def tenant_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = Tenant.select()
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

def get_tenant(id: int) -> tuple[bool, dict | None]:
    tenant_object = Tenant.get_or_none(Tenant.id==id)

    if tenant_object is not None:
        return True, tenant_object

    return False, None

def create_tenant(data: dict) -> bool:
    try:

        tenant_object = Tenant.create(**data)
        tenant_object.save()

        return True

    except Exception:
        return False

def update_tenant(data: dict) -> bool:
    try:
        id = data.pop('id')

        tenant_object = Tenant.get_by_id(id)

        for key, value in data.items():
            if hasattr(tenant_object, key):
                setattr(tenant_object, key, value)

        tenant_object.save()

        return True

    except Exception:
        return False
