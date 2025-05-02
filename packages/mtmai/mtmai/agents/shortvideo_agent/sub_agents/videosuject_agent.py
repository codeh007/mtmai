from google.adk.agents import LlmAgent
from google.genai import types  # noqa
from mtmai.model_client.utils import get_default_litellm_model


def new_video_subject_agent():
    video_subject_generator = LlmAgent(
        name="VideoSubjectGenerator",
        model=get_default_litellm_model(),
        instruction="""
    # Role: Video Subject Generator

    ## Goals:
    Generate a subject for a video, depending on the user's input.

    ## Constrains:
    1. the subject is to be returned as a string.
    2. the subject must be related to the user's input.
    """.strip(),
        input_schema=None,
        output_key="video_subject",  # Key for storing output in session state
    )
    return video_subject_generator
