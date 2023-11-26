from bs4 import BeautifulSoup


def get_data(content, status_code):
    parse_data = BeautifulSoup(content, 'lxml')

    title = parse_data.title.text if parse_data.title else None
    h1 = parse_data.h1.text if parse_data.h1 else None
    description = None
    meta = parse_data.find("meta", attrs={"name": "description"})
    if meta:
        description = meta.get('content', None)
    return {
        'status_code': status_code,
        'title': title,
        'h1': h1,
        'description': description,
    }
