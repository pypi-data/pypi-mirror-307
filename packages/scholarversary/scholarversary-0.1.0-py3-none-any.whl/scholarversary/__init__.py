import time
import httpx
from typing import Literal
import datetime


def sluggable(func):
    """
    A decorator that adds an extra option to the function to return the slug.

    Argumentss:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    Example:
        @sluggable
        def my_function():
            # function implementation
            pass

        result = my_function(return_slug=True)
        # returns the slug of the response

    """

    def wrapper(*args, **kwargs):
        return_slug = kwargs.pop("return_slug", False)
        response = func(*args, **kwargs)
        if return_slug:
            return OpenAlex.get_slug_from_uri(response)
        return response

    return wrapper


def depaginated(func):
    """
    A decorator that handles pagination for OpenAlex API requests.

    Arguments:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    """

    # Automatically handle pagination. Meta looks like this in each req:
    #     {'meta': {'count': 48,
    # 'db_response_time_ms': 24,
    # 'page': 1,
    # 'per_page': 25,
    # 'groups_count': None},
    # 'results': [{'id': 'https://openalex.org/works/1', ...
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        results = response["results"]
        page = 1
        while len(results) < response["meta"]["count"]:
            page += 1
            response = func(*args, **kwargs, page=page)
            results.extend(response["results"])
        return results

    return wrapper


class OpenAlex:
    """
    A class for interacting with the OpenAlex API.

    Args:
        base_url (str, optional): The base URL of the OpenAlex API. Defaults to "https://api.openalex.org/".

    Attributes:
        base_url (str): The base URL of the OpenAlex API.
        client (httpx.Client): An HTTP client for making requests to the API.

    """

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the class.

        Args:
            base_url (str, optional): The base URL for the API. Defaults to "https://api.openalex.org/".

        """
        self.base_url = kwargs.get("base_url", "https://api.openalex.org/")
        self.client = httpx.Client()

    def _get(self, endpoint, retry_429: bool | int = 5, **kwargs):
        url = self.base_url + endpoint
        response = self.client.get(url, **kwargs)
        if response.status_code == 429 and retry_429:
            time.sleep(1)
            return self._get(endpoint, retry_429 - 1, **kwargs)
        response.raise_for_status()
        return response.json()

    def _get_noun(self, noun: Literal["works", "authors"], **kwargs):
        filter_params = kwargs.get("filter", {})
        filter_string = (
            "filter=" + ",".join([f"{k}:{v}" for k, v in filter_params.items()])
            if filter_params
            else ""
        )
        page = kwargs.get("page", 1)
        return self._get(f"{noun}?{filter_string}&page={page}")

    @depaginated
    def get_works(self, **kwargs):
        return self._get_noun("works", **kwargs)

    @depaginated
    def get_authors(self, **kwargs):
        return self._get_noun("authors", **kwargs)

    @depaginated
    def get_citers(self, work_slug: str, **kwargs):
        page = kwargs.get("page", 1)
        return self._get(f"works?filter=cites:{work_slug}&page={page}")

    @sluggable
    def get_author_uri_by_search(self, search: str):
        response_data = self._get(f"authors?search={search}")
        if "results" in response_data:
            return response_data["results"][0]["id"]
        else:
            raise ValueError("No results found for search " + search)

    @staticmethod
    def get_slug_from_uri(uri: str):
        return uri.split("/")[-1]

    def get_author_institutions(self, author_id: str):
        response = self._get(f"people/{author_id}")
        return response.get("affiliations")


def slug_from_url(url):
    return url.split("/")[-1]


Work = dict
Year = int
Count = int
Slug = str


class Scholarversary:

    def __init__(self, **kwargs):
        self.openalex = OpenAlex(**kwargs)

    def get_author_works(self, author_search: str) -> list[Work]:
        """
        Get all the Works by an author, searching by name.

        Arguments:
            author_search (str): The name of the author to search for.

        Returns:
            list[Work]: A list of works by the author.

        """
        author_uri = self.openalex.get_author_uri_by_search(
            author_search, return_slug=True
        )
        works = self.openalex.get_works(filter={"authorships.author.id": author_uri})
        return works

    def get_work_cites(self, work_slug: str) -> list[Work]:
        """
        Get all the Works that cite a given work.

        Arguments:
            work_slug (str): The slug of the work to search for.

        Returns:
            list[Work]: A list of works that cite the given work.

        """
        cites = self.openalex.get_citers(work_slug)
        return cites

    def get_work_cites_by_year(self, work_slug: str) -> dict[Year, Count]:
        """
        Get all the Works that cite a given work, grouped by year.

        Arguments:
            work_slug (str): The slug of the work to search for.

        Returns:
            dict: A dictionary of works that cite the given work, grouped by year.

        """
        cites = self.get_work_cites(work_slug)
        cites_by_year = {}
        for cite in cites:
            year = cite["publication_year"]
            if year in cites_by_year:
                cites_by_year[year] += 1
            else:
                cites_by_year[year] = 1
        return cites_by_year

    def get_total_author_cites(self, author_search: str) -> Count:
        """
        Get the total number of citations of all works by an author.

        Arguments:
            author_search (str): The name of the author to search for.

        Returns:
            int: The total number of citations of all works by the author.

        """
        works = self.get_author_works(author_search)
        total_cites = 0
        for work in works:
            cites = self.get_work_cites(slug_from_url(work["id"]))
            total_cites += len(cites)
        return total_cites

    def get_total_author_cites_by_year(self, author_search: str) -> dict[Year, Count]:
        """
        Get the total number of citations of all works by an author, grouped by year.

        Arguments:
            author_search (str): The name of the author to search for.

        Returns:
            dict: A dictionary of the total number of citations of all works by the author, grouped by year.

        """
        works = self.get_author_works(author_search)
        total_cites_by_year = {}
        for work in works:
            cites = self.get_work_cites_by_year(slug_from_url(work["id"]))
            for year, count in cites.items():
                if year in total_cites_by_year:
                    total_cites_by_year[year] += count
                else:
                    total_cites_by_year[year] = count
        return total_cites_by_year

    def get_author_work_cites_by_year(
        self, author_search: str, index_by: str = "id"
    ) -> dict[Slug, dict[Year, Count]]:
        """
        Get the number of citations of each work by an author, grouped by year.

        Arguments:
            author_search (str): The name of the author to search for.
            index_by (str): The key to index the dictionary by. Defaults to "id" but can also be "title".

        Returns:
            dict: A dictionary of each work by the author, keying the number of citations grouped by year.

        """
        works = self.get_author_works(author_search)
        cites_by_work = {}
        for work in works:
            cites = self.get_work_cites_by_year(slug_from_url(work["id"]))
            cites_by_work[work[index_by]] = cites
        return cites_by_work

    def get_author_citation_milestone_dates(
        self, author_search: str, milestones: list[int] | None = None
    ) -> dict[Count, datetime.date]:
        """
        Get the dates of the author's citation milestones.

        Arguments:
            author_search (str): The name of the author to search for.
            milestones (list[int]|None): The citation milestones to search for. Defaults to [1, 10, 50, 100, 200, 500, 1000].

        Returns:
            dict: A dictionary of the dates of the author's citation milestones.

        """
        if milestones is None:
            milestones = [1, 10, 50, 100, 200, 500, 1000]
        # Get all the author's works
        works = self.get_author_works(author_search)
        # Get the number of citations of each work
        all_cites: list[Work] = []
        for work in works:
            cites = self.get_work_cites(slug_from_url(work["id"]))
            all_cites.extend(cites)

        # Sort the citations by date
        all_cites.sort(key=lambda x: x["publication_date"])

        # For each milestone, get the first N citations and return the date of
        # the Nth citation
        milestone_dates = {}
        for milestone in milestones:
            milestone_date = None
            milestone_cites = all_cites[:milestone]
            if len(milestone_cites) >= milestone:
                milestone_date = milestone_cites[milestone - 1]["publication_date"]
                milestone_dates[milestone] = milestone_date
        return milestone_dates
