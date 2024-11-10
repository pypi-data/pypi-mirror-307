import configparser
import json
from math import log
import os
from typing import Any, Dict

from linkedin_api import Linkedin
from linkedin_api.cookie_repository import CookieRepository
from loguru import logger
from requests import post
from requests.cookies import RequestsCookieJar, create_cookie
from tqdm import tqdm

LOX_PATH = os.path.expanduser("~/.lox")
CONFIG_PATH = os.path.join(LOX_PATH, "config")

if not os.path.exists(LOX_PATH):
    os.makedirs(LOX_PATH)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


class Lox:
    def __init__(self):
        self.linkedin_email = config.get("linkedin", "email")
        self.linkedin_password = config.get("linkedin", "password")
        self.notion_api_key = config.get("notion", "api_key")
        self.notion_database_id = config.get("notion", "database_id")

        self.load_linkedin_cookies()
        self.setup_linkedin_client()
        self.setup_notion_client()

    def load_linkedin_cookies(self):
        cookies = json.load(open(os.path.join(LOX_PATH, "cookies.json")))

        cookie_jar = RequestsCookieJar()

        for cookie_data in cookies:
            cookie = create_cookie(
                domain=cookie_data["domain"],
                name=cookie_data["name"],
                value=cookie_data["value"],
                path=cookie_data["path"],
                secure=cookie_data["secure"],
                expires=cookie_data.get("expirationDate", None),
                rest={
                    "HttpOnly": cookie_data.get("httpOnly", False),
                    "SameSite": cookie_data.get("sameSite", "unspecified"),
                    "HostOnly": cookie_data.get("hostOnly", False),
                },
            )
            cookie_jar.set_cookie(cookie)

        new_repo = CookieRepository()
        new_repo.save(cookie_jar, self.linkedin_email)

    def setup_linkedin_client(self):
        self.linkedin = Linkedin(self.linkedin_email, self.linkedin_password)

    def setup_notion_client(self):
        self.notion_headers = {
            "Authorization": f"Bearer {self.notion_api_key}",
            "Notion-Version": "2021-08-16",
            "Content-Type": "application/json",
        }

        response = self.read_from_notion()
        if response and "results" in response and len(response["results"]) > 0:
            self.notion_schema = response["results"][0]["properties"]
            logger.info(f"Loaded Notion schema: {self.notion_schema}")
        else:
            logger.error("Failed to load Notion schema")
            self.notion_schema = {}

    def get_post_content(self, url: str) -> str | None:
        try:
            post_id = self.extract_post_urn(url)
            comments = self.linkedin.get_post_comments(post_id)
            logger.info(f"Found {len(comments)} comments")
            cleaned_comments = self.clean_comments(comments)
            json.dump(cleaned_comments, open("comments.json", "w"))
            return json.dumps({"comments": cleaned_comments})
        except Exception as e:
            logger.error(f"Error fetching LinkedIn post: {e}")
            return None

    def get_notion_fields(self) -> list[str]:
        notion_schema = self.notion_schema
        return list(notion_schema.keys())

    def extract_post_urn(self, url: str) -> str:
        base_url = url.split("?")[0]
        base_url = base_url.rstrip("/")

        return base_url if ":" not in base_url else base_url.split(":")[-1]

    def read_from_notion(self):
        response = post(
            "https://api.notion.com/v1/databases/{}/query".format(self.notion_database_id), headers=self.notion_headers
        )
        response_json = response.json()
        return response_json

    def write_to_notion(self, data: dict[str, Any]) -> bool:
        try:
            if "entries" not in data:
                logger.error("No entries found in data")
                return False

            for entry in tqdm(data["entries"], desc="Writing to Notion"):
                notion_data = self.format_notion_entry(entry, self.notion_database_id)
                response = post("https://api.notion.com/v1/pages", headers=self.notion_headers, json=notion_data)
                if response.status_code != 200:
                    logger.error(f"Failed to write to Notion: {response.json()}")
            return True
        except Exception as e:
            logger.error(f"Error writing to Notion: {e}")
            return False

    def format_notion_value(self, type: str, value: str) -> dict[str, Any]:
        if type == "title":
            return {"title": [{"text": {"content": value}}]}
        elif type == "email":
            return {"email": value}
        elif type == "url":
            if "https://linkedin.com/in/" in value:
                return {"url": value}
            else:
                return {"url": f"https://linkedin.com/in/{value}"}
        elif type == "phone_number":
            return {"phone_number": value}
        else:
            return {"rich_text": [{"text": {"content": value}}]}

    def format_notion_entry(self, entry: Dict[str, Any], database_id: str) -> Dict[str, Any]:
        if type(entry) is not dict:
            logger.error(f"Invalid entry: {entry}")
            return {}

        properties = {}
        for k, v in entry.items():
            if k not in self.notion_schema:
                logger.warning(f"Field {k} not found in Notion schema: {self.notion_schema}")
                continue

            field_type = self.notion_schema[k]["type"]
            field_value = self.format_notion_value(field_type, v)
            properties[k] = field_value

        return {"parent": {"database_id": database_id}, "properties": properties}

    def extract_email(self, text: str) -> str | None:
        import re

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def clean_comments(self, comments: list) -> list:
        cleaned_comments = []
        for comment in comments:
            publicIdentifier = (
                comment.get("commenter", {})
                .get("com.linkedin.voyager.feed.MemberActor", {})
                .get("miniProfile", {})
                .get("publicIdentifier", "")
            )

            cleaned_comment = {
                "text": comment.get("commentV2", {}).get("text", ""),
                "created_time": comment.get("createdTime", ""),
                "commenter": {
                    "first_name": comment.get("commenter", {})
                    .get("com.linkedin.voyager.feed.MemberActor", {})
                    .get("miniProfile", {})
                    .get("firstName", ""),
                    "last_name": comment.get("commenter", {})
                    .get("com.linkedin.voyager.feed.MemberActor", {})
                    .get("miniProfile", {})
                    .get("lastName", ""),
                    "occupation": comment.get("commenter", {})
                    .get("com.linkedin.voyager.feed.MemberActor", {})
                    .get("miniProfile", {})
                    .get("occupation", ""),
                    "public_identifier": (
                        f"https://linkedin.com/in/{publicIdentifier}"
                        if "https://linkedin.com/in" not in publicIdentifier
                        else publicIdentifier
                    ),
                },
            }
            cleaned_comments.append(cleaned_comment)

        return cleaned_comments
