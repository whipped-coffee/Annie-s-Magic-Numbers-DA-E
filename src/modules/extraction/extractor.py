import os
from typing import Literal
from .adapter import APIClient

class Extractor:
    def __init__(self):
        self.adapter = APIClient("https://www.pwc.com/us/en/careers/university_relations/data_analytics_cases_studies/")
        self.available_data = {
            "purchases": "PurchasesFINAL12312016csv.zip",
            "sales": "SalesFINAL12312016csv.zip"
        }
        self.purchases = self.download_and_save_zip("purchases")
        self.sales = self.download_and_save_zip("sales")

    def download_and_save_zip(self, data_type: Literal["purchases", "sales"]) -> str:
        """Download and save a ZIP file from a URL"""
        try:
            response = self.adapter.make_get_request(self.available_data[data_type])
            response.raise_for_status()
            
            os.makedirs("data", exist_ok=True)
            zip_path = os.path.join("data", self.available_data[data_type])
            
            with open(zip_path, "wb") as f:
                f.write(response.content)
                
            print(f"Successfully saved ZIP to: {zip_path}", flush=True)
            return zip_path
        except Exception as e:
            print(f"Error downloading/saving ZIP file: {e}", flush=True)
            raise
