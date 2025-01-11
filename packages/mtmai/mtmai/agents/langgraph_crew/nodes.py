import logging
import os
import time

logger = logging.getLogger()

# from langchain_community.agent_toolkits import GmailToolkit
# from langchain_community.tools.gmail.search import GmailSearch


class Nodes:
    def __init__(self):
        # self.gmail = GmailToolkit()
        pass

    def check_email(self, state):
        logger.info("# Checking for new emails")
        # search = GmailSearch(api_resource=self.gmail.api_resource)
        # emails = search("after:newer_than:1d")
        emails = []
        checked_emails = (
            state["checked_emails_ids"] if state["checked_emails_ids"] else []
        )
        thread = []
        new_emails = []
        for email in emails:
            if (
                (email["id"] not in checked_emails)
                and (email["threadId"] not in thread)
                and (os.environ["MY_EMAIL"] not in email["sender"])
            ):
                thread.append(email["threadId"])
                new_emails.append(
                    {
                        "id": email["id"],
                        "threadId": email["threadId"],
                        "snippet": email["snippet"],
                        "sender": email["sender"],
                    }
                )

        ids_to_check = ["id1", "id2"]
        # checked_emails.extend([email["id"] for email in emails])
        checked_emails.extend(ids_to_check)
        return {**state, "emails": new_emails, "checked_emails_ids": checked_emails}

    def wait_next_run(self, state):
        logger.debug("## wait_next_run")
        time.sleep(2)
        return state

    def new_emails(self, state):
        if len(state["emails"]) == 0:
            logger.info("## No new emails")
            return "end"
        else:
            print("## New emails")
            return "continue"
