import torch
import os

def download_model():
    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)
    
    # Downloads Keremberke's YOLOv8n Hard Hat model (No API Key needed)
    url = "https://huggingface.co/keremberke/yolov8n-hard-hat-detection/resolve/main/best.pt"
    output_path = "models/best.pt"
    
    print(f"Downloading model from {url}...")
    torch.hub.download_url_to_file(url, output_path)
    print(f"Model downloaded to {output_path}")

if __name__ == "__main__":
    download_model()
