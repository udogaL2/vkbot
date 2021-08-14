import requests
from bs4 import BeautifulSoup as BS


def get_status(id: str):
    id = id.strip().lower()
    r = requests.get('https://vk.com/{0}'.format(id))

    if r.status_code == 200:
        html = BS(r.text, 'html.parser')

        status = html.find('span', class_='pp_last_activity_text').text
        name = html.find('h2', class_='op_header').text

        if status != '':
            return status.replace('   \n\n', ''), name
        else:
            return 'error'
    else:
        return 'error'
