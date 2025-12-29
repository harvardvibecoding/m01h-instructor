import requests
import json

# Read API key from file
try:
    with open("MyApiKey.txt", "r") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print("Error: MyApiKey.txt file not found.")
    exit(1)

def fetch_random_dog():
    """Fetch a random dog image from thedogapi.com and save it."""
    
    url = "https://api.thedogapi.com/v1/images/search"
    
    headers = {
        "x-api-key": API_KEY
    }
    
    try:
        # Fetch a random dog image
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        if data:
            image_url = data[0]["url"]
            print(f"Fetched image URL: {image_url}")
            
            # Download the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save the image
            with open("random_dog.jpg", "wb") as f:
                f.write(image_response.content)
            
            print("Image saved as random_dog.jpg")
        else:
            print("No image data received from API")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")

if __name__ == "__main__":
    fetch_random_dog()
