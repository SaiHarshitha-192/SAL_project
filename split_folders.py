import os
import shutil

# Specify the folder containing the files
source_folder = "LIBRISPEECH_ROOT1/segments/sdhubert_base/test-clean/8224/274384"
destination_folder = "testinggg2"

# required = [84,174,251,422,652,777,1272,1462,1673,1919,1988,1993,2035,2078,2086,2277,2412,2428,2803,2902,3000,3081,3170,3536,3576,3752,3853,5338,5536,5694,5895,6241,6295,6313,6319,6345,7850,7976,8297,8842]

# # Define the allowed 'a' parts
# allowed_a_parts = {"1", "2", "3"}

allowed_a_parts = {"84", "8297", "8842"}

# Loop through all the .npy files in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".npy"):
        # Split the filename to extract folder names
        parts = file_name.split("-")
        print(type(parts))
        if len(parts) == 3:
            folder_a, folder_b, file_c = parts
            
            # Check if 'a' is in the allowed set
            if folder_a in allowed_a_parts:
                # Create the destination subfolders
                folder_path = os.path.join(destination_folder, folder_a, folder_b)
                os.makedirs(folder_path, exist_ok=True)
                
                # Move the file to the new destination
                source_path = os.path.join(source_folder, file_name)
                destination_path = os.path.join(folder_path, file_name)
                shutil.move(source_path, destination_path)

print("Files have been filtered and organized successfully.")
