from argparse import ArgumentParser

from loguru import logger
from perse import extract_json_fields
from pydantic import BaseModel

from lox import utils
from lox.lox import Lox
from lox.version import __version__


def get_user_field_selection(fields_info) -> list[str]:
    print("\nAvailable fields:")
    for idx, field in enumerate(fields_info.fields):
        print(f"{idx + 1}. {field.name} ({field.type})")

    selected = input("\nEnter field numbers to extract (comma-separated): ")
    selected_indices = [int(x.strip()) - 1 for x in selected.split(",")]
    return [fields_info.fields[i] for i in selected_indices]


def main():
    parser = ArgumentParser(description="Extract LinkedIn post data to Notion")
    parser.add_argument("--url", type=str, required=True, help="LinkedIn post URL")
    parser.add_argument("--version", action="store_true", help="Show version information")
    args = parser.parse_args()

    if args.version:
        print(f"lox v{__version__}")
        return

    lox = Lox()

    logger.info("Fetching LinkedIn post...")
    post_content = lox.get_post_content(args.url)

    if not post_content:
        logger.error("Failed to fetch post")
        return

    logger.info("Getting fields from notion...")
    fields = lox.get_notion_fields()

    logger.info(f"Building data model for {len(fields)} fields...")
    PydanticModel = utils.build_pydantic_model(fields)

    class Entries(BaseModel):
        entries: list[PydanticModel]

    logger.info("Extracting data...")
    extracted_data = extract_json_fields(post_content, Entries, model="gpt-4o-2024-08-06")

    logger.info("Writing to Notion...")
    success = lox.write_to_notion(extracted_data)

    if success:
        logger.info("Successfully wrote data to Notion")
    else:
        logger.error("Failed to write data to Notion")


if __name__ == "__main__":
    main()
