# Animal Sales Application

## Overview

The Animal Sales Application is a Python-based GUI tool designed to assist pet shops or animal breeders in managing sales and inventory. It uses image recognition to identify animal characteristics and matches them against a database of previous sales, helping to price new animals or find similar past sales.

## Features

- Image analysis for animal identification
- Customer selection and management
- Database searching with tiered matching (breed first, then coat characteristics)
- Order form population from image analysis or database matches
- Mock order saving functionality

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- SQLite3
- Tkinter (usually comes with Python)
- Pillow (PIL Fork) for image processing
- An Ollama server running with the llava:34b model for image analysis

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/animal-sales-application.git
   cd animal-sales-application
   ```

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Ensure you have SQLite installed on your system.

4. Set up the Ollama server with the llava:34b model. Follow the instructions on the [Ollama website](https://ollama.ai/) for installation and model setup.

## File Structure

- `main.py`: The main application script with GUI implementation
- `database_operations.py`: Handles all database-related operations
- `image_analysis.py`: Manages image analysis using the Ollama API
- `models.py`: Contains Pydantic models for data structures
- `animal_sales.db`: SQLite database file (you need to create this with appropriate schema)

## Usage

1. Start the Ollama server with the llava:34b model.

2. Run the main application:

   ```
   python main.py
   ```

3. Use the GUI to:
   - Select a customer from the dropdown (or leave as "Any")
   - Click "Select Image" to choose an animal image for analysis
   - View matching sales results in the treeview
   - Double-click a result to populate the order form
   - Manually edit the order form as needed
   - Click "Save Order" to (mock) save the order

## Database Schema

The `animal_sales` table should have the following structure:

```sql
CREATE TABLE animal_sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    species TEXT,
    breed TEXT,
    size TEXT,
    weight REAL,
    coat_length TEXT,
    coat_color TEXT,
    price REAL,
    client_name TEXT,
    client_email TEXT
);
```

Ensure your `animal_sales.db` file is set up with this schema before running the application.

## Contributing

Contributions to the Animal Sales Application are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - sdgwynn@gmail.com

Project Link: [https://github.com/shiftbug/catsanddogs](https://github.com/shiftbug/catsanddogs)

## Acknowledgements

- [Ollama](https://ollama.ai/) for providing the image analysis model
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- [SQLite](https://www.sqlite.org/index.html) for the database engine
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation and settings management
