# Extract course data
import requests
from bs4 import BeautifulSoup
import time


# URL of the free courses page
url = "https://courses.analyticsvidhya.com/collections/courses?page=1"

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
course_links = []
link_containers = soup.find_all('a', class_='course-card course-card__public published')  # Example class name for links
for link in link_containers:
        href = link.get('href')
        if href:
            course_links.append(f"https://courses.analyticsvidhya.com{href}")  # Make full URL
    
# for i in course_links:
#      print(i)
for i in course_links:
    response = requests.get(i)
    if response.status_code != 200:
        print(f"Failed to fetch course details from {i}")
        
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
        # Scrape course details (update selectors as per structure)
        # Extract the title
    title_tag = soup.find('h1', class_='section__heading')
    title = title_tag.text.strip() if title_tag else "No Title"

        # Extract the description
    # Extract the description
    description_tag = soup.find('div', class_='fr-view')
    description = description_tag.get_text(strip=True) if description_tag else "No Description"
    curriculum = []
    
    curriculum_section = soup.find('ul', class_='course-curriculum__chapter-content')  # Example class for curriculum section
    if curriculum_section:
        curriculum_items = curriculum_section.find_all('li')  # Assuming curriculum is in a list
        for item in curriculum_items:
            curriculum.append(item.text.strip())
    print(curriculum)
