import os
import random
import logging
from faker import Faker
import psycopg2
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://shop:admin@localhost:5433/shop')

# Sample data
BRANDS = [
    "Nike", "Adidas", "Apple", "Samsung", "Sony", "Dell", "HP", "Lenovo",
    "Canon", "Nikon", "Levi's", "Zara", "H&M", "Puma", "Reebok"
]

CATEGORIES = [
    ("Electronics", "Electronic devices and accessories"),
    ("Clothing", "Men's and women's clothing"),
    ("Shoes", "Footwear for all occasions"),
    ("Accessories", "Jewelry, watches, and other accessories"),
    ("Home & Garden", "Home decor and garden supplies"),
    ("Sports & Outdoors", "Sports equipment and outdoor gear"),
    ("Beauty & Personal Care", "Cosmetics and personal care products"),
    ("Toys & Games", "Toys, games, and entertainment")
]

PRODUCT_NAMES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smart Watch", "Tablet", "Camera", "Gaming Console", "Bluetooth Speaker"],
    "Clothing": ["T-Shirt", "Jeans", "Dress", "Jacket", "Hoodie", "Sweater", "Shorts", "Skirt"],
    "Shoes": ["Running Shoes", "Sneakers", "Boots", "Sandals", "Formal Shoes", "Basketball Shoes", "Hiking Boots"],
    "Accessories": ["Watch", "Necklace", "Backpack", "Sunglasses", "Wallet", "Belt", "Hat"],
    "Home & Garden": ["Lamp", "Rug", "Chair", "Table", "Bedding Set", "Curtains", "Wall Art"],
    "Sports & Outdoors": ["Yoga Mat", "Dumbbell Set", "Tent", "Bicycle", "Basketball", "Soccer Ball", "Tennis Racket"],
    "Beauty & Personal Care": ["Perfume", "Moisturizer", "Lipstick", "Shampoo", "Hair Dryer", "Electric Razor"],
    "Toys & Games": ["Board Game", "Lego Set", "Action Figure", "Doll", "Puzzle", "Remote Control Car"]
}

def create_connection():
    """Create a database connection."""
    try:
        logger.info(f"Attempting to connect to database at: {DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL)
        logger.info("Successfully connected to the database")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        logger.error(f"Connection string used: {DATABASE_URL}")
        logger.error("Please verify that:")
        logger.error("1. PostgreSQL is running")
        logger.error("2. The connection details in your .env file are correct")
        logger.error("3. The database 'shop' exists and the user has proper permissions")
        logger.error("4. The port number is correct (5433 as per your docker-compose)")
        logger.error("5. If using Docker, the container is running (check with 'docker ps')")
        return None
        return None

def populate_brands(conn):
    """Populate the brand table."""
    cursor = conn.cursor()
    try:
        for i, brand_name in enumerate(BRANDS, 1):
            cursor.execute(
                "INSERT INTO brand (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                (i, brand_name)
            )
        conn.commit()
        logger.info(f"Inserted {len(BRANDS)} brands.")
        return len(BRANDS)
    except Exception as e:
        conn.rollback()
        logger.error(f"Error populating brands: {e}")
        return 0

def populate_categories(conn):
    """Populate the category table."""
    cursor = conn.cursor()
    try:
        for i, (name, description) in enumerate(CATEGORIES, 1):
            cursor.execute(
                """
                INSERT INTO category (id, display_text, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (i, name, description)
            )
        conn.commit()
        logger.info(f"Inserted {len(CATEGORIES)} categories.")
        return len(CATEGORIES)
    except Exception as e:
        conn.rollback()
        logger.error(f"Error populating categories: {e}")
        return 0

def populate_products(conn, num_products=100):
    """Populate the product table."""
    cursor = conn.cursor()

    # Get all category IDs
    cursor.execute("SELECT id, display_text FROM category")
    categories = cursor.fetchall()

    if not categories:
        logger.error("No categories found. Please run populate_categories first.")
        return 0

    # Get all brand IDs
    cursor.execute("SELECT id FROM brand")
    brand_ids = [row[0] for row in cursor.fetchall()]

    if not brand_ids:
        logger.error("No brands found. Please run populate_brands first.")
        return 0

    try:
        for i in range(1, num_products + 1):
            # Select a random category
            category_id, category_name = random.choice(categories)

            # Generate product data
            product_type = random.choice(PRODUCT_NAMES[category_name])
            product_name = f"{random.choice(BRANDS)} {product_type} {fake.bothify(text='####')}"
            description = fake.paragraph(nb_sentences=3)
            sku = fake.bothify(text='???-########', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            small_image = f"https://picsum.photos/200/200?random={i}"
            out_of_stock = random.choice([True, False])
            brand_id = random.choice(brand_ids)

            cursor.execute(
                """
                INSERT INTO product (id, name, description, sku, small_image, out_of_stock, category_id, brand_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (i, product_name, description, sku, small_image, out_of_stock, category_id, brand_id)
            )

            if i % 10 == 0:
                conn.commit()
                logger.info(f"Inserted {i} products...")

        conn.commit()
        logger.info(f"Inserted {num_products} products.")
        return num_products
    except Exception as e:
        conn.rollback()
        logger.error(f"Error populating products: {e}")
        return 0

def clear_tables(conn):
    """Delete all records from all tables in the correct order to maintain referential integrity."""
    cursor = conn.cursor()
    try:
        # Disable foreign key checks temporarily
        cursor.execute("SET session_replication_role = 'replica';")

        # Clear tables in reverse order of dependencies
        tables = ["product", "brand", "category"]

        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
            logger.info(f"Cleared table: {table}")

        # Re-enable foreign key checks
        cursor.execute("SET session_replication_role = 'origin'")
        conn.commit()
        logger.info("All tables have been cleared successfully.")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Error clearing tables: {e}")
        return False

def main():
    """Main function to populate the database."""
    logger.info("Starting database population...")

    conn = create_connection()
    if not conn:
        logger.error("Failed to connect to the database.")
        return

    # Clear all tables before populating
    logger.info("Clearing existing data...")
    if not clear_tables(conn):
        logger.error("Failed to clear tables. Exiting...")
        conn.close()
        return

    try:
        # Populate tables
        brand_count = populate_brands(conn)
        category_count = populate_categories(conn)
        product_count = populate_products(conn, num_products=200)

        logger.info("- Database population completed!")
        logger.info(f"- Brands: {brand_count}")
        logger.info(f"- Categories: {category_count}")
        logger.info(f"- Products: {product_count}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    main()
