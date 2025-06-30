import os
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from ..extraction import Extracter

class Transformer:
    def __init__(self, extracter: Extracter):
        self.extracter = extracter
        self.df_purchases = self.process_purchases(extracter.purchases)
        self.df_sales = self.process_sales(extracter.sales, self.df_purchases["inventory_id"])

    def get_first_csv_from_zip(self, file_path: str) -> BytesIO:
        """Extract first CSV from ZIP file"""
        try:
            with ZipFile(file_path, 'r') as zip_file:
                for filename in zip_file.namelist():
                    if filename.lower().endswith('.csv'):
                        with zip_file.open(filename) as csv_file:
                            return BytesIO(csv_file.read())
                raise ValueError("No CSV file found in ZIP archive.", flush=True)
        except Exception as e:
            print(f"Error extracting CSV from ZIP: {e}", flush=True)
            raise

    def process_purchases(self, zip_path: str) -> pd.DataFrame:
        """Process purchases data"""
        csv_buffer = self.get_first_csv_from_zip(zip_path)
        df = pd.read_csv(csv_buffer)
        
        # Keep only unique inventory IDs with their purchase price
        df = df[["InventoryId", "PurchasePrice"]].drop_duplicates(subset="InventoryId")
        
        # Rename columns to snake_case
        df = df.rename(columns={
            "InventoryId": "inventory_id",
            "PurchasePrice": "purchase_price"
        })
        
        return df

    def process_sales(self, zip_path: str, unique_inventory_ids: pd.Series) -> pd.DataFrame:
        """Process sales data"""
        csv_buffer = self.get_first_csv_from_zip(zip_path)
        df = pd.read_csv(csv_buffer)
        
        # Filter sales for inventory IDs we have purchase prices for
        df = df[df["InventoryId"].isin(unique_inventory_ids)]
        
        # Take a sample due to memory constraints
        df = df.sample(n=int(os.getenv("SALES_ENTRIES_LIMIT", 1_000_000)), random_state=42)
        
        # Drop unnecessary columns
        df = df.drop(columns=["Description", "Size", "Classification", "VendorNo"])
        
        # Convert date
        df["SalesDate"] = pd.to_datetime(df["SalesDate"])
        
        # Rename columns to snake_case
        df = df.rename(columns={
            "InventoryId": "inventory_id",
            "Store": "store",
            "Brand": "brand",
            "SalesDate": "sale_date",
            "SalesPrice": "sale_price",
            "SalesDollars": "sale_amount",
            "Volume": "product_volume",
            "ExciseTax": "excise_tax",
            "VendorName": "vendor_name",
            "SalesQuantity": "sale_quantity"
        })
        
        return df