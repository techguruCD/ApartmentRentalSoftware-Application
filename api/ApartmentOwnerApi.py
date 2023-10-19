def apartment_owner_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'apartment': { 'name': 'apartment_name_1'}, 'phone': '123456789', 'last_name': 'last_name 1', 'first_name': 'first_name 1'},
                    {'id': 0, 'apartment': { 'name', 'apartment_name_2'}, 'phone': '987654321', 'last_name': 'last_name 2', 'first_name': 'first_name 2'}]
    }

def apartment_owner_save(data: any) -> bool:
    return False
