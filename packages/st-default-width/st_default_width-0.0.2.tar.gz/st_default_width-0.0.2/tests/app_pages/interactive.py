import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from st_default_width import (
    set_use_container_width_default,
    revert_use_container_width_default,
)


def main():
    st.header("↔️ `st_default_width`", divider="rainbow")

    with st.expander("Image", expanded=True):
        with st.echo():
            st.image("https://placehold.co/100x100")

    with st.expander("Dataframe", expanded=True):
        with st.echo():
            df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
            st.dataframe(df)
            st.data_editor(df)

    with st.expander("Plots", expanded=True):
        with st.echo():
            fig, ax = plt.subplots(figsize=(2, 1))
            ax.plot([1, 2, 3], [4, 5, 6])
            st.pyplot(fig)

    ## Module Controls
    with st.sidebar:
        st.button(
            "Set default to `True`",
            on_click=set_use_container_width_default,
        )

        st.button(
            "Set default to `False`",
            on_click=set_use_container_width_default,
            args=(False,),
        )

        st.button("Revert defaults", on_click=revert_use_container_width_default)


if __name__ == "__main__":
    main()

elif __name__ == "__page__":
    main()
