import random

from proxy import Proxy

class ProxyHandler (object):
    """ Handles proxy """
    proxy: Proxy
    valid_proxies: list

    def fetch(self) -> None:
        """ Fetch proxies and validate them """
        country_code = ["US", "UK"]
        
        self.proxy = Proxy(
            random.choice(country_code),
            validate_proxies=True
        )

        self.valid_proxies = self.proxy.proxies

    def get_random_proxy(self) -> dict:
        """ Returns a random proxy """
        current_proxy = random.choice(self.valid_proxies)
        proxy = {
            "http": f"http://{current_proxy[0]}:{current_proxy[1]}"
        }

        return proxy
