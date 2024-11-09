from typing import Optional, Dict, Union, List

from pinecone_plugin_interface import PineconePlugin

from .db_data.core.client.api.vector_operations_api import VectorOperationsApi
from .db_data.core.client import ApiClient
from .db_data.core.client.models import (
    SearchRecordsRequest,
    SearchRecordsRequestQuery,
    SearchRecordsResponse,
)
from .models import SearchRequest
from .version import API_VERSION


class SearchRecords(PineconePlugin):
    """
    The `SearchRecords` class adds functionality to the Pinecone SDK to allow searching for records.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required
    """

    def __init__(self, config, openapi_client_builder):
        self.config = config
        self.db_data_api = openapi_client_builder(
            ApiClient, VectorOperationsApi, API_VERSION
        )

    def __call__(
        self,
        namespace: str,
        query: Union[Dict, SearchRequest],
        fields: Optional[List[str]] = ["*"],  # Default to returning all fields
    ) -> SearchRecordsResponse:
        """
        Search for records.

        This operation converts a query to a vector embedding and then searches a namespace

        :param namespace: The namespace in the index to search.
        :type namespace: str, required
        :param inputs: The input data to search for.
        :type inputs: Dict[str, Any], required
        :param top_k: The number of records to return.
        :type top_k: int, required
        :param fields: The fields to return in the search results.
        :type fields: Optional[List[str]], optional
        :param filter: The filter to apply to the search.
        :type filter: Optional[Dict[str, Any]], optional
        :return: The records that match the search.
        :rtype: RecordModel
        """

        if not namespace:
            raise Exception("Namespace is required when searching records")

        query_dict = query.as_dict() if isinstance(query, SearchRequest) else query
        request = SearchRecordsRequest(
            query=SearchRecordsRequestQuery(**query_dict),
            fields=fields,
        )

        return self.db_data_api.search_records_namespace(namespace, request)
