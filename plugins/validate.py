# w3c validator plugin by ine (2020)
# updated 04/2022
from util import hook
from utilities import request
from bs4 import BeautifulSoup


@hook.command('w3c')
@hook.command
def validate(inp):
    """validate <url> -- Runs url through the w3c markup validator."""

    if not inp.startswith('http'):
        inp = 'https://' + inp

    url = 'https://validator.nu/?out=xhtml&doc=' + request.urlencode(inp)
    html = request.get(url)
    soup = BeautifulSoup(html, 'lxml')

    sys_errors = soup.find('li', attrs={'class': 'non-document-error'})

    if sys_errors is not None:
        return "[w3c] The validator returned an error: {}".format(sys_errors.get_text())

    results = soup.find('div', attrs={'id': 'results'})

    if results is None:
        return "[w3c] The validator didn't return anything"

    errors = len(results.find_all('li', attrs={'class': 'error'}))
    warns = len(results.find_all('li', attrs={'class': 'warning'}))
    info = len(results.find_all('li', attrs={'class': 'info'}))

    if errors == 0 and warns == 0 and info == 0:
        return "[w3c] Successfully validated with no errors"

    return "[w3c] Found {} errors, {} warnings and {} notices.".format(errors, warns, info)
