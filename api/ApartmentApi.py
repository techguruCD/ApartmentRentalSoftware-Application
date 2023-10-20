def apartment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'owner': { 'first_name': 'first_name_1', 'last_name': 'last_name_1'}, 'address': 'address_1', 'name': 'namne_1', 'unique_identifier': 'unique_identifier1'},
                    {'id': 1, 'owner': { 'first_name': 'first_name_2', 'last_name': 'last_name_1'}, 'address': 'address_2', 'name': 'namne_2', 'unique_identifier': 'unique_identifier2'}]
    }

def apartment_save(data: any) -> bool:
    return False
