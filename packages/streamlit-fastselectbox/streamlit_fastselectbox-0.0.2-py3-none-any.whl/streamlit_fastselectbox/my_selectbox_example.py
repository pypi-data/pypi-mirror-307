
import os
import sys
import streamlit as st

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Insert the path to the streamlit_fastselectbox directory into sys.path
sys.path.insert(0, os.path.join(current_dir, '..'))


def write_something(*args, **kwargs):
    st.write(
        f"You picked {st.session_state.selectbox}", f"args: {args}", f"kwargs: {kwargs}")


def run():
    from streamlit_fastselectbox import st_fastselectbox
    st.subheader("Component with constant args")

    sample_companies = ["Smith Inc.", "Jones Ltd.",
                        "Brown Plc.", "Smithson Inc."]

    selection = st_fastselectbox(
        "my label",
        options=sample_companies,
        max_results=None,
        key="selectbox",
        on_change=write_something,
        args=["foo"],
        kwargs={"bar": "baz"},
        is_searchable=True,
        is_clearable=True,
    )

    st.write("You selected:", selection)


if __name__ == "__main__":
    run()
