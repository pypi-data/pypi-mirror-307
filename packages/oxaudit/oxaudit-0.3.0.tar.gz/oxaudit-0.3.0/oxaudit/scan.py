import requests

def scan_contract(file_path):
    url = "https://fastapi-oxaudit-app-u80l.onrender.com/scan_contract/"

    # Open the contract file and send it to the FastAPI endpoint
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file, 'application/octet-stream')}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raises an error if the status code is not 200
            return response.json()  # Return the JSON response from the server
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
