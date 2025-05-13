import pytest
import json
from ..workflows import get_results_json


pytestmark = pytest.mark.asyncio


async def test_get_results_json_success(
    mocker,
):
    json_results = {"key": "value"}
    obstore_result_mock = mocker.AsyncMock()
    obstore_result_mock.bytes_async = mocker.AsyncMock(
        return_value=json.dumps(json_results).encode("utf-8")
    )
    obstore_store_mock = mocker.MagicMock()
    obstore_store_mock.get_async = mocker.AsyncMock(return_value=obstore_result_mock)
    obstore_mock = mocker.MagicMock()
    obstore_mock.store = obstore_store_mock
    obstore_mock.store.from_url.return_value = obstore_store_mock
    mocker.patch("src.ecoscope_eda_core.workflows.results.obstore", obstore_mock)
    results_url = "gs://bucket/results/user_id/workflow_run_id/result.json"

    results = await get_results_json(results_url=results_url)

    assert results == json_results
    obstore_mock.store.from_url.assert_called_once_with(results_url)
    obstore_store_mock.get_async.assert_called_once_with("result.json")


async def test_get_results_json_raises_on_null_results(
    mocker,
):
    obstore_result_mock = mocker.AsyncMock()
    obstore_result_mock.bytes_async = mocker.AsyncMock(return_value=None)
    obstore_store_mock = mocker.MagicMock()
    obstore_store_mock.get_async = mocker.AsyncMock(return_value=obstore_result_mock)
    obstore_mock = mocker.MagicMock()
    obstore_mock.store = obstore_store_mock
    obstore_mock.store.from_url.return_value = obstore_store_mock
    mocker.patch("src.ecoscope_eda_core.workflows.results.obstore", obstore_mock)
    results_url = "gs://bucket/results/user_id/workflow_run_id/result.json"

    with pytest.raises(
        RuntimeError, match="Failed to get result json from result store."
    ):
        await get_results_json(results_url=results_url)
