# app.py
# Arts & Advanced Big Data - Week 10
# Open API Project: "Artworks Explorer with The Met Museum by Seyeon (Fixed)"
# Author: Kim Seyeon

import streamlit as st
import requests
import random

# -------------------------------
# 🌟 Page Settings
# -------------------------------
st.set_page_config(page_title="Artworks Explorer by Seyeon", page_icon="🎨", layout="wide")

st.markdown("""
<style>
h1, h2, h3, h4, h5, h6 {font-family: 'Didot', serif; letter-spacing: 0.5px;}
body {font-family: 'Helvetica', sans-serif; background-color: #faf8f6;}
hr {border: none; border-top: 2px solid #d2b48c;}
.caption {color: #6c757d; font-style: italic;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🖼️ Title Section
# -------------------------------
st.title("🖼️ *Artworks Explorer with The Met Museum by Seyeon*")
st.markdown("### Discover timeless art and culture through the Met’s open collection.")
st.write("Search for artworks, explore artistic eras, and enjoy visual storytelling powered by Open API from The Metropolitan Museum of Art.")

st.divider()

# -------------------------------
# 🔍 Search Section
# -------------------------------
col1, col2 = st.columns([3,1])
with col1:
    query = st.text_input("🎨 Enter a theme, artist, or artwork keyword", "impressionism")
with col2:
    random_btn = st.button("✨ Surprise Me!")

# -------------------------------
# 🎲 Random Artwork Recommendation
# -------------------------------
if random_btn:
    random_list = ["love", "music", "nature", "moon", "fashion", "flower", "portrait", "light"]
    query = random.choice(random_list)
    st.info(f"🎲 Random theme selected: **{query.capitalize()}**")

if query:
    st.markdown(f"#### Searching artworks for: *{query}* …")

    # 1️⃣ Search by keyword
    search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}"
    res = requests.get(search_url)
    data = res.json()

    if data["total"] == 0:
        st.warning("No artworks found. Try another keyword 🎭")
    else:
        object_ids = data["objectIDs"][:15]
        st.markdown(f"##### Found **{len(object_ids)}** related artworks in the Met Collection.")
        st.write("---")

        # 2️⃣ Display artworks in grid format (with JSONDecodeError handling)
        cols = st.columns(3)
        for i, obj_id in enumerate(object_ids):
            detail_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
            detail_res = requests.get(detail_url)

            try:
                detail_data = detail_res.json()
            except Exception:
                continue  # Skip invalid JSON results

            if "primaryImageSmall" in detail_data and detail_data["primaryImageSmall"]:
                title = detail_data.get("title", "Untitled")
                artist = detail_data.get("artistDisplayName", "Unknown Artist")
                year = detail_data.get("objectDate", "N/A")
                medium = detail_data.get("medium", "")
                image = detail_data["primaryImageSmall"]

                with cols[i % 3]:
                    st.image(image, use_column_width=True)
                    st.markdown(f"**{title}**")
                    st.caption(f"👤 {artist} | 🗓 {year}")
                    with st.expander("More about this artwork"):
                        st.write(f"**Medium:** {medium}")
                        st.write(f"**Department:** {detail_data.get('department', '—')}")
                        st.write(f"**Culture:** {detail_data.get('culture', '—')}")
                        st.markdown(f"[🔗 View on The Met Website]({detail_data.get('objectURL', '#')})")
