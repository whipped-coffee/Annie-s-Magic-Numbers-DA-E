import os
import time
from sqlalchemy import create_engine, text
from ..transformation import Transformer
from .mviews_constants import drop_views, sales_with_costs_view, product_margins_view

class Loader:
    def __init__(self, transformer: Transformer):
        self.engine = self.get_database_connection()
        self.transformer = transformer
        self.load_data()

    def get_database_connection(self):
        """Get database connection with retries"""
        max_retries = 5
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                # Get connection params from environment variables
                db_user = os.getenv('POSTGRES_USER', 'annie')
                db_pass = os.getenv('POSTGRES_PASSWORD', 'annieMagicWord')
                db_host = os.getenv('POSTGRES_HOST', 'db')
                db_name = os.getenv('POSTGRES_DB', 'liquor')
                
                engine = create_engine(f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}")
                # Test the connection
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return engine
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...", flush=True)
                time.sleep(retry_delay)

    def load_data(self):
        """Load data into database"""
        print("Loading data into database...")
        self.drop_materialized_views()
        self.transformer.df_purchases.to_sql("purchases", self.engine, if_exists="replace", index=False)
        self.transformer.df_sales.to_sql("sales", self.engine, if_exists="replace", index=False)
        self.create_materialized_views()

    def create_materialized_views(self):
        """Create materialized views for analysis"""
        with self.engine.connect() as connection:
            # Create sales with costs view
            connection.execute(sales_with_costs_view)
            # Create product margins view
            connection.execute(product_margins_view)
            
            connection.commit()

    def drop_materialized_views(self):
        """Create materialized views for analysis"""
        with self.engine.connect() as connection:
            # Create sales with costs view
            connection.execute(drop_views)
            connection.commit()