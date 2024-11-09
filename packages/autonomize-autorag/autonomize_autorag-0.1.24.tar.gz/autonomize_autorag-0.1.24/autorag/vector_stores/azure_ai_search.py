"""
Azure AI Search Vector Store Module.

This module provides a concrete implementation of the VectorStore abstract base class,
using Azure AI Search for managing collections of vectors and their associated metadata.
"""

# pylint: disable=line-too-long, duplicate-code, too-many-instance-attributes, arguments-differ

from __future__ import annotations

import uuid
from typing import Any, Dict, List, override

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
    from azure.search.documents import SearchClient, SearchIndexingBufferedSender
    from azure.search.documents.aio import SearchClient as AsyncSearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.aio import (
        SearchIndexClient as AsyncSearchIndexClient,
    )
    from azure.search.documents.indexes.models import (
        ExhaustiveKnnAlgorithmConfiguration,
        ExhaustiveKnnParameters,
        HnswAlgorithmConfiguration,
        HnswParameters,
        SearchField,
        SearchFieldDataType,
        SearchIndex,
        SimpleField,
        VectorSearch,
        VectorSearchAlgorithmKind,
        VectorSearchAlgorithmMetric,
        VectorSearchProfile,
    )
    from azure.search.documents.models import VectorizedQuery
except ImportError as err:  # pragma: no cover
    raise ImportError(
        "Unable to locate azure-search-documents package. "
        'Please install it with `pip install "autonomize-autorag[azure-ai-search]"`.'
    ) from err

from autorag.types.vector_stores import DistanceType, VectorStoreQueryResult
from autorag.vector_stores.base import VectorStore


class AzureAISearchVectorStore(VectorStore):
    """
    Azure AI Search vector store implementation.

    This class provides an interface for interacting with an Azure AI Search vector database,
    utilizing the Azure SDK for Python for different operations.

    Args:
        endpoint (str): The endpoint of your Azure AI Search service.
        api_key (str): The API key for your Azure AI Search service.

    Attributes:
        _m (int): Number of edges per node in the HNSW index graph.
                  Larger values lead to more accurate searches but require more space.
                  Default is 10.
        _ef_construct (int): Number of neighbors considered during the index building process.
                             Larger values improve accuracy but increase indexing time.
                             Default is 512.
        _ef_search (int): Size of the beam during a beam-search operation.
                          Larger values lead to more accurate search results but require more time.
                          Recommended to be the same as `_ef_construct`. Default is 512.

    Example:

    .. code-block:: python

        from autorag.vector_stores.azure_ai_search import AzureAISearchVectorStore
        from autorag.types.vector_stores import DistanceType

        client = AzureAISearchVectorStore(
            endpoint='https://<your-service-name>.search.windows.net',
            api_key='<your-api-key>'
        )

        client.create_collection(
            collection_name="test_collection",
            embedding_dimensions=768,
            distance=DistanceType.COSINE,
            metadata_fields=["content"]
        )
    """

    def __init__(self, endpoint: str, api_key: str) -> None:
        self._endpoint = endpoint
        self._credential = AzureKeyCredential(key=api_key)

        self._index_client = SearchIndexClient(
            endpoint=self._endpoint, credential=self._credential
        )
        self._async_index_client = AsyncSearchIndexClient(
            endpoint=self._endpoint, credential=self._credential
        )

        # Initialize collection parameters for HNSW
        self._m = (
            10  # Max allowed value is 10 for some reason, I wanted to set it to 16.
        )
        self._ef_construct = 512
        self._ef_search = self._ef_construct

        # Embedding field name
        # Fixed name for the field in the vector db to store embeddings.
        self._embedding_field_name = "embedding"

    def _create_fields(
        self, embedding_dimensions: int, metadata_fields: List[str]
    ) -> List[SearchField]:  # SimpleField instantiates SearchField class
        """
        Creates a list of fields for the collection, including metadata and embedding fields.

        Args:
            embedding_dimensions (int): Number of dimensions for the embeddings.
            metadata_fields (List[str]): List of metadata field names.

        Returns:
            List[SearchField]: List of SearchFields for the collection schema.
        """

        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True,
            )  # Default id field as key
        ]

        for metadata_field in metadata_fields:
            fields.append(
                SimpleField(
                    name=metadata_field,
                    type=SearchFieldDataType.String,
                    filterable=True,
                )
            )

        fields.append(
            SearchField(
                name=self._embedding_field_name,
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=embedding_dimensions,
                vector_search_profile_name="myHnswProfile",
            )
        )

        return fields

    def _create_vector_search_config(
        self, vector_distance: VectorSearchAlgorithmMetric
    ) -> VectorSearch:
        """
        Creates vector search configurations using HNSW and KNN algorithms.

        Args:
            vector_distance (VectorSearchAlgorithmMetric): The distance metric to use.

        Returns:
            VectorSearch: The vector search configuration for the collection.
        """
        return VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="myHnsw",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(
                        m=self._m,
                        ef_construction=self._ef_construct,
                        ef_search=self._ef_search,
                        metric=vector_distance,
                    ),
                ),
                ExhaustiveKnnAlgorithmConfiguration(
                    name="myExhaustiveKnn",
                    kind=VectorSearchAlgorithmKind.EXHAUSTIVE_KNN,
                    parameters=ExhaustiveKnnParameters(metric=vector_distance),
                ),
            ],
            profiles=[
                VectorSearchProfile(
                    name="myHnswProfile",
                    algorithm_configuration_name="myHnsw",
                ),
                VectorSearchProfile(
                    name="myExhaustiveKnnProfile",
                    algorithm_configuration_name="myExhaustiveKnn",
                ),
            ],
        )

    def _get_distance_metric(
        self, distance: DistanceType
    ) -> VectorSearchAlgorithmMetric:
        """
        Converts DistanceType to the corresponding `VectorSearchAlgorithmMetric`
        metric as per the configurations required by the Azure AI Search Vector Store.

        Args:
            distance (DistanceType): The type of distance metric to use.

        Returns:
            str: The matching distance metric for the Qdrant configuration.
        """
        if distance == DistanceType.EUCLIDEAN:
            return VectorSearchAlgorithmMetric.EUCLIDEAN
        if distance == DistanceType.COSINE:
            return VectorSearchAlgorithmMetric.COSINE
        return VectorSearchAlgorithmMetric.DOT_PRODUCT

    def _create_collection(  # type: ignore[override]
        self,
        collection_name: str,
        embedding_dimensions: int,
        distance: DistanceType,
        metadata_fields: List[str],
        **kwargs: Any,
    ) -> None:
        """
        Creates a new collection (index) in Azure AI Search.

        Args:
            collection_name (str): The name of the index to be created.
            embedding_dimensions (int): The number of dimensions for the embeddings.
            distance (DistanceType): The type of distance metric to use.
            metadata_fields (List[str]): A list of fields to define the schema of the collection.
            kwargs (Any): Any additional arguments to be used.
        """

        if "id" in metadata_fields:
            raise ValueError(
                "Field `id` is a reserved keyword. Please use a different identifier in metadata_fields."
            )

        vector_distance = self._get_distance_metric(distance=distance)

        fields = self._create_fields(
            embedding_dimensions=embedding_dimensions, metadata_fields=metadata_fields
        )

        vector_search = self._create_vector_search_config(
            vector_distance=vector_distance
        )

        index = SearchIndex(
            name=collection_name,
            fields=fields,
            vector_search=vector_search,
        )

        self._index_client.create_index(index, **kwargs)

    def _delete_collection(self, collection_name: str, **kwargs: Any) -> None:
        """
        Deletes an existing collection (index) in Azure AI Search.

        Args:
            collection_name (str): The name of the collection to be deleted.
            kwargs (Any): Any additional arguments to be used.
        """
        self._index_client.delete_index(collection_name, **kwargs)

    def _upsert(
        self,
        collection_name: str,
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        """
        Upserts embeddings and metadata into the collection (index).

        Args:
            collection_name (str): The name of the collection to upsert into.
            embeddings (List[List[float]]): A list of vectors to be upserted.
            metadatas (List[Dict[str, Any]]): A list of metadata dictionaries corresponding to the embeddings.
            kwargs (Any): Any additional arguments to be used.
        """

        if "id" in metadatas[0]:
            raise ValueError(
                "Field `id` is a reserved keyword. Please use a different identifier in metadata."
            )

        documents = []
        for embedding, metadata in zip(embeddings, metadatas):
            doc = {
                "id": str(uuid.uuid4()),
                self._embedding_field_name: embedding,
                **metadata,
            }
            documents.append(doc)

        try:
            # `SearchIndexingBufferedSender` is preferred when batching uploading requests
            with SearchIndexingBufferedSender(
                endpoint=self._endpoint,
                index_name=collection_name,
                credential=self._credential,
            ) as batch_client:
                batch_client.upload_documents(documents=documents, **kwargs)

                # Manually flushing any remaining documents
                batch_client.flush()
        except HttpResponseError as e:  # pragma: no cover
            raise ValueError(f"Error occurred when uploading documents: {e}") from e

    def _query(
        self,
        collection_name: str,
        query_embedding: List[float],
        top_k: int,
        metadata_filter: Dict[str, Any],
        metadata_fields: List[str],
        **kwargs: Any,
    ) -> List[VectorStoreQueryResult]:
        """
        Queries the vector store to find the top_k most similar vectors to the given query embedding.

        Args:
            collection_name (str): The name of the collection to query.
            query_embedding (List[float]): The vector to query for.
            top_k (int): The number of top similar vectors to retrieve.
            metadata_filter (Dict[str, Any]): A dictionary to filter the results based on metadata.
            metadata_fields (List[str]): A list of fields to retrieve in the results.
            kwargs (Any): Any additional arguments to be used.

        Returns:
            List[VectorStoreQueryResult]: A list of type VectorStoreQueryResult containing the search results.
        """

        filter_conditions = self._build_query_filter(metadata_filter=metadata_filter)

        search_client = SearchClient(
            endpoint=self._endpoint,
            index_name=collection_name,
            credential=self._credential,
        )

        vector = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields=self._embedding_field_name,
        )

        results = search_client.search(
            search_text="",
            vector_queries=[vector],
            filter=filter_conditions,
            select=metadata_fields,
            top=top_k,
            **kwargs,
        )
        vectorised_results = [
            VectorStoreQueryResult(
                score=result.get("@search.score", 0.0),
                metadata={
                    k: v
                    for k, v in result.items()
                    if k not in {"content", "@search.score"}
                },
            )
            for result in results
        ]
        return vectorised_results

    def _build_query_filter(self, metadata_filter: Dict[str, Any]) -> str:
        """
        Constructs a query filter for the Azure AI Search vector store based on the provided metadata.

        The function translates a dictionary of metadata filters into a string format suitable for querying
        the vector store. Each key-value pair in the metadata_filter dictionary is converted
        into a corresponding OData filter condition needed for Azure AI Search.

        Supported filter conditions:
        - Equality

        Note:
            Additional filter conditions to be added later.

        Args:
            metadata_filter (Dict[str, Any]): A dictionary to filter the results based on metadata.

        Returns:
            str: A filter string formatted for Azure AI Search's API.
        """

        field_conditions = []

        for key, value in metadata_filter.items():
            if isinstance(value, list):
                or_conditions = " or ".join([f"{key} eq '{item}'" for item in value])
                or_conditions = "(" + or_conditions + ")"
                field_conditions.append(or_conditions)
            else:
                condition = f"{key} eq '{value}'"
                field_conditions.append(condition)

        return " and ".join(field_conditions)

    def _collection_exists(self, collection_name: str) -> bool:
        """
        Checks if a collection (index) exists in Azure AI Search.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        try:
            self._index_client.get_index(collection_name)
            return True
        except ResourceNotFoundError:
            return False

    @override
    async def acreate_collection(  # type: ignore[override]
        self,
        collection_name: str,
        embedding_dimensions: int,
        distance: DistanceType,
        metadata_fields: List[str],
        **kwargs: Any,
    ) -> None:
        """
        Asynchronously creates a new collection (index) in Azure AI Search.

        Args:
            collection_name (str): The name of the index to be created.
            embedding_dimensions (int): The number of dimensions for the embeddings.
            distance (DistanceType): The type of distance metric to use.
            metadata_fields (List[str]): A list of fields to define the schema of the collection.
            kwargs (Any): Any additional arguments to be used.
        """

        if "id" in metadata_fields:
            raise ValueError(
                "Field `id` is a reserved keyword. Please use a different identifier in metadata_fields."
            )

        if await self._acollection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' already exists.")

        vector_distance = self._get_distance_metric(distance=distance)

        fields = self._create_fields(
            embedding_dimensions=embedding_dimensions, metadata_fields=metadata_fields
        )

        vector_search = self._create_vector_search_config(
            vector_distance=vector_distance
        )

        index = SearchIndex(
            name=collection_name,
            fields=fields,
            vector_search=vector_search,
        )

        await self._async_index_client.create_index(index, **kwargs)

    @override
    async def adelete_collection(self, collection_name: str, **kwargs: Any) -> None:
        """
        Asynchronously deletes an existing collection in the vector store.

        Args:
            collection_name (str): The name of the collection to be deleted.
            kwargs (Any): Any additional arguments to be used.

        Raises:
            ValueError: If the collection does not exist.
        """
        if not await self._acollection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        await self._async_index_client.delete_index(collection_name, **kwargs)

    @override
    async def aquery(
        self,
        collection_name: str,
        query_embedding: List[float],
        top_k: int,
        metadata_filter: Dict[str, Any],
        metadata_fields: List[str],
        **kwargs: Any,
    ) -> List[VectorStoreQueryResult]:
        """
        Asynchronously queries the vector store to find the top_k most similar vectors to the given query embedding.

        Args:
            collection_name (str): The name of the collection to query.
            query_embedding (List[float]): The vector to query for.
            top_k (int): The number of top similar vectors to retrieve.
            metadata_filter (Dict[str, Any]): A dictionary to filter the results based on metadata.
            metadata_fields (List[str]): A list of fields to retrieve in the results.
            kwargs (Any): Any additional arguments to be used.

        Returns:
            List[VectorStoreQueryResult]: A list of type VectorStoreQueryResult containing the embeddings and their corresponding metadatas.
        """
        if not await self._acollection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist.")

        filter_conditions = self._build_query_filter(metadata_filter=metadata_filter)

        search_client = AsyncSearchClient(
            endpoint=self._endpoint,
            index_name=collection_name,
            credential=self._credential,
        )

        vector = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields=self._embedding_field_name,
        )

        results = await search_client.search(
            search_text="",
            vector_queries=[vector],
            filter=filter_conditions,
            select=metadata_fields,
            top=top_k,
            **kwargs,
        )

        vectorised_results = [
            VectorStoreQueryResult(
                score=result.get("@search.score", 0.0),
                metadata={
                    k: v for k, v in result.items() if k not in {"@search.score"}
                },
            )
            async for result in results
        ]
        return vectorised_results

    async def _acollection_exists(self, collection_name: str) -> bool:
        """
        Asynchronously checks if a collection (index) exists in Azure AI Search.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        try:
            await self._async_index_client.get_index(collection_name)
            return True
        except ResourceNotFoundError:
            return False
