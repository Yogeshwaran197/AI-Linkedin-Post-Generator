import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []

        for post in posts:
            # Make sure correct key exists (Text or text)
            content = post.get("Text") or post.get("text")
            if not content:
                raise KeyError("No valid text field found in post")

            metadata = extract_metadata(content)
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


# -------------------------
# FIXED extract_metadata
# -------------------------
def extract_metadata(post):
    json_parser = JsonOutputParser()

    template = """
    You are given a LinkedIn post.

    Extract:
    - line_count (integer)
    - language (must always be "English")
    - tags (array of maximum two short tags)

    Important Rules:
    1. Language MUST always be "English".
    2. Do NOT return Hinglish.
    3. Return valid JSON only.
    4. No explanation. No code. JSON only.

    {format_instructions}

    Here is the post:
    {post}
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm | json_parser

    result = chain.invoke({
        "post": post,
        "format_instructions": json_parser.get_format_instructions()
    })

    return result


# -------------------------
# FIXED get_unified_tags
# -------------------------
def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    json_parser = JsonOutputParser()

    template = """
    I will give you a list of tags.

    You need to unify tags with the following requirements:

    1. Merge similar tags.
    2. Use Title Case.
    3. Return JSON mapping original tag → unified tag.
    4. No explanation. JSON only.

    {format_instructions}

    Here are the tags:
    {tags}
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm | json_parser

    result = chain.invoke({
        "tags": unique_tags_list,
        "format_instructions": json_parser.get_format_instructions()
    })

    return result


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")