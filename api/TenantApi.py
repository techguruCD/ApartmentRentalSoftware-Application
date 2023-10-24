from models import (
    Tenant,
    LeaseContract,
    TENANT_STATUS
)
from tools import total_pages
from peewee import JOIN
import datetime
import settings


def _filter(search, status, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
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

    today = datetime.date.today()

    if status == TENANT_STATUS.active:
        subquery = LeaseContract.select().where(
            (LeaseContract.tenant == Tenant.id) & 
            (LeaseContract.end_date >= today)
        )
        queryset = queryset.join(LeaseContract, JOIN.INNER, on=(Tenant.id == LeaseContract.tenant)).where(
            LeaseContract.id << subquery
        )
    elif status == TENANT_STATUS.inactive:
        queryset = queryset.join(LeaseContract, JOIN.LEFT_OUTER ,on=(Tenant.id == LeaseContract.tenant)).where(
            (LeaseContract.id.is_null()) |
            (LeaseContract.end_date < today)
        )

    return queryset.distinct()

def tenant_list(search: str = None, status: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    queryset = Tenant.select()
    page, previous_page, current_page, next_page = 1, None, final_url, None

    if final_url is not None:
        page, search, status = final_url.split('\n')
        page = int(page)

        queryset = _filter(search, status, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{status}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{status}'

    else:
        queryset = _filter(search, status, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{status}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'current': current_page,
        'results': [Tenant._to_dict(tenant_object) for tenant_object in queryset.order_by(Tenant.id).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_tenant(id: int) -> tuple[bool, dict | None]:
    try:
        tenant_object = Tenant.select().where(Tenant.id==id).get()
        return True, Tenant._to_dict(tenant_object)

    except Tenant.DoesNotExist:
        return False, None

def create_tenant(data: dict) -> tuple[bool, dict | None]:
    try:

        tenant_object = Tenant.create(**data)
        tenant_object.save()

        return True, Tenant._to_dict(tenant_object)

    except Exception:
        return False, None

def update_tenant(data: dict) -> tuple[bool, dict | None]:
    try:
        _data = data.copy()
        id = _data.pop('id')

        tenant_object = Tenant.get_by_id(id)

        for key, value in _data.items():
            if hasattr(tenant_object, key):
                setattr(tenant_object, key, value)

        tenant_object.save()

        return True, Tenant._to_dict(tenant_object)

    except Exception:
        return False, None
