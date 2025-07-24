# E-Commerce Dummy Data Generator

This project provides a simple Python script to generate and populate an e-commerce database with realistic dummy data. It's perfect for testing and development purposes.

## Features

- Generates realistic e-commerce data including:
  - Brands (15+ popular brands)
  - Categories (8 main categories with descriptions)
  - Products (200+ products with images, descriptions, and SKUs)
- Automatically clears existing data before populating
- Uses PostgreSQL as the database
- Configurable through environment variables
- Detailed logging for monitoring the population process

## Prerequisites

- Python 3.7+
- PostgreSQL server
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd e-commerce-dummy-data
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your database configuration:

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database
   ```

## Usage

1. Make sure your PostgreSQL server is running and the database exists.

2. Run the population script:

   ```bash
   python populate_db.py
   ```

3. The script will:
   - Clear all existing data from the database
   - Populate brands, categories, and products
   - Show progress in the console

## Database Schema

The script populates the following tables:

- `brand`: Contains brand information
- `category`: Product categories with descriptions
- `product`: Product details with references to brands and categories

## Configuration

You can customize the script's behavior by editing the following constants in `populate_db.py`:

- `BRANDS`: List of brand names
- `CATEGORIES`: List of categories with descriptions
- `PRODUCT_NAMES`: Dictionary of product names by category

## Logging

The script uses Python's built-in `logging` module with the following log levels:

- `INFO`: General progress information
- `ERROR`: Error conditions

Logs are output to the console with timestamps and log levels.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the GitHub repository.
