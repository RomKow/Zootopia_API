"""
Generates an HTML list of animals using the API Ninjas.
"""

import os
import sys
from urllib.parse import urlsplit, urlunsplit

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
_RAW_URL = os.getenv('API_URL', 'https://api.api-ninjas.com/v1/animals')
_split = urlsplit(_RAW_URL)
API_URL = urlunsplit((_split.scheme, _split.netloc, _split.path, '', ''))
HEADERS = {'X-Api-Key': API_KEY} if API_KEY else {}

TEMPLATE_PATH = 'animals_template.html'
OUTPUT_PATH = 'animals.html'


def load_template(path):
    """Load the HTML template from the given file path."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        sys.exit(f'Template file not found: {path}')


def write_output(path, content):
    """Write the generated HTML content to the specified output file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        sys.exit(f'Error writing output file: {e}')


def fetch_animal(name):
    """
    Fetch information about the given animal name from the API.
    Returns the JSON-decoded response.
    """
    if not API_KEY:
        raise RuntimeError('API_KEY is not defined in .env')

    params = {'name': name}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise RuntimeError(f'HTTP error: {err}. Response: {response.text}')

    return response.json()


def serialize_animal(animal):
    """
    Serialize a single animal record to an HTML <li> block.
    """
    lines = ['    <li class="cards__item">']

    name = animal.get('name')
    if name:
        lines.append(f'      <div class="card__title">{name}</div>')

    lines.append('      <p class="card__text">')

    diet = animal.get('characteristics', {}).get('diet')
    if diet:
        lines.append(f'        <strong>Diet:</strong> {diet}<br/>')

    locations = animal.get('locations', [])
    if locations:
        locs = ' and '.join(locations)
        lines.append(f'        <strong>Location:</strong> {locs}<br/>')

    animal_type = animal.get('characteristics', {}).get('type')
    if animal_type:
        lines.append(f'        <strong>Type:</strong> {animal_type}<br/>')

    lines.append('      </p>')
    lines.append('    </li>')

    return '\n'.join(lines) + '\n'


def main():
    """
    Prompt the user for an animal name, fetch data, and generate the HTML page.
    """
    name = input('Enter a name of an animal: ').strip()
    if not name:
        sys.exit('No animal name provided.')

    template = load_template(TEMPLATE_PATH)

    try:
        data = fetch_animal(name)
    except Exception as e:
        sys.exit(f"Error fetching '{name}': {e}")

    animals = data if isinstance(data, list) else [data]

    if not animals:
        # Generate a friendly message if no animals are found
        animals_html = f'<h2>The animal "{name}" does not exist.</h2>\n'
    else:
        animals_html = ''.join(serialize_animal(a) for a in animals)

    result_html = template.replace('__REPLACE_ANIMALS_INFO__', animals_html)

    write_output(OUTPUT_PATH, result_html)
    print(f'Website was successfully generated to the file {OUTPUT_PATH}.')


if __name__ == '__main__':
    main()
