#!/usr/bin/env python3
"""
Generiert eine HTML-Liste von Tieren über die API Ninjas.
"""

import argparse
import sys
import os
from urllib.parse import urlsplit, urlunsplit

import requests
from dotenv import load_dotenv

# .env laden
load_dotenv()

API_KEY = os.getenv('API_KEY')
_RAW_URL = os.getenv('API_URL', 'https://api.api-ninjas.com/v1/animals')
_split = urlsplit(_RAW_URL)
API_URL = urlunsplit((_split.scheme, _split.netloc, _split.path, '', ''))
HEADERS = {'X-Api-Key': API_KEY} if API_KEY else {}

TEMPLATE_PATH = 'animals_template.html'
OUTPUT_PATH = 'animals.html'


def parse_args():
    """Liest die Tiernamen von der Kommandozeile ein."""
    parser = argparse.ArgumentParser(
        description='Generiert eine HTML-Liste von Tieren über die API.'
    )
    parser.add_argument(
        'names',
        nargs='*',
        default=['Fox'],
        help='Liste der Tiernamen, z. B.: Fox Lion Elephant (Default: Fox)',
    )
    return parser.parse_args()


def load_template(path):
    """Lädt das HTML-Template."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        sys.exit(f'Template-Datei nicht gefunden: {path}')


def write_output(path, content):
    """Schreibt das generierte HTML in die Ausgabedatei."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        sys.exit(f'Fehler beim Schreiben der Ausgabedatei: {e}')


def fetch_animal(name):
    """
    Ruft Informationen zum Tier 'name' von der API ab.
    Gibt das JSON-dekodierte Ergebnis zurück.
    """
    if not API_KEY:
        raise RuntimeError('API_KEY nicht in der .env definiert')

    params = {'name': name}
    response = requests.get(API_URL, headers=HEADERS, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as err:
        raise RuntimeError(f'HTTP-Fehler: {err}. Antwort: {response.text}')

    return response.json()


def serialize_animal(animal):
    """
    Serialisiert einen einzelnen Tier-Datensatz zu einem HTML-<li>-Block.
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
    args = parse_args()
    template = load_template(TEMPLATE_PATH)

    animals_data = []
    for name in args.names:
        try:
            data = fetch_animal(name)
        except Exception as e:
            print(f"Fehler beim Abrufen von '{name}': {e}", file=sys.stderr)
            continue

        if isinstance(data, list):
            animals_data.extend(data)
        else:
            animals_data.append(data)

    animals_html = ''.join(serialize_animal(a) for a in animals_data)
    result_html = template.replace('__REPLACE_ANIMALS_INFO__', animals_html)

    write_output(OUTPUT_PATH, result_html)
    print(f'{OUTPUT_PATH} wurde erfolgreich erstellt.')


if __name__ == '__main__':
    main()
