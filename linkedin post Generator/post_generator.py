from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, tag):
    prompt = get_prompt(length, tag)
    response = llm.invoke(prompt)
    return response.content.strip()


def get_prompt(length, tag):
    length_str = get_length_str(length)

    prompt = f"""
You are an expert LinkedIn content creator.

Generate a high-quality LinkedIn post with the following requirements:

1) Topic: {tag}
2) Length: {length_str}
3) Language: English only
4) Tone: Professional but engaging
5) No preamble. No explanation. Only the final post.
6) Add proper spacing between lines for readability.
7) End with a subtle engaging line or thought (optional question or insight).

"""

    examples = few_shot.get_filtered_posts(length=length, tag=tag)

    if len(examples) > 0:
        prompt += "\nUse the writing style similar to the examples below:\n"

    for i, post in enumerate(examples):
        post_text = post["Text"]
        prompt += f"\nExample {i+1}:\n{post_text}\n"

        if i == 1:  # Maximum 2 examples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "Mental Health"))