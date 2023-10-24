from models import (
    Reminder,
    Task,
    Tenant,
    Owner,
    Apartment,
    LeaseContract,
    NamedDate,
    CellAction,
)
from tools import total_pages
from peewee import JOIN
import datetime
import settings


def _reminder_filter(search, active, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Reminder.date.contains(term)) |
                (Reminder.text.contains(term)) |
                (Reminder.email_subject.contains(term)) |

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
    
    if active == True:
        queryset = queryset.where(NamedDate.date >= datetime.datetime.utcnow())

    return queryset.distinct()

def _task_filter(search, active, queryset):
    if search not in (None, 'None'):
        search_terms = [term.strip() for term in search.split(settings.SEARCH_DELIMETER)]
        combined_query = None

        for term in search_terms:
            term_query = (
                (Task.date.contains(term)) |
                (Task.text.contains(term)) |
                (Task.email_subject.contains(term)) |
                (Task.note.contains(term)) |

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
    
    if active == True:
        queryset = queryset.where(NamedDate.date >= datetime.datetime.utcnow())

    return queryset.distinct()


def _add_dates(object, dates):
    for named_date in object.dates:
        named_date.delete_instance()
    object.dates.clear()

    for date in dates:
        date.pop('id', None)
        date_object = NamedDate.create(**date)
        object.dates.add(date_object)

def _add_actions(object, actions):
    for cell_action in object.actions:
        cell_action.delete_instance()
    object.actions.clear()

    for action in actions:
        action.pop('id', None)
        action_object = CellAction.create(**action)
        object.actions.add(action_object)


def reminder_list(search: str = None, active: bool = None, final_url: str = None) -> tuple[bool, dict | None]:
    ReminderNamedDate = Reminder.dates.get_through_model()
    queryset = (Reminder.select()
                .join(LeaseContract, JOIN.LEFT_OUTER, on=(Reminder.lease_contract == LeaseContract.id))
                .join(ReminderNamedDate, JOIN.LEFT_OUTER, on=(Reminder.id == ReminderNamedDate.reminder_id))
                .join(Apartment, JOIN.LEFT_OUTER, on=(LeaseContract.apartment == Apartment.id))
                .join(Tenant, JOIN.LEFT_OUTER, on=(LeaseContract.tenant == Tenant.id))
                .join(Owner, JOIN.LEFT_OUTER, on=(Apartment.owner == Owner.id))
                .join(NamedDate, JOIN.LEFT_OUTER, on=(ReminderNamedDate.nameddate_id == NamedDate.id))
    )
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search, active = final_url.split('\n')
        page = int(page)

        if active != 'None':
            active = bool(active)

        queryset = _reminder_filter(search, active, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{active}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{active}'

    else:
        queryset = _reminder_filter(search, active, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{active}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'results': [Reminder._to_dict(reminder_object) for reminder_object in queryset.order_by(Reminder.date).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_reminder(id: int) -> tuple[bool, dict | None]:
    try:
        reminder_object = Reminder.select().where(Reminder.id==id).get()
        return True, Reminder._to_dict(reminder_object)
    
    except Reminder.DoesNotExist:
        return False, None

def create_reminder(data: dict) -> bool:
    try:
        _data = data.copy()
        lease_contract_object = LeaseContract.get_by_id(_data.pop('lease_contract')['id'])
        dates = _data.pop('dates', [])

        reminder_object = Reminder.create(**_data)
        reminder_object.lease_contract = lease_contract_object
        
        _add_dates(reminder_object, dates)

        reminder_object.save()

        return True, Reminder._to_dict(reminder_object)

    except Exception:
        return False, None

def update_reminder(data: dict) -> bool:
    try:
        _data = data.copy()
        id = _data.pop('id')

        lease_contract_object = _data.pop('lease_contract', None)
        if lease_contract_object is not None:
            lease_contract_object = LeaseContract.get_by_id(lease_contract_object['id'])

        dates = _data.pop('dates', None)

        reminder_object = Reminder.get_by_id(id)
        if lease_contract_object is not None:
            reminder_object.lease_contract = lease_contract_object

        if dates is not None:
            _add_dates(reminder_object, dates)

        for key, value in _data.items():
            if hasattr(reminder_object, key):
                setattr(reminder_object, key, value)

        reminder_object.save()

        return True, Reminder._to_dict(reminder_object)

    except Exception:
        return False, None


def task_list(search: str = None, active: bool = None, final_url: str = None) -> tuple[bool, dict | None]:
    TaskNamedDate = Task.dates.get_through_model()
    TaskCellAction = Task.actions.get_through_model()
    queryset = (Task.select()
                .join(LeaseContract, JOIN.LEFT_OUTER, on=(Task.lease_contract == LeaseContract.id))
                .join(TaskNamedDate, JOIN.LEFT_OUTER, on=(Task.id == TaskNamedDate.task_id))
                .join(TaskCellAction, JOIN.LEFT_OUTER, on=(Task.id == TaskCellAction.task_id))
                .join(Apartment, JOIN.LEFT_OUTER, on=(LeaseContract.apartment == Apartment.id))
                .join(Tenant, JOIN.LEFT_OUTER, on=(LeaseContract.tenant == Tenant.id))
                .join(Owner, JOIN.LEFT_OUTER, on=(Apartment.owner == Owner.id))
                .join(NamedDate, JOIN.LEFT_OUTER, on=(TaskNamedDate.nameddate_id == NamedDate.id))
                .join(CellAction, JOIN.LEFT_OUTER, on=(TaskCellAction.cellaction_id == CellAction.id))
    )
    page, previous_page, next_page = 1, None, None

    if final_url is not None:
        page, search, active = final_url.split('\n')
        page = int(page)

        if active != 'None':
            active = bool(active)

        queryset = _task_filter(search, active, queryset)

        pages = total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE)

        if pages > 1 and page > 1:
            previous_page = f'{page - 1}\n{search}\n{active}'

        if pages > 1 and page < pages:
            next_page = f'{page + 1}\n{search}\n{active}'

    else:
        queryset = _task_filter(search, active, queryset)

        if total_pages(queryset.count(), settings.PAGINATION_PAGE_SIZE) > 1:
            next_page = f'2\n{search}\n{active}'

    return True, {
        'next': next_page,
        'previous': previous_page,
        'results': [Task._to_dict(task_object) for task_object in queryset.order_by(Task.date).paginate(page, settings.PAGINATION_PAGE_SIZE)]
    }

def get_task(id: int) -> tuple[bool, dict | None]:
    try:
        task_object = Task.select().where(Task.id==id).get()
        return True, Task._to_dict(task_object)
    
    except Task.DoesNotExist:
        return False, None

def create_task(data: dict) -> bool:
    try:
        _data = data.copy()
        lease_contract_object = LeaseContract.get_by_id(_data.pop('lease_contract')['id'])
        dates = _data.pop('dates', [])
        actions = _data.pop('actions', [])

        task_object = Task.create(**_data)
        task_object.lease_contract = lease_contract_object
        
        _add_dates(task_object, dates)
        _add_actions(task_object, actions)

        task_object.save()

        return True, Task._to_dict(task_object)

    except Exception:
        return False, None

def update_task(data: dict) -> bool:
    try:
        _data = data.copy()
        id = _data.pop('id')

        lease_contract_object = _data.pop('lease_contract', None)
        if lease_contract_object is not None:
            lease_contract_object = LeaseContract.get_by_id(lease_contract_object['id'])

        dates = _data.pop('dates', None)
        actions = _data.pop('actions', None)

        task_object = Task.get_by_id(id)
        if lease_contract_object is not None:
            task_object.lease_contract = lease_contract_object
        
        if dates is not None:
            _add_dates(task_object, dates)
        if actions is not None:
            _add_actions(task_object, actions)

        for key, value in _data.items():
            if hasattr(task_object, key):
                setattr(task_object, key, value)

        task_object.save()

        return True, Task._to_dict(task_object)

    except Exception:
        return False, None
