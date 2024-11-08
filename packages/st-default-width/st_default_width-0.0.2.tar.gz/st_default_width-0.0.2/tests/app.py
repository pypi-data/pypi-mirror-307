import streamlit as st
from st_default_width import set_use_container_width_default


def main():
    st.header("`st_default_width`", divider="rainbow")

    st.markdown("**Getting started:**")
    st.code(
        """
        import streamlit as st
        from st_default_width import set_use_container_width_default

        set_use_container_width_default()
        st.image("https://placehold.co/50x50")
        st.button("Botón")
        """,
        language="python",
    )
    st.divider()
    st.markdown("**Examples:**")

    with st.echo():
        set_use_container_width_default()

        cols = st.columns([1, 2])
        with cols[0]:
            st.image("https://placehold.co/50x50")
            st.button("A button :)")

        with cols[1]:
            st.image("https://placehold.co/100x50")
            st.button("A button :D")

    st.divider()

    with st.echo():
        set_use_container_width_default(False)

        cols = st.columns([1, 2])
        with cols[0]:
            st.image("https://placehold.co/50x50")
            st.button("A button :(")

        with cols[1]:
            st.image("https://placehold.co/100x50")
            st.button("A button :S")

    with st.sidebar:
        st.markdown(
            "Make `use_container_width = True` in all streamlit elements.",
        )
        st.divider()
        st.markdown("**Installation:**")
        st.code("pip install st_default_width", language="sh")
        st.markdown(
            "**Source:**\n\n"
            "[![Source](https://img.shields.io/static/v1?label=&message=Source%20code&color=informational&logo=github)]"
            "(https://github.com/edsaac/st_default_width)"
            "&nbsp;"
            "[![Source](https://badgen.net/pypi/v/st_default_width)]"
            "(https://pypi.org/project/st-default-width/)"
        )


if __name__ == "__main__":
    st.set_page_config(page_title="st_default_width", page_icon="↔️")

    intro_page = st.Page(main, title="Start here", icon="↔️", default=True)

    interactive_page = st.Page(
        "app_pages/interactive.py", title="Interactive", icon="🕹️"
    )

    small_test_page = st.Page("app_pages/small_test.py", title="Small Test", icon="🧪")

    pg = st.navigation(
        {"Intro": [intro_page], "Examples": [small_test_page, interactive_page]}
    )
    pg.run()
