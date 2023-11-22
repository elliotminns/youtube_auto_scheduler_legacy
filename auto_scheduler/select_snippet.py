# This script selects which title, description, and tags should be used for the video being uploaded.

import random

def select_random_line(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return random.choice(lines).strip()  # Randomly select a line and remove leading/trailing whitespace

def select_random_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        all_tags = file.read().split(',')
        # Remove whitespace around each tag using strip(), then filter out empty strings if any
        tags = [tag.strip() for tag in all_tags if tag.strip()]
        return random.sample(tags, k=random.randint(1, 32))  # Select random tags as an array

def upload_random_video():
    title = select_random_line('resources/title_descriptions.txt')
    tags = select_random_tags('resources/tags.txt')

    # Example placeholder print to show the selected title and description
    return title, tags
