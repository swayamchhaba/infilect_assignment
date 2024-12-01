import requests

# Step 1: Send POST request to Flask server with an image
url = "http://127.0.0.1:5000/upload"  # Replace with your Flask server URL
files = {"image": open("sample.jpeg", "rb")}  # Replace with your image path

response = requests.post(url, files=files)

# Check if the response is successful
if response.status_code == 200:
    print("Request Successful!")

    # Step 2: Extract the base64-encoded image from the response
    data = response.json()  # Get the JSON response
    base64_string = data.get("image_with_visualizations", "")  # Extract the base64 string

    # Step 3: Save the base64 string into a text file
    with open("base64_image.txt", "w") as file:
        file.write(base64_string)  # Save the base64 string

    print("Base64 string saved to 'base64_image.txt'")

else:
    print("Error:", response.status_code)
