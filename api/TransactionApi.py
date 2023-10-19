def transaction_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    return True, {
        'next': None,
        'previous': None,
        'results': [{'id': 0, 'amount': 100, 'category': 'category_1', 'transaction_type': 'income', 'description': 'description_1'},
                    {'id': 1, 'amount': 100, 'category': 'category_2', 'transaction_type': 'expense', 'description': 'description_2'}]
    }

def transaction_save(data: any) -> bool:
    return False
