"""This module is used to test the DatabaseHelper class."""

from unittest import TestCase

from src.eam_db_helper.db import DatabaseHelper


# pylint: disable=unused-argument
class CosmosClientMock:
    """This class is used to mock the CosmosClient class."""

    def __init__(self, uri, key):
        self.results = []

    def get_database_client(self, data_base: str):
        """Return the database client."""
        return self

    def get_container_client(self, container: str):
        """Return the container client."""
        return self

    def query_items(
            self, query: str,
            parameters: list = None,
            enable_cross_partition_query: bool = False):
        """Return the query results."""
        results = self.results
        self.results = []

        return results

    def upsert_item(self, body):
        """Add an item to the results."""
        self.results.append(body)
        return body

    def delete_item(self, item_id, partition_key):
        """Delete an item from the results."""
        self.results = None

    def execute_item_batch(self, *args, **kwargs):
        """Return the batch."""
        results = self.results
        self.results = []
        return results


DATABASE = DatabaseHelper(
    {
        'account_uri': 'test_uri',
        'key': 'test_key',
        'db_name': 'test_database',
        'container_name': 'test_container'
    },
    CosmosClientMock
)


class TestDatabaseHelper(TestCase):
    """This class is used to test the DatabaseHelper class."""

    def test_get_results(self):
        """Test the get_results method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        results = DATABASE.get_results('SELECT * FROM c')
        self.assertEqual(results, [{'id': '1'}, {'id': '2'}])

    def test_get_result(self):
        """Test the get_result method."""
        DATABASE.client.results = [{'id': '1'}]
        result = DATABASE.get_result('SELECT * FROM c')
        self.assertEqual(result, {'id': '1'})

    def test_get_column(self):
        """Test the get_column method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        column = DATABASE.get_column('id', 'SELECT * FROM c')
        self.assertEqual(column, ['1', '2'])

    def test_delete_item(self):
        """Test the delete_item method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        DATABASE.delete_item('1', '2')
        self.assertEqual(DATABASE.client.results, None)

    def test_upsert(self):
        """Test the upsert method."""
        DATABASE.client.results = []
        DATABASE.upsert({'id': '1', 'partition_key': '2'})
        self.assertEqual(DATABASE.client.results, [
                         {'id': '1', 'partition_key': '2'}])

    def test_batch_transactions(self):
        """Test the execute_item_batch method."""
        DATABASE.client.results = [
            True,
            {
                "id": "68719519884",
                "category": "road-bikes",
                "name": "Tronosuros Tire",
                "productId": "68719520766"
            },
            True,
            True
        ]

        create_demo_item = {
            "id": "68719520766",
            "category": "road-bikes",
            "name": "Chropen Road Bike"
        }

        upsert_demo_item = {
            "id": "68719519885",
            "category": "road-bikes",
            "name": "Tronosuros Tire Upserted",
            "productId": "68719520768"
        }

        replace_demo_item = {
            "id": "68719519886",
            "category": "road-bikes",
            "name": "Tronosuros Tire replaced",
            "productId": "68719520769"
        }

        create_item_operation = ("create", (create_demo_item,), {})
        read_item_operation = ("read", ("68719519884",), {})
        upsert_item_operation = ("upsert", (upsert_demo_item,), {})
        replace_item_operation = (
            "replace", ("68719519886", replace_demo_item), {})

        batch_operations = [
            create_item_operation,
            read_item_operation,
            upsert_item_operation,
            replace_item_operation,
        ]

        results = DATABASE.execute_item_batch(
            batch_operations=batch_operations)
        self.assertEqual(results, [
            True,
            {
                "id": "68719519884",
                "category": "road-bikes",
                "name": "Tronosuros Tire",
                "productId": "68719520766"
            },
            True,
            True
        ])

    def test_parallel_get_results(self):
        """Test the queue_get_results method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        results = DATABASE.queue_get_results('SELECT * FROM c')
        DATABASE.execute_operation_queue()
        self.assertEqual(results.value, [{'id': '1'}, {'id': '2'}])

    def test_parallel_get_result(self):
        """Test the queue_get_result method."""
        DATABASE.client.results = [{'id': '1'}]
        result = DATABASE.queue_get_result('SELECT * FROM c')
        DATABASE.execute_operation_queue()
        self.assertEqual(result.value, {'id': '1'})

    def test_parallel_get_column(self):
        """Test the queue_get_column method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        column = DATABASE.queue_get_column('id', 'SELECT * FROM c')
        DATABASE.execute_operation_queue()
        self.assertEqual(column.value, ['1', '2'])

    def test_parallel_delete_item(self):
        """Test the queue_delete_item method."""
        DATABASE.client.results = [{'id': '1'}, {'id': '2'}]
        DATABASE.queue_delete_item('1', '2')
        DATABASE.execute_operation_queue()
        self.assertEqual(DATABASE.client.results, None)

    def test_parallel_upsert(self):
        """Test the queue_upsert method."""
        DATABASE.client.results = []
        d = DATABASE.queue_upsert({'id': '1', 'partition_key': '2'})
        DATABASE.execute_operation_queue()
        self.assertEqual(DATABASE.client.results, [
                         {'id': '1', 'partition_key': '2'}])
