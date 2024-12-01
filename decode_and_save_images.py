import os
import base64

# Input file containing base64 responses
input_file = "responses.txt"
output_folder = "output_images"  # Folder to save decoded images

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read and decode base64 data
with open(input_file, "r") as file:
    for line in file:
        # Each line contains: filename<TAB>base64_string
        filename, base64_string = line.strip().split("\t")

        # Decode the base64 string
        image_data = base64.b64decode(base64_string)

        # Save the decoded image
        output_path = os.path.join(output_folder, filename)
        with open(output_path, "wb") as img_file:
            img_file.write(image_data)

        print(f"Saved: {output_path}")

print("All images decoded and saved.")
