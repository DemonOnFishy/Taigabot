# urban dictionary plugin by ine (2020)
# checked 04/2022
from util import hook
from utilities import request, formatting

base_url = 'https://api.urbandictionary.com/v0/define?term='


def clean_text(text):
    return formatting.compress_whitespace(text.replace('[', '').replace(']', ''))


def search(input):
    json = request.get_json(base_url + request.urlencode(input))

    if json is None or "error" in json or "errors" in json:
        return ["the server fucked up"]

    data = []
    for item in json['list']:
        definition = item['definition']
        word = item['word']
        example = item['example']
        votes_up = item['thumbs_up']
        votes_down = item['thumbs_down']

        output = '\x02' + word + '\x02 '

        try:
            votes = int(votes_up) - int(votes_down)
            if votes > 0:
                votes = '+' + str(votes)
        except:
            votes = 0

        if votes != 0:
            output = output + '(' + str(votes) + ') '

        output = output + clean_text(definition)

        if example:
            output = output + ' \x02Example:\x02 ' + clean_text(example)

        data.append(output)

    return data


@hook.command('u')
@hook.command('ud')
@hook.command('nig')
@hook.command('ebonics')
@hook.command
def urban(inp):
    "urban <phrase> [entry] -- Looks up <phrase> on urbandictionary.com."

    inp_val = inp.strip()
    inp_count = 1

    try:
        inp_rev = inp_val[::-1]
        inp_count, rest = inp_rev.split(' ', 1)

        inp_val = rest[::-1]
        inp_count = int(inp_count[::-1])
    except:
        inp_val = inp.strip()
        inp_count = 1

    if inp_count < 1:
        return '[ud] Results start at 1'

    results = search(inp_val)
    results_len = len(results)

    if inp_count > results_len:
        return '[ud] this entry only has {} results'.format(results_len)

    try:
        if results_len == 1:
            return u'[ud] {}'.format(results[inp_count-1])
        else:
            return u'[ud {}/{}] {}'.format(inp_count, results_len, results[inp_count-1])
    except IndexError:
        return '[ud] Not found'
