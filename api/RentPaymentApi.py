page = 0
def rent_payment_list(search: str = None, final_url: str = None) -> tuple[bool, dict | None]:
    global page
    page = final_url
    return True, {
        'next': page + 1,
        'previous': page -1,
        'results': []
    }