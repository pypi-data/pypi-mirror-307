import requests

class ProxyLists:
    @staticmethod
    def get_proxyscrape(protocol: str = 'http', timeout: int = 1000, country: str = 'all', ssl: str = 'all', anonymity: str = 'all'):
        """
        Retrieve proxies from the Proxyscrape API.

        Args:
            protocol (str): The protocol of proxies to retrieve (e.g., 'http', 'https', 'socks4', 'socks5').
            timeout (int): The maximum timeout for the proxies in milliseconds.
            country (str): The country code of the proxies to retrieve ('all' for any country).
            ssl (str): SSL support required ('all', 'yes', or 'no').
            anonymity (str): Anonymity level of the proxies ('all', 'transparent', 'anonymous', 'elite').

        Returns:
            List[Dict[str, str]]: A list of proxies in the form {protocol: ip}.
        """
        # Construct the URL for the Proxyscrape API request
        url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country={country}&ssl={ssl}&anonymity={anonymity}"
        try:
            # Make a GET request to the Proxyscrape API
            response = requests.get(url, timeout=10)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            # Parse the response text into a list of proxies
            return [{protocol: ip.strip()} for ip in response.text.splitlines() if ip.strip()]
        except requests.RequestException as e:
            # Print an error message if there is an exception during the request
            print(f"Error fetching proxies: {e}")
            # Return an empty list if an error occurs
            return []
