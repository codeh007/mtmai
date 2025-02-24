import asyncio
import os

import pytest
from dotenv import load_dotenv

envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
load_dotenv(envFileAbsPath)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


data = r"""{
  "messages": [
    {
      "content": "You are a precise browser automation agent that interacts with websites through structured commands. Your role is to:\n1. Analyze the provided webpage elements and structure\n2. Plan a sequence of actions to accomplish the given task\n3. Respond with valid JSON containing your action sequence and state assessment\n\nCurrent date and time: 2025-01-17 05:51\n\n\nINPUT STRUCTURE:\n1. Current URL: The webpage you're currently on\n2. Available Tabs: List of open browser tabs\n3. Interactive Elements: List in the format:\n   index[:]<element_type>element_text</element_type>\n   - index: Numeric identifier for interaction\n   - element_type: HTML element type (button, input, etc.)\n   - element_text: Visible text or element description\n\nExample:\n33[:]<button>Submit Form</button>\n_[:] Non-interactive text\n\n\nNotes:\n- Only elements with numeric indexes are interactive\n- _[:] elements provide context but cannot be interacted with\n\n\n\n1. RESPONSE FORMAT: You must ALWAYS respond with valid JSON in this exact format:\n   {\n     \"current_state\": {\n       \"evaluation_previous_goal\": \"Success|Failed|Unknown - Analyze the current elements and the image to check if the previous goals/actions are successful like intended by the task. Ignore the action result. The website is the ground truth. Also mention if something unexpected happened like new suggestions in an input field. Shortly state why/why not\",\n       \"memory\": \"Description of what has been done and what you need to remember until the end of the task\",\n       \"next_goal\": \"What needs to be done with the next actions\"\n     },\n     \"action\": [\n       {\n         \"one_action_name\": {\n           // action-specific parameter\n         }\n       },\n       // ... more actions in sequence\n     ]\n   }\n\n2. ACTIONS: You can specify multiple actions in the list to be executed in sequence. But always specify only one action name per item. \n\n   Common action sequences:\n   - Form filling: [\n       {\"input_text\": {\"index\": 1, \"text\": \"username\"}},\n       {\"input_text\": {\"index\": 2, \"text\": \"password\"}},\n       {\"click_element\": {\"index\": 3}}\n     ]\n   - Navigation and extraction: [\n       {\"open_new_tab\": {}},\n       {\"go_to_url\": {\"url\": \"https://example.com\"}},\n       {\"extract_page_content\": {}}\n     ]\n\n\n3. ELEMENT INTERACTION:\n   - Only use indexes that exist in the provided element list\n   - Each element has a unique index number (e.g., \"33[:]<button>\")\n   - Elements marked with \"_[:]\" are non-interactive (for context only)\n\n4. NAVIGATION & ERROR HANDLING:\n   - If no suitable elements exist, use other functions to complete the task\n   - If stuck, try alternative approaches\n   - Handle popups/cookies by accepting or closing them\n   - Use scroll to find elements you are looking for\n\n5. TASK COMPLETION:\n   - Use the done action as the last action as soon as the task is complete\n   - Don't hallucinate actions\n   - If the task requires specific information - make sure to include everything in the done function. This is what the user will see.\n   - If you are running out of steps (current step), think about speeding it up, and ALWAYS use the done action as the last action.\n\n6. VISUAL CONTEXT:\n   - When an image is provided, use it to understand the page layout\n   - Bounding boxes with labels correspond to element indexes\n   - Each bounding box and its label have the same color\n   - Most often the label is inside the bounding box, on the top right\n   - Visual context helps verify element locations and relationships\n   - sometimes labels overlap, so use the context to verify the correct element\n\n7. Form filling:\n   - If you fill an input field and your action sequence is interrupted, most often a list with suggestions popped up under the field and you need to first select the right element from the suggestion list.\n\n8. ACTION SEQUENCING:\n   - Actions are executed in the order they appear in the list \n   - Each action should logically follow from the previous one\n   - If the page changes after an action, the sequence is interrupted and you get the new state.\n   - If content only disappears the sequence continues.\n   - Only provide the action sequence until you think the page will change.\n   - Try to be efficient, e.g. fill forms at once, or chain actions where nothing changes on the page like saving, extracting, checkboxes...\n   - only use multiple actions if it makes sense. \n\n\n   - use maximum 10 actions per sequence\n\nFunctions:\nSearch Google in the current tab: \n{search_google: {'query': {'type': 'string'}}}\nNavigate to URL in the current tab: \n{go_to_url: {'url': {'type': 'string'}}}\nGo back: \n{go_back: {}}\nClick element: \n{click_element: {'index': {'type': 'integer'}, 'xpath': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None}}}\nInput text into a input interactive element: \n{input_text: {'index': {'type': 'integer'}, 'text': {'type': 'string'}, 'xpath': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None}}}\nSwitch tab: \n{switch_tab: {'page_id': {'type': 'integer'}}}\nOpen url in new tab: \n{open_tab: {'url': {'type': 'string'}}}\nExtract page content to get the pure text or markdown with links if include_links is set to true: \n{extract_content: {'include_links': {'type': 'boolean'}}}\nComplete task: \n{done: {'text': {'type': 'string'}}}\nScroll down the page by pixel amount - if no amount is specified, scroll down one page: \n{scroll_down: {'amount': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None}}}\nScroll up the page by pixel amount - if no amount is specified, scroll up one page: \n{scroll_up: {'amount': {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': None}}}\nSend strings of special keys like Backspace, Insert, PageDown, Delete, Enter, Shortcuts such as `Control+o`, `Control+Shift+T` are supported as well. This gets used in keyboard.press. Be aware of different operating systems and their shortcuts: \n{send_keys: {'keys': {'type': 'string'}}}\nIf you dont find something which you want to interact with, scroll to it: \n{scroll_to_text: {'text': {'type': 'string'}}}\nGet all options from a native dropdown: \n{get_dropdown_options: {'index': {'type': 'integer'}}}\nSelect dropdown option for interactive element index by the text of the option you want to select: \n{select_dropdown_option: {'index': {'type': 'integer'}, 'text': {'type': 'string'}}}\n\nRemember: Your responses must be valid JSON matching the specified format. Each action in the sequence must be valid.",
      "role": "system"
    },
    {
      "content": "",
      "role": "assistant",
      "tool_calls": [
        {
          "type": "function",
          "id": "",
          "function": {
            "name": "AgentOutput",
            "arguments": "{\"current_state\": {\"evaluation_previous_goal\": \"Unknown - No previous actions to evaluate.\", \"memory\": \"\", \"next_goal\": \"Obtain task from user\"}, \"action\": []}"
          }
        }
      ]
    },
    {
      "content": "Your ultimate task is: Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'. If you achieved your ultimate task, stop everything and use the done action in the next step to complete the task. If not, continue as usual.",
      "role": "user"
    },
    {
      "content": "\n\nCurrent url: about:blank\nAvailable tabs:\n[TabInfo(page_id=0, url='about:blank', title='')]\nInteractive elements from current page view:\nempty page\n",
      "role": "user"
    }
  ],
  "model": "llama3.1-70b",
  "max_completion_tokens": 4096,
  "n": 1,
  "stream": false,
  "temperature": 0.0,
  "tool_choice": {
    "type": "function",
    "function": {
      "name": "AgentOutput"
    }
  },
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "AgentOutput",
        "description": "",
        "parameters": {
          "type": "object",
          "properties": {
            "current_state": {
              "description": "Current state of the agent",
              "properties": {
                "evaluation_previous_goal": {
                  "type": "string"
                },
                "memory": {
                  "type": "string"
                },
                "next_goal": {
                  "type": "string"
                }
              },
              "required": [
                "evaluation_previous_goal",
                "memory",
                "next_goal"
              ],
              "type": "object"
            }
          }
        }
      }
    }
  ]
}"""
# @pytest.mark.asyncio
# async def test_abc():

# target_url=os.getenv("OPENAI_BASE_URL")+"/chat/completions"
# request_data = json.loads(data)
# response=httpx.post(
#   	target_url,json=request_data,
# 	headers={"Authorization":f"Bearer {os.getenv('OPENAI_API_KEY')}"})
# # 返回的文本中不包含error
# assert response.text.find("error")==-1
