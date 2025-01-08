
import requests
from bs4 import BeautifulSoup
import pandas as pd
import langchain
import llama_index
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

import pinecone
import gradio as gr


# Extract course data
import requests
from bs4 import BeautifulSoup
import csv
import time

# # Base URL
# base_url = "https://courses.analyticsvidhya.com/collections/courses?page="

# # Function to get individual course links from a page
# def get_course_links(page_number):
#     url = f"{base_url}{page_number}"
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to fetch page {page_number}")
#         return None
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     course_links = []
    
#     # Find course links (update selector as per website structure)
#     link_containers = soup.find_all('a', class_='course-card course-card__public published')  # Example class name for links

#     for link in link_containers:
#         href = link.get('href')
#         if href:
#             course_links.append(f"https://courses.analyticsvidhya.com{href}")  # Make full URL
    
#     return course_links

# # Function to scrape details from an individual course page
# def scrape_course_details(course_url):
#     response = requests.get(course_url)
#     if response.status_code != 200:
#         print(f"Failed to fetch course details from {course_url}")
#         return None
    
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Scrape course details (update selectors as per structure)
#     # Extract the title
#     title_tag = soup.find('h1', class_='section__heading')
#     title = title_tag.text.strip() if title_tag else "No Title"

#         # Extract the description
#     # Extract the description
#     description_tag = soup.find('div', class_='fr-view')
#     description = description_tag.get_text(strip=True) if description_tag else "No Description"
#     curriculum = []
    
#     curriculum_section = soup.find('ul', class_='course-curriculum__chapter-content')  # Example class for curriculum section
#     if curriculum_section:
#         curriculum_items = curriculum_section.find_all('li')  # Assuming curriculum is in a list
#         for item in curriculum_items:
#             curriculum.append(item.text.strip())
    
#     return {
#         'title': title,
#         'description': description,
#         'curriculum': " | ".join(curriculum)  # Join curriculum items with separator
#     }

# # Scrape all courses
# all_courses = []
# page = 1

# while True:
#     print(f"Scraping page {page}...")
#     course_links = get_course_links(page)
    
#     if not course_links:
#         print(f"No more courses found on page {page}. Stopping.")
#         break
    
#     for course_url in course_links:
#         print(f"Scraping course: {course_url}")
#         course_details = scrape_course_details(course_url)
#         if course_details:
#             all_courses.append(course_details)
#         time.sleep(1)  # Add delay to avoid overwhelming the server
    
#     page += 1

# # Save data to CSV
# csv_file = "courses_details.csv"
# with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
#     fieldnames = ["title", "description", "curriculum"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(all_courses)

# print(f"Data saved to {csv_file}")



# Example Data
courses = [
    {"Title": "Intro to AI", "Description": "Learn basics of AI."},
    {"Title": "Data Science", "Description": "Introduction to data science."}
]

# Initialize Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Generate Embeddings
course_texts = [course['Title'] + " " + course['Description'] for course in courses]
embeddings = [embedding_model.embed_query(text) for text in course_texts]

print(embeddings)
# Check if the index exists, and create one if it doesn't
import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone instance
pc = Pinecone(
    api_key="pcsk_9U1cJ_G6eXnzGmxrXg9ga4NyT323yw5riFVeBrJWBsdWZyk6DocpyemypxHp9BrTCcoXS",  # Replace with your actual API key
)
# Check if the index already exists
# Index name
index_name = "my-index2"

# Check if the index exists
existing_indexes = pc.list_indexes()

# Check if the index exists
if index_name in existing_indexes:
    print(f"Index '{index_name}' already exists.")
else:
    # Create the index if it does not exist
    try:
        pc.create_index(
            name=index_name,
            dimension=384,   # Adjust dimension based on embeddings
            metric='cosine',  # Supported metrics: cosine, euclidean, dotproduct
            spec=ServerlessSpec(
                cloud='aws',   # Specify cloud
                region='us-east-1'  # Specify AWS region
            )
        )
        print(f"Index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error creating index: {e}")

# Access the existing or newly created index
try:
    index = pc.Index(index_name)
    print("Index accessed successfully.")
except Exception as e:
    print(f"Error accessing index: {e}")


# embbing
for i, embed in enumerate(embeddings):
    index.upsert([(str(i), embed)])
print("Data stored in Pinecone")

import faiss
import numpy as np

# Create FAISS Index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))  # Add embeddings to index

# Query Example
query_vector = embedding_model.embed_query("AI basics")
distances, indices = index.search(np.array([query_vector]), k=3)
print("Closest Courses:", indices)


def search_courses(query):
    # Perform search using embeddings or Pinecone/FAISS
    # Example: return top course titles
    return ["Course 1", "Course 2", "Course 3"]

iface = gr.Interface(fn=search_courses, inputs="text", outputs="text")
iface.launch(share=True)

import streamlit as st

st.title("Course Search Tool")
query = st.text_input("Enter your query:")
if query:
    # Perform search using embeddings or Pinecone/FAISS
    # Example: Display top results
    st.write(["Course 1", "Course 2", "Course 3"])
