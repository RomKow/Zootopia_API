import json

def load_data(file_path):
    """Loads a JSON file and returns its content."""
    with open(file_path, "r") as handle:
        return json.load(handle)

def main():
    # 1. Template einlesen
    with open('animals_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # 2. Daten aus JSON laden und String aufbauen
    animals_data = load_data('animals_data.json')
    output = ''
    for animal in animals_data:
        # Name
        name = animal.get('name')
        if name:
            output += f"Name: {name}\n"
        # Diet
        diet = animal.get('characteristics', {}).get('diet')
        if diet:
            output += f"Diet: {diet}\n"
        # First Location
        locations = animal.get('locations', [])
        if locations:
            output += f"Location: {locations[0]}\n"
        # Type
        animal_type = animal.get('characteristics', {}).get('type')
        if animal_type:
            output += f"Type: {animal_type}\n"
        # Leerzeile zwischen Einträgen
        output += "\n"

    # 3. Platzhalter ersetzen
    filled = template.replace('__REPLACE_ANIMALS_INFO__', output)

    # 4. Neue HTML schreiben
    with open('animals.html', 'w', encoding='utf-8') as f:
        f.write(filled)

    print("animals.html wurde erzeugt. Im Browser öffnen, um das Ergebnis zu sehen.")

if __name__ == "__main__":
    main()
