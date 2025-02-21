import streamlit as st
import json
import os
import nltk
from collections import defaultdict

# Ensure required nltk resources are downloaded
nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load stored categories from storage.json
STORAGE_FILE = "storage.json"

def initialize_storage():
    """Creates storage.json if it doesn't exist with predefined categories."""
    if not os.path.exists(STORAGE_FILE):
        categories = {
            "categories": {
                "Python": "python_resources.json",
                "Java": "java_resources.json",
                "Machine Learning": "ml_resources.json",
                "Deep Learning": "dl_resources.json",
                "Artificial Intelligence": "ai_resources.json",
                "Cloud Computing": "cloud_resources.json",
                "DevOps": "devops_resources.json",
                "Competitive Programming": "cp_resources.json",
                "Frontend": "frontend_resources.json",
                "Backend": "backend_resources.json",
                "AI Tools": "ai_tools_resources.json",
                "Data Science": "data_science_resources.json",
                "General Resources": "general_resources.json"
            }
        }
        with open(STORAGE_FILE, "w") as f:
            json.dump(categories, f, indent=4)

def load_data(file):
    """Loads JSON data from a file, returns empty dict if file doesn't exist."""
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(data, file):
    """Saves data to a JSON file."""
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Initialize storage.json if not exists
initialize_storage()

# Load categories
storage_data = load_data(STORAGE_FILE)
categories = storage_data.get("categories", {})

# Ensure category files exist
for category, filename in categories.items():
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({category: []}, f, indent=4)

# Streamlit UI
st.set_page_config(page_title="Educational Resources", layout="wide")

# Center the title using markdown and inline CSS
st.markdown(
    """
    <style>
        .centered-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #F5F5F5;
        }
        .stButton>button {
            border: 2px solid #fff;
            border-radius: 8px;
            padding: 10px;
            background-color: #212121;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            border: 2px solid #fff;
            box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.6);
        }
        .form-label {
            color: #FFFDF0;
        }
        .form-input, .stSelectbox, .stTextArea, .stTextInput {
            color: #FBF5DD;
        }
    </style>
    """, unsafe_allow_html=True
)

# Apply the text color #FFF0BD for the entire text
st.markdown('<div class="centered-title">🌐📖EduLinks</div><br>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 18px; color: #D84040;">Explore Educational Resources by Category</div><br>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Display categories in a grid with toggle feature
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None

for index, category in enumerate(categories.keys()):
    with (col1 if index % 3 == 0 else col2 if index % 3 == 1 else col3):
        if st.button(category, key=f"btn_{category}"):

            # Toggle category selection
            st.session_state["selected_category"] = (
                None if st.session_state["selected_category"] == category else category
            )

# Display selected category resources
if st.session_state["selected_category"]:
    selected_category = st.session_state["selected_category"]
    filename = categories.get(selected_category, "")

    if filename:
        st.subheader(f"\U0001F4CC {selected_category} Resources")  # 📌
        category_data = load_data(filename)
        resources = category_data.get(selected_category, [])

        if resources:
            for resource in resources:
                st.markdown(
                    f"<a href='{resource['url']}' target='_blank' title='{resource['description']}' style='color: #FFFFBF5DD;'>{resource['name']}</a>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("No resources available.")

# Form to submit new resources
st.markdown('<div style="font-size: 20px; color: #E50046;">💡 Share a Valuable New Resource</div>', unsafe_allow_html=True)  # Title in #FFF0BD color

name = st.text_input("Website Name", key="website_name")
department = st.text_input("Department", key="department")
category_selection = st.selectbox("Select Category", list(categories.keys()))
url = st.text_input("Resource URL", key="url")
description = st.text_area("Short Description", key="description")

if st.button("Submit Resource"):
    if name and department and url and description and category_selection:
        # Handle "None" option as "General Resources"
        if category_selection == "None":
            category_selection = "General Resources"  # Assign to General Resources

        # Load the relevant category data
        filename = categories.get(category_selection, "")
        if filename:
            category_data = load_data(filename)
            if category_selection not in category_data:
                category_data[category_selection] = []

            # Check if the resource URL already exists in the category
            existing_resources = category_data[category_selection]
            resource_exists = any(
                res["url"] == url or res["name"] == name for res in existing_resources
            )

            if resource_exists:
                st.warning("This resource already exists in the selected category.")
            else:
                # Add the new resource if it does not exist
                category_data[category_selection].append(
                    {"name": name, "url": url, "description": description}
                )
                save_data(category_data, filename)
                st.success("Resource added successfully!")
    else:
        st.warning("Please fill in all fields.")