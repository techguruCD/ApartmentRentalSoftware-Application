def rent_payment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'paid': True, 'amount': 100, 'month': '10', 'tenant': {'last_name': 'last_name 1', 'first_name': 'first_name 1'}, 'apartment': {'name': 'name 1', 'unique_identifier': 'some identifier 1'}},
                    {'id': 0, 'paid': False, 'amount': 200, 'month': '10', 'tenant': {'last_name': 'last_name 2', 'first_name': 'first_name 2'}, 'apartment': {'name': 'name 2', 'unique_identifier': 'some identifier 2'}}]
    }

def rent_payment_update(data: list) -> bool:
    return False
