import json
import os
from typing import List
from typing import Union, Literal, Annotated

from pydantic import BaseModel, Field


class PUB(BaseModel):
    topic_type: Literal["PUB"]
    topic_name: str
    topic_key: str
    message_type: str


class SUB(BaseModel):
    topic_type: Literal["SUB"]
    topic_name: str
    topic_key: str
    message_type: str


Topic = Annotated[Union[PUB, SUB], Field(discriminator="topic_type")]


class Topics(BaseModel):
    topics: List[Topic]


def parse_topics() -> Topics:
    try:
        topic_data_env = os.environ["TOPICS"]
        return Topics.model_validate_json(topic_data_env)
    except KeyError:
        raise EnvironmentError("`TOPICS` environment variable not set.")
    except json.JSONDecodeError as e:
        raise ValueError("`TOPICS` environment variable is not valid JSON.") from e
