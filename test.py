import torch

# Check if CUDA is available
if torch.cuda.is_available():
    print("CUDA is available! You can use the GPU.")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    print(f"Current GPU: {torch.cuda.current_device()}")
    print(f"GPU Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
else:
    print("CUDA is not available. Running on CPU.")
