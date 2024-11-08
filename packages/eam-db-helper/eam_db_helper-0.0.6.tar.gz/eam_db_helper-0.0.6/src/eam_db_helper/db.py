"""This module contains the DatabaseHelper class,
which is used to interact with the Azure Cosmos DB database.
It provides methods to query, insert, update, and delete data from the database.
It also exposes CosmosDB's batch transaction api.

Also added is a parallelization queue which provides alternative
methods for each db method starting with `queue_` that add operations to a queue which
are evaluated in parallel when the `execute_operation_queue` method is called."""

import logging
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosBatchOperationError, CosmosHttpResponseError
from azure.core import MatchConditions
from concurrent.futures import ThreadPoolExecutor


# Exposed imports, there's nothing unused in the module but this should quiet linters
__all__ = ["DatabaseHelper", "CosmosBatchOperationError",
           "CosmosHttpResponseError", "MatchConditions"]

LOGGER = logging.getLogger("azure")
LOGGER.setLevel(logging.WARN)

MAX_THREADS = 10


class ThunkContainer:
    def __init__(self, thunk, value=None):
        self.thunk = thunk
        self.value = value
        self.has_ran = False

    def exec_func(self):
        self.value = self.thunk()
        self.has_ran = True


class DatabaseHelper:
    """This class is used to interact with the Azure Cosmos DB database."""

    def __init__(self, cosmos_metadata, connection=CosmosClient):
        self.cosmos_metadata = {
            'account_uri': cosmos_metadata['account_uri'],
            'key': cosmos_metadata['key'],
            'db_name': cosmos_metadata['db_name'],
            'container_name': cosmos_metadata['container_name']
        }
        self.client = connection(
            self.cosmos_metadata["account_uri"], self.cosmos_metadata["key"]
        )
        self.data_base = self.client.get_database_client(
            self.cosmos_metadata["db_name"])
        self.container = self.data_base.get_container_client(
            self.cosmos_metadata["container_name"])
        self.operation_queue = []

        def thunkify(func):
            def thunk(*args, **kwargs):
                thunk_reference = ThunkContainer(lambda: func(*args, **kwargs))
                self.operation_queue.append(thunk_reference)
                return thunk_reference
            return thunk

        # NOTE: This array must be kept up to date
        queueable_methods = ['get_results', 'get_result',
                             'get_column', 'delete_item', 'upsert']

        for method in queueable_methods:
            setattr(self, f"queue_{method}", thunkify(getattr(self, method)))

    def execute_operation_queue(self):
        """Execute all queued operations with multi-threading"""
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            # Submit each task to the executor
            futures = [executor.submit(task.exec_func)
                       for task in self.operation_queue]

            # Await completion
            [future.result() for future in futures]

        self.operation_queue = []

    # pylint: disable=dangerous-default-value

    def get_results(self, query: str, parameters: list = None, enable_cross_partition=False) -> list:
        """Return a list of results from the database."""
        try:
            items = self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=enable_cross_partition
            )
            return list(items)
        except ValueError as err:
            LOGGER.error("Error getting results: %s", err)
            return []

    # pylint: disable=dangerous-default-value
    def get_result(self, query: str, parameters: list = None, enable_cross_partition=False) -> dict:
        """Return a single result from the database."""
        try:
            items = self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=enable_cross_partition
            )
            items_list = list(items)

            if items_list:
                return items_list[0]

            return {}
        except (ValueError, IndexError, TypeError) as err:
            LOGGER.error("Error getting result: %s", err)
            return {}

    def get_column(self, column_name: str, query: str, parameters: list = None) -> list:
        """Return a list of a single column from the query results."""
        try:
            items = self.container.query_items(
                query=query, parameters=parameters)
            return [item[column_name] for item in items]
        except IndexError as err:
            LOGGER.error("Error getting column: %s", err)
            return []

    def delete_item(self, item_id: str, primary_key: str) -> None:
        """Delete an item from the database by id and partition key."""
        self.container.delete_item(item_id, partition_key=primary_key)

    def upsert(self, item: dict) -> dict:
        """Upsert an item into the database."""
        return self.container.upsert_item(item)

    def execute_item_batch(self, *args, **kwargs):
        """
        This is a passthrough method for the CosmosDB transactional
        batch API. Use this function to execute a series of transactions
        together in an ACID manner. All transactions must occur within
        the SAME partition key.

        Executes the transactional batch for the specified partition key.

        :param batch_operations: The batch of operations to be executed.
        :type batch_operations: List[Tuple[Any]]
        :param partition_key: The partition key value of the batch operations.
        :type partition_key: Union[str, int, float, bool, List[Union[str, int, float, bool]]]
        :keyword str pre_trigger_include: trigger id to be used as pre operation trigger.
        :keyword str post_trigger_include: trigger id to be used as post operation trigger.
        :keyword str session_token: Token for use with Session consistency.
        :keyword str etag: An ETag value, or the wildcard character (*). Used to check if the resource
            has changed, and act according to the condition specified by the `match_condition` parameter.
        :keyword ~eam_db_helper.db.MatchConditions match_condition: The match condition to use upon the etag.
        :keyword Literal["High", "Low"] priority: Priority based execution allows users to set a priority for each
            request. Once the user has reached their provisioned throughput, low priority requests are throttled
            before high priority requests start getting throttled. Feature must first be enabled at the account level.
        :keyword Callable response_hook: A callable invoked with the response metadata.
        :returns: A list representing the item after the batch operations went through.
        :raises ~eam_db_helper.db.CosmosHttpResponseError: The batch failed to execute.
        :raises ~eam_db_helper.db.CosmosBatchOperationError: A transactional batch operation failed in the batch.
        :rtype: List[Dict[str, Any]]
        """
        return self.container.execute_item_batch(*args, **kwargs)
