from flask import Flask, render_template_string, jsonify
import os
from dog import fetch_random_dog

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dog Image Fetcher</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .image-container {
            margin: 30px 0;
            min-height: 400px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f5f5f5;
            border-radius: 15px;
            overflow: hidden;
        }
        
        #dogImage {
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            object-fit: cover;
        }
        
        .loading {
            color: #667eea;
            font-size: 1.2em;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            font-weight: 600;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        .error {
            color: #e74c3c;
            padding: 15px;
            background: #fadbd8;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐕 Dog Image Fetcher</h1>
        <p class="subtitle">Click the button to fetch a random dog image</p>
        
        <div class="image-container">
            <div id="content">
                <p style="color: #999;">No image loaded yet. Click the button below!</p>
            </div>
        </div>
        
        <button id="fetchBtn" onclick="fetchDogImage()">Fetch Dog Image</button>
        
        <div class="error" id="errorMsg"></div>
    </div>
    
    <script>
        async function fetchDogImage() {
            const button = document.getElementById('fetchBtn');
            const content = document.getElementById('content');
            const errorMsg = document.getElementById('errorMsg');
            
            // Clear previous error
            errorMsg.classList.remove('show');
            
            // Disable button and show loading state
            button.disabled = true;
            content.innerHTML = '<div class="spinner"></div><p class="loading">Fetching a random dog...</p>';
            
            try {
                const response = await fetch('/fetch-dog');
                const data = await response.json();
                
                if (data.success) {
                    // Display the image
                    const img = document.createElement('img');
                    img.id = 'dogImage';
                    img.src = data.image_url;
                    img.onload = function() {
                        content.innerHTML = '';
                        content.appendChild(img);
                    };
                    img.onerror = function() {
                        errorMsg.textContent = 'Failed to load the image.';
                        errorMsg.classList.add('show');
                        content.innerHTML = '<p style="color: #999;">No image loaded yet. Click the button below!</p>';
                    };
                } else {
                    errorMsg.textContent = data.error || 'An error occurred while fetching the dog image.';
                    errorMsg.classList.add('show');
                    content.innerHTML = '<p style="color: #999;">No image loaded yet. Click the button below!</p>';
                }
            } catch (error) {
                errorMsg.textContent = 'Failed to fetch image. Please try again.';
                errorMsg.classList.add('show');
                content.innerHTML = '<p style="color: #999;">No image loaded yet. Click the button below!</p>';
            } finally {
                button.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/fetch-dog')
def fetch_dog():
    """Fetch a random dog image and return the URL."""
    try:
        # Call the fetch_random_dog function from dog.py
        fetch_random_dog()
        
        # Read the image and get its URL from the API response
        # Since fetch_random_dog doesn't return the URL, we'll call the API directly
        import requests
        from dog import API_KEY
        
        url = "https://api.thedogapi.com/v1/images/search"
        headers = {
            "x-api-key": API_KEY
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data:
            image_url = data[0]["url"]
            return jsonify({
                "success": True,
                "image_url": image_url
            })
        else:
            return jsonify({
                "success": False,
                "error": "No image data received from API"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
