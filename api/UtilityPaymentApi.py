def utility_payment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'paid': True, 'amount': 0, 'month': '10', 'utility_bills': {'water': 0, 'electricity': 0, 'taxes': 0}, 'rent': {'id': 0}, 'tenant': {'last_name': 'last_name 1', 'first_name': 'first_name 1'}, 'apartment': {'name': 'name 1', 'unique_identifier': 'some identifier 1'}},
                    {'id': 1, 'paid': False, 'amount': 0, 'month': '10', 'utility_bills': {'water': 0, 'electricity': 0, 'taxes': 0}, 'rent': {'id': 1}, 'tenant': {'last_name': 'last_name 2', 'first_name': 'first_name 2'}, 'apartment': {'name': 'name 2', 'unique_identifier': 'some identifier 2'}}]
    }

def utility_payment_update(data: list) -> bool:
    return True
