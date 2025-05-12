import json

def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)

def main():
    animals_data = load_data('animals_data.json')

    for animal in animals_data:
        # Name
        name = animal.get('name')
        if name:
            print(f"Name: {name}")

        # Diet
        diet = animal.get('characteristics', {}).get('diet')
        if diet:
            print(f"Diet: {diet}")

        # First location
        locations = animal.get('locations', [])
        if locations:
            print(f"Location: {locations[0]}")

        # Type
        animal_type = animal.get('characteristics', {}).get('type')
        if animal_type:
            print(f"Type: {animal_type}")

        # Leerzeile zwischen den Einträgen
        print()

if __name__ == "__main__":
    main()
