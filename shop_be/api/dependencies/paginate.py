def paginate(data: dict) -> dict:
    return {
        'data': data,
        'total': 10,
        'current_page': 1,
        'count': 1,
        'last_page': 1,
        'firstItem': 10,
        'per_page': 10,
        'first_page_url': '',
        'last_page_url': '',
        'next_page_url': '',
        'prev_page_url': '',
    }
