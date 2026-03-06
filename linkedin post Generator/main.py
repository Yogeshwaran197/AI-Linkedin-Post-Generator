import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post


# Page Config
st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="",
    layout="wide"
)

# Options
length_options = ["Short", "Medium", "Long"]


def main():
    st.title("AI LinkedIn Post Generator")
    st.markdown("Generate high-quality LinkedIn posts using AI + Few-Shot Learning.")

    st.divider()

    fs = FewShotPosts()
    tags = fs.get_tags()

    # UI Layout
    col1, col2 = st.columns(2)

    with col1:
        selected_tag = st.selectbox("Select Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Select Length", options=length_options)

    st.divider()

    # Generate Button
    if st.button("Generate Post", use_container_width=True):

        with st.spinner("Generating your LinkedIn post..."):
            post = generate_post(
                selected_length,
                selected_tag
            )

        st.success("Post Generated Successfully!")

        st.subheader("Your Generated Post")
        st.write(post)

        # Copy Section
        st.code(post, language="markdown")

        st.info("Tip: Copy and paste directly into LinkedIn")


if __name__ == "__main__":

    main()

