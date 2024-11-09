import os
import warnings
from uuid import uuid4

import pytest
import requests

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    async_agent_query,
    async_send_feedback,
    check_dois,
    get_bibliography,
    get_query_request,
    upload_file,
    upload_paper,
)


def test_bad_bibliography():
    with pytest.raises(requests.exceptions.HTTPError):
        get_bibliography("bad-bibliography")


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
def test_agent_query(query: QueryRequest | str) -> None:
    response = agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


def test_query_request_deprecation_warning(recwarn: pytest.WarningsRecorder) -> None:
    warnings.simplefilter("always", DeprecationWarning)
    query = {
        "query": "How are bispecific antibodies engineered?",
        "id": uuid4(),
        "group": "default",
    }

    response = agent_query(query, "default")

    deprecation_warnings = [
        w for w in recwarn if isinstance(w.message, DeprecationWarning)
    ]
    # there are two -- one for the QueryRequest and one for AnswerResponse
    assert len(deprecation_warnings) == 2
    assert "Using legacy query format" in str(deprecation_warnings[0].message)
    # just to vibe check we're still getting a healthly response with old queryrequest
    assert response.status == "success"


def test_query_named_template():
    response = agent_query(
        "How are bispecific antibodies engineered?", named_template="hasanybodydone"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_get_query_request() -> None:
    assert isinstance(
        await get_query_request(name="better table parsing"), QueryRequest
    )


def test_upload_file() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "default",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    )
    assert response["success"], f"Expected success in response {response}."


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
@pytest.mark.asyncio
async def test_async_agent_query(query: QueryRequest | str) -> None:
    response = await async_agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_feedback_model() -> None:
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)
    feedback = {"test_feedback": "great!"}
    assert (
        len(await async_send_feedback([response.answer.id], [feedback], "default")) == 1
    )


@pytest.mark.asyncio
async def test_async_tmp():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_upload_paper() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    upload_paper("10.1021/acs.jctc.2c01235", file)


def test_check_dois() -> None:
    response = check_dois(
        dois=[
            "10.1126/science.1240517",
            "10.1126/science.1240517",  # NOTE: duplicate input DOI
            "10.1016/j.febslet.2014.11.036",
        ]
    )
    assert response == {
        "10.1016/j.febslet.2014.11.036": ["c1433904691e17c2", "cached"],
        "10.1126/science.1240517": ["", "DOI not found"],
    }
