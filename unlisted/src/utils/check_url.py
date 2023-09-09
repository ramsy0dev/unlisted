import re

def is_url(text: str) -> bool:
    """ Checks if a text is a url or not """
    regex = r'https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]'

    return re.match(regex, text)
