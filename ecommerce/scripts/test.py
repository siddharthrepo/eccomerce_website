import requests
from django.core.files.base import ContentFile
from store.models import Product

image_url = "https://www.bigbasket.com/media/uploads/p/l/40075537_5-fresho-onion.jpg"

# Use headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    # Clean the URL (remove any appended invalid characters)
    image_url = image_url.split(',')[0]  

    # Make the request
    response = requests.get(image_url, headers=headers, timeout=10)
    response.raise_for_status()  # Check for HTTP errors

    # Save the image to the product model
    product = Product(name="Test Product", price=100, inventory=10)
    product.image.save("test_image.jpg", ContentFile(response.content), save=True)
    print("Image downloaded and saved successfully!")
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch image: {e}")
