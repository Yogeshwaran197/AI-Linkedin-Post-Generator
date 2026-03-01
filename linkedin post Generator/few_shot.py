import pandas as pd
import json
import random


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        self.df = pd.json_normalize(posts)

        # Force only English posts
        self.df = self.df[self.df["language"] == "English"]

        # Categorize length
        self.df["length"] = self.df["line_count"].apply(self.categorize_length)

        # Collect unique tags
        all_tags = self.df["tags"].sum()
        self.unique_tags = list(set(all_tags))

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length=None, tag=None, sample_size=3):
        df_filtered = self.df

        if length:
            df_filtered = df_filtered[df_filtered["length"] == length]

        if tag:
            df_filtered = df_filtered[
                df_filtered["tags"].apply(lambda tags: tag in tags)
            ]

        # Random sampling for better few-shot examples
        if len(df_filtered) > sample_size:
            df_filtered = df_filtered.sample(sample_size)

        return df_filtered.to_dict(orient="records")

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()

    print("Available Tags:", fs.get_tags())

    posts = fs.get_filtered_posts(
        length="Medium",
        tag="Job Search",
        sample_size=2
    )

    print(posts)