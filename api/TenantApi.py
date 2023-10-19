def tenant_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'status': 'active', 'phone': '123456789', 'last_name': 'last_name 1', 'first_name': 'first_name 1'},
                    {'id': 0, 'status': 'inactive', 'phone': '987654321', 'last_name': 'last_name 2', 'first_name': 'first_name 2'}]
    }

def tenant_save(data: any) -> bool:
    return False
