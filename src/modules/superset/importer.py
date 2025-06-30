import os
import json
import time
import requests

class SupersetImporter:
    def __init__(self, dashboard_path: str):
        self.base_url = "http://superset:8088"
        self.session = requests.Session()
        self.username = os.getenv("SUPERSET_USERNAME", "annie")
        self.password = os.getenv("SUPERSET_PASSWORD", "annieMagicWord")
        self.wait_for_service()
        self.get_superset_access_token()
        self.get_csrf_token()
        
        if os.path.exists(dashboard_path):
            self.import_dashboard(dashboard_path)
        else:
            print(f"Warning: Dashboard file not found at {dashboard_path}", flush=True)
        
    def wait_for_service(
        self, 
        max_retries: int = 30, 
        delay: int = 10
    ):
        """Wait for a service to be available"""
        for attempt in range(max_retries):
            try:
                endpoint = "/health"
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url)
                if response.status_code == 200:
                    print(f"Service at {self.base_url} is up!", flush=True)
                    return True
            except requests.exceptions.RequestException:
                pass
            print(f"Service at {self.base_url} not ready. Attempt {attempt + 1}/{max_retries}", flush=True)
            time.sleep(delay)
        raise Exception(f"Service at {self.base_url} did not become available after {max_retries} attempts")
        
    def get_superset_access_token(self):
        # Authenticate and get access token
        endpoint = "/api/v1/security/login"
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(
            url,
            json={
                "username": self.username,
                "password": self.password,
                "provider": "db",
                "refresh": True
            },
        )
        if response.status_code != 200:
            raise Exception(f"Got HTTP code of {response.status_code} from {url}; expected 200")
        access_token = response.json()["access_token"]
        print("Received access token")
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })
    
    def get_csrf_token(self):
        endpoint = "/api/v1/security/csrf_token/"  # Trailing slash required to avoid redirect"
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception(f"Got HTTP code of {response.status_code} from {url}; expected 200")
        token = response.json()["result"]
        print("Received CSRF token")
        self.session.headers.update({
            "X-CSRFToken": token
        })
    
    def import_dashboard(self, zip_file_path : str):
        endpoint = "/api/v1/dashboard/import/"
        url = f"{self.base_url}{endpoint}"
        
        with open(zip_file_path, 'rb') as infile:
            files = {'formData': ('dashboard.zip', infile.read(), 'application/zip')}
        
        database_password = os.getenv("POSTGRES_PASSWORD", "annieMagicWord")
        payload={
            'passwords': (None, json.dumps({"databases/PostgreSQL.yaml": database_password})),
            'overwrite': 'true'
        }
        
        response = self.session.post(
            url,
            files=files,
            data=payload
        )
        
        response.raise_for_status()

        print("Dashboard imported successfully")
    