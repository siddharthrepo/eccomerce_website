import csv
import requests
from django.core.files.base import ContentFile
from vendor.models import Vendor
from store.models import Product


csv_file_path = '/home/siddharth/Desktop/Django_dev/Django_Ecommerce_app/backup/description.csv'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Map CSV columns to model fields
        product = Product(
            name=row['ProductName'],
            price=row['Price'],
            discounted_price=row.get('DiscountPrice'),
            inventory=row['Quantity'],
            Brand = row['Brand'],
            # digital=row['digital'] == 'True',  # Convert to Boolean
            catgory=row.get('Category'),
            sub_catgory=row.get('SubCategory'),
            description = row.get('description'),
        )

        # Associate a default vendor if needed
        default_vendor = Vendor.objects.get(email = "shiv@g.com")  # Replace with your logic
        if default_vendor:
            product.vendor = default_vendor

        # Handle image URL if provided
        if row.get('Image_Url'):
            try:
                response = requests.get(row['Image_Url'] , headers=headers)
                response.raise_for_status()  # Ensure the request was successful
                # Extract the image file name from the URL
                image_name = row['Image_Url'].split('/')[-1]
                # Save the image to the product model
                product.image.save(image_name, ContentFile(response.content), save=False)
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch image for {row['ProductName']}: {e}")

        # Save the product to the database
        # print("worked successfully!")
        # break
        product.save()

print("Products imported successfully!")