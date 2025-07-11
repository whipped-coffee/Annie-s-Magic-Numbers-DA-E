from modules.extraction import Extractor
from modules.transformation import Transformer
from modules.loading import Loader
from modules.superset import SupersetImporter

def main():
    try:
        extractor = Extractor()
        transformer = Transformer(extractor)
        Loader(transformer)
        print("ETL process completed successfully!", flush=True)
        
        SupersetImporter("/app/dashboards/dashboard_export_20250630T172417.zip")
        print("Superset dashboard imported successfully!", flush=True)
        
    except Exception as e:
        print(f"Error during process: {e}", flush=True)
        raise

if __name__ == "__main__":
    main()