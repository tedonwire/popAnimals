"""Streamlit version: show a random animal picture. Click the picture to get a new one.

Requirements:  pip install streamlit requests
Run:           streamlit run streamlit_app.py
"""
import random

import requests
import streamlit as st

TIMEOUT = 10

SOURCES = [
    ("Dog", lambda: requests.get("https://dog.ceo/api/breeds/image/random", timeout=TIMEOUT).json()["message"]),
    ("Cat", lambda: requests.get("https://api.thecatapi.com/v1/images/search", timeout=TIMEOUT).json()[0]["url"]),
    ("Fox", lambda: requests.get("https://randomfox.ca/floof/", timeout=TIMEOUT).json()["image"]),
    ("Duck", lambda: requests.get("https://random-d.uk/api/v2/random", timeout=TIMEOUT).json()["url"]),
    ("Shiba", lambda: requests.get("https://shibe.online/api/shibes", timeout=TIMEOUT).json()[0]),
]


def fetch_random_animal():
    """Try the sources in random order until one works. Returns (name, image URL)."""
    sources = SOURCES[:]
    random.shuffle(sources)
    for name, get_url in sources:
        try:
            return name, get_url()
        except Exception:
            continue
    return None, None


st.set_page_config(page_title="Random Animal", page_icon="🐾")
st.title("🐾 Random Animal")

# The script re-runs on every page load or button click, so each run picks a new animal.
name, url = fetch_random_animal()

if url is None:
    st.error("Could not load an animal image. Please try again.")
else:
    # st.image() is not clickable, so wrap the picture in a link back to this page.
    # Clicking it reloads the app, which picks a new random animal.
    st.markdown(
        f'<a href="./" target="_self">'
        f'<img src="{url}" style="max-width:100%; max-height:600px; border-radius:12px; cursor:pointer;">'
        f"</a>",
        unsafe_allow_html=True,
    )
    st.caption(f"{name} - click the picture for a new animal")

# Fallback for browsers or setups where the link click doesn't refresh.
st.button("Show another animal")