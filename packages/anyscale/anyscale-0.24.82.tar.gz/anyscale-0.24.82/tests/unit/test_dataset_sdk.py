from datetime import datetime
from unittest.mock import Mock, patch

import anyscale
from anyscale._private.anyscale_client.anyscale_client import AnyscaleClient
from anyscale._private.models.model_base import ListResponse
from anyscale.llm.dataset import Dataset


def test_sdk():
    dataset = Dataset(
        id="dataset_123",
        name="my_dataset",
        filename="test.jsonl",
        storage_uri="s3://bucket/path/to/test.jsonl",
        version=3,
        num_versions=3,
        created_at=datetime(2024, 1, 1),
        creator_id="usr_123",
        project_id="prj_123",
        cloud_id="cld_123",
        description="description",
    )

    mock_list_response = ListResponse(
        after=None,
        limit=2,
        get_next_page=Mock(
            side_effect=[
                Mock(results=[dataset], has_more=True),
                Mock(results=[dataset, dataset], has_more=False),
            ]
        ),
        cls=Dataset,
    )

    with patch.multiple(
        AnyscaleClient,
        **{
            AnyscaleClient.__init__.__name__: Mock(return_value=None),
            AnyscaleClient.upload_dataset.__name__: Mock(return_value=dataset),
            AnyscaleClient.get_dataset.__name__: Mock(return_value=dataset),
            AnyscaleClient.download_dataset.__name__: Mock(return_value="hi".encode()),
            AnyscaleClient.list_datasets.__name__: Mock(
                return_value=mock_list_response
            ),
        }
    ):
        assert anyscale.llm.dataset.upload("test.jsonl", "my_dataset") == dataset
        assert anyscale.llm.dataset.get("my_dataset") == dataset
        assert anyscale.llm.dataset.download("my_dataset").decode() == "hi"

        list_response = anyscale.llm.dataset.list(limit=2)
        assert list_response == [dataset]
        assert list_response.has_more
        # Lists up to `limit` when iterated over
        assert [dataset.id for dataset in list_response] == [dataset.id, dataset.id]
