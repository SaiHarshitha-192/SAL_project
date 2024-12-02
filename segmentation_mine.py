import os
import numpy as np

# Specify paths to your data
input_folder = "/home/harshitha/Desktop/sdhubert_project/sdhubert/LIBRISPEECH_ROOT1/segments_84_121123"  # Replace with your data folder's path
output_folder = "/home/harshitha/Desktop/sdhubert_project/sdhubert/LIBRISPEECH_ROOT1/outputs"  # Replace with your desired output folder path

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all the files in the input folder
for base_name in sorted(set(f.split('_')[0] for f in os.listdir(input_folder))):
    # Generate filenames
    print(input)
    features_file = os.path.join(input_folder, f"{base_name}_feature.npy")
    segments_file = os.path.join(input_folder, f"{base_name}_segment.txt")
    segment_features_file = os.path.join(input_folder, f"{base_name}_segmentfeature.npy")
    output_file = os.path.join(output_folder, f"{base_name}.npy")

    # print(features_file)

    
    # Load data
    if os.path.exists(features_file) and os.path.exists(segments_file) and os.path.exists(segment_features_file):
        # Load features
        features = np.load(features_file)
        # Load segments from txt file
        segments = []
        with open(segments_file, "r") as seg_file:
            for line in seg_file:
                # Split using comma and strip whitespace
                segments.append(list(map(float, line.strip().replace(',', '').split())))
        segments = np.array(segments, dtype=float)

        
        # Load segment features
        segment_features = np.load(segment_features_file)
        
        # Compute length
        length = features.shape[0]
        
        # Prepare dictionary
        data = {
            "segments": segments,
            "features": features,
            "segment_features": segment_features
        }
        
        # Save the dictionary as a .npy file
        np.save(output_file, data)
        # print(f"Saved: {output_file}")
    else:
        print(f"Files missing for base {base_name}. Skipping...")
