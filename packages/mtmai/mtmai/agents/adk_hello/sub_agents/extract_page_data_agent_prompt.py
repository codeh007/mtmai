"""Prompt definition for extract_page_data_agent in FOMC Research Agent"""

PROMPT = """
Your job is to extract important data from a web page.

 <PAGE_CONTENTS>
 {page_contents}
 </PAGE_CONTENTS>

<INSTRUCTIONS>
The contents of the web page are provided above in the 'page_contents' section.
The data fields needed are provided in the 'data_to_extract' section of the user
input.

Read the contents of the web page and extract the pieces of data requested.
Don't use any other HTML parser, just examine the HTML yourself and extract the
information.

First, use the store_state tool to store the extracted data in the ToolContext.

Second, return the information you found to the user in JSON format.
 </INSTRUCTIONS>

"""
