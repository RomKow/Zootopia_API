import json

def load_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def serialize_animal(animal):
    """
    Serializes a single animal record to HTML.
    Returns an <li> block in the desired format.
    """
    output = '    <li class="cards__item">\n'

    # Title with name
    name = animal.get("name")
    if name:
        output += f'      <div class="card__title">{name}</div>\n'

    # Open the text section
    output += '      <p class="card__text">\n'

    # Diet
    diet = animal.get("characteristics", {}).get("diet")
    if diet:
        output += f'        <strong>Diet:</strong> {diet}<br/>\n'

    # Location (joined with ' and ')
    locations = animal.get("locations", [])
    if locations:
        locs = " and ".join(locations)
        output += f'        <strong>Location:</strong> {locs}<br/>\n'

    # Type
    animal_type = animal.get("characteristics", {}).get("type")
    if animal_type:
        output += f'        <strong>Type:</strong> {animal_type}<br/>\n'

    # Close the text section and li
    output += '      </p>\n'
    output += '    </li>\n'

    return output

def main():
    # 1. Read the template
    with open("animals_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 2. Load data
    animals_data = load_data("animals_data.json")

    # 3. Generate HTML for all animals
    animals_html = ""
    for animal in animals_data:
        animals_html += serialize_animal(animal)

    # 4. Replace placeholder in template
    result = template.replace("__REPLACE_ANIMALS_INFO__", animals_html)

    # 5. Write the result
    with open("animals.html", "w", encoding="utf-8") as f:
        f.write(result)

    # print("animals.html has been generated. Open it in the browser to view.")

if __name__ == "__main__":
    main()
