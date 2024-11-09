from typing import NamedTuple, Optional, Dict, Any, List


class SearchRequest(NamedTuple):
    """
    SearchRequest represents the query when searching within a specific namespace.
    """

    inputs: Dict[str, Any]
    """
    The input data to search with.
    Required.
    """

    top_k: int
    """
    The number of results to return with each search.
    Required.
    """

    filter: Optional[Dict[str, Any]] = {}
    """
    The filter to apply to the search.
    Optional.
    """

    def as_dict(self):
        """
        Returns the SearchRequest as a dictionary.
        """
        return self._asdict()
