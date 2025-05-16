# animals_web_generator.py
"""
Module responsible for generating the website from animal data.
Depends on data_fetcher for data retrieval; agnostic to source.
"""

import sys
import data_fetcher


def load_template(path):
    """Load the HTML template from file."""
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
    Prompt the user for an animal name, fetch via data_fetcher, and generate the HTML page.
    """
    animal_name = input('Please enter an animal: ').strip()
    if not animal_name:
        sys.exit('No animal name provided.')

    template = load_template('animals_template.html')

    try:
        animals = data_fetcher.fetch_data(animal_name)
    except Exception as e:
        sys.exit(f"Error fetching '{animal_name}': {e}")

    if not animals:
        animals_html = f'<h2>The animal "{animal_name}" does not exist.</h2>\n'
    else:
        animals_html = ''.join(serialize_animal(a) for a in animals)

    result_html = template.replace('__REPLACE_ANIMALS_INFO__', animals_html)
    write_output('animals.html', result_html)
    print('Website was successfully generated to the file animals.html.')


if __name__ == '__main__':
    main()
