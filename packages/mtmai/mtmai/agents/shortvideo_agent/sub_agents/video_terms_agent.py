import json

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types  # noqa
from json_repair import repair_json
from mtmai.model_client.utils import get_default_litellm_model


def after_agent_callback(callback_context: CallbackContext):
    # 修正 video_terms 的类型, 确保为json array
    video_terms = callback_context.state.get("video_terms")
    if video_terms:
        if isinstance(video_terms, str):
            video_terms = json.loads(repair_json(video_terms))
        callback_context.state["video_terms"] = video_terms

    return None


def new_video_terms_agent():
    video_terms_agent = LlmAgent(
        name="VideoTermsGenerator",
        model=get_default_litellm_model(),
        instruction="""
    # Role: Video Search Terms Generator

    ## Goals:
    Generate {video_terms_amount} search terms for stock videos, depending on the subject of a video.

    ## Constrains:
    1. the search terms are to be returned as a json-array of strings.
    2. each search term should consist of 1-3 words, always add the main subject of the video.
    3. you must only return the json-array of strings. you must not return anything else. you must not return the script.
    4. the search terms must be related to the subject of the video.
    5. reply with english search terms only.

    ## Output Example:
    ["search term 1", "search term 2", "search term 3","search term 4","search term 5"]

    ## Context:
    ### Video Subject
    {video_subject}

    ### Video Script
    {video_script}

    Please note that you must use English for generating video search terms; Chinese is not accepted.
    """.strip(),
        input_schema=None,
        output_key="video_terms",
        after_agent_callback=after_agent_callback,
    )
    return video_terms_agent
