# Animal Website Generator

Generates a static HTML page listing animals fetched from the API Ninjas.

## Description

Animal Web Generator is a simple Python CLI tool that:

* Prompts the user for an animal name (e.g. "Fox").
* Fetches data for the given animal from the API Ninjas.
* Generates a static HTML file (`animals.html`) displaying the retrieved information.

This modular project separates data retrieval from site generation, making it easy to swap or extend data sources.

## Features

* Interactive CLI prompt for animal names.
* Modular architecture:

  * `data_fetcher.py`: handles all data retrieval (API calls, JSON files, etc.).
  * `animals_web_generator.py`: generates the HTML page based on fetched data.
* Graceful error handling:

  * Exits cleanly on missing API key or template file.
  * Displays friendly message in the HTML if an animal doesn’t exist.

## Requirements

* Python 3.6+
* Dependencies listed in [requirements.txt](requirements.txt)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/animal-web-generator.git
   cd animal-web-generator
   ```

2. **(Optional) Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials** Create a `.env` file in the project root:

   ```ini
   API_KEY=your_api_key_here
   ```

## Usage

Run the generator script:

```bash
python3 animals_web_generator.py
```

1. Enter an animal name when prompted (e.g. `Fox`).
2. The script creates `animals.html` in the project root.
3. Open `animals.html` in your browser to view the results.

## File Structure

```
.
├── data_fetcher.py            # Module for fetching animal data
├── animals_web_generator.py   # CLI and HTML generator
├── animals_template.html      # Base HTML template with placeholder
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview and instructions
└── .env                       # Environment variables (excluded from VCS)
```

## Contributing

Contributions are welcome! To get started:

1. Fork this repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Implement your changes and ensure PEP8 compliance.
4. Commit your work with descriptive messages:

   ```bash
   git commit -m "Add feature XYZ"
   ```
5. Push to your branch and open a Pull Request.

Please follow existing code style and write clear, concise commit messages.

## License

This project is licensed under the MIT License.
