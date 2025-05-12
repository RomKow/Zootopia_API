import json

def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)

def main():
    # Template einlesen
    with open('animals_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # JSON laden
    animals_data = load_data('animals_data.json')
    output = ''
    for animal in animals_data:
        name = animal.get('name')
        diet = animal.get('characteristics', {}).get('diet')
        locations = animal.get('locations', [])
        animal_type = animal.get('characteristics', {}).get('type')

        # li starten
        output += '    <li class="cards__item">\n'
        # Titel
        if name:
            output += f'      <div class="card__title">{name}</div>\n'
        # Text-Block starten
        output += '      <p class="card__text">\n'
        # Diet
        if diet:
            output += f'          <strong>Diet:</strong> {diet}<br/>\n'
        # Location (mit " and " verknüpfen)
        if locations:
            locs = ' and '.join(locations)
            output += f'          <strong>Location:</strong> {locs}<br/>\n'
        # Type
        if animal_type:
            output += f'          <strong>Type:</strong> {animal_type}<br/>\n'
        # Text-Block und li schließen
        output += '      </p>\n'
        output += '    </li>\n'

    # Platzhalter ersetzen und schreiben
    filled = template.replace('__REPLACE_ANIMALS_INFO__', output)
    with open('animals.html', 'w', encoding='utf-8') as f:
        f.write(filled)

    print("animals.html wurde mit neuem Layout erzeugt.")

if __name__ == "__main__":
    main()
