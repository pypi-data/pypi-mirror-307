"""FPBase API client with local SQLite caching."""

from typing import Dict, List, Generator
from urllib.parse import urljoin, urlencode
import requests
from time import sleep


class FPBaseAPI:
    """A Python client for the FPBase REST API with local SQLite caching."""

    BASE_URL = "https://www.fpbase.org/api/"

    def __init__(
        self,
        rate_limit_delay: float = 0.5,
    ):
        """Initialize the API client with caching support.

        Args:
            rate_limit_delay: Delay between requests in seconds
            cache_max_age: Maximum age of cached data before refresh
        """
        self.session = requests.Session()
        self.rate_limit_delay = rate_limit_delay

    def _build_url(self, endpoint: str, params: Dict) -> str:
        """Build the complete URL with parameters for the API request."""
        if "format" not in params:
            params["format"] = "json"
        url = urljoin(self.BASE_URL, endpoint)
        return f"{url}?{urlencode(params)}"

    def _get_paginated_results(
        self, endpoint: str, params: Dict = None
    ) -> Generator[Dict, None, None]:
        """Fetch all pages of results from a paginated endpoint."""
        if params is None:
            params = {}

        next_url = self._build_url(endpoint, params)

        while next_url:
            sleep(self.rate_limit_delay)
            response = self.session.get(next_url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                results = data.get("results", [])
                next_url = data.get("next")
                for item in results:
                    yield item
            else:
                for item in data:
                    yield item
                next_url = None

    def get_all_proteins(self) -> List[Dict]:
        """Fetch all proteins,

        Returns:
            List of all protein dictionaries
        """

        return list(self._get_paginated_results("proteins/"))

    def get_proteins(self, **kwargs) -> Dict:
        """Search for proteins using various filters.

        Available fields and lookups (use double underscore between field and lookup):
            name: icontains, iendswith, istartswith, iexact
            seq: icontains, iendswith, istartswith, cdna_contains
            default_state__ex_max: around, range, lte, gte, exact
            default_state__em_max: around, range, lte, gte, exact
            default_state__lifetime: gte, lte, range, exact
            default_state__maturation: gte, lte, range, exact
            default_state__ext_coeff: gte, lte, range, exact
            default_state__qy: gte, lte, range, exact
            default_state__brightness: gte, lte, range, exact
            default_state__pka: gte, lte, range, exact
            default_state__bleach_measurements__rate: gte, lte, range, exact
            agg: exact
            genbank: iexact
            pdb: contains
            uniprot: iexact
            status: exact
            switch_type: exact, ne
            parent_organism: exact
            primary_reference__year: gte, gt, lt, lte, range, exact
            spectral_brightness: gt, lt

        Example:
            >>> api.get_proteins(name__icontains='green', default_state__qy__gte=0.7)

        Returns:
            Dictionary containing search results
        """
        sleep(self.rate_limit_delay)
        return list(self._get_paginated_results("proteins/", kwargs))

    def get_all_spectra(self) -> List[Dict]:
        """Fetch all protein spectra,

        Returns:
            List of all spectra dictionaries
        """
        return list(self._get_paginated_results("proteins/spectra/"))

    def search_by_name(self, name: str, partial_match: bool = True) -> List[Dict]:
        """Search for proteins by name.

        Args:
            name: The protein name to search for
            partial_match: If True, searches for partial matches. If False, requires exact match

        Returns:
            List of matching protein dictionaries
        """
        if partial_match:
            return self.get_proteins(name__icontains=name)
        return self.get_proteins(name__iexact=name)
