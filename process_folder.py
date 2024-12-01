import requests

# Path to the image to upload
image_path = "./sample.jpeg"  # Replace with your image path

# Flask server URL
url = "http://127.0.0.1:5000/upload"

# Send the image to the Flask server
with open(image_path, "rb") as img_file:
    response = requests.post(url, files={"image": img_file})

# Check the response
if response.status_code == 200:
    data = response.json()
    base64_image = data.get("image_with_visualizations")

    # Save the base64 response to a file
    with open("output_image_base64.txt", "w") as file:
        file.write(base64_image)

    print("Image processed successfully! Saved base64 result to output_image_base64.txt.")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
