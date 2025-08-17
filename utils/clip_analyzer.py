import torch
from transformers import AutoProcessor, AutoModel
from PIL import Image
import numpy as np
from typing import List, Dict

class CLIPAnalyzer:
    """
    A class to analyze images using a real CLIP model.
    """
    def __init__(self, model_name="laion/CLIP-ViT-B-32-laion2B-s34B-b79K"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        self.initialized = False

    def initialize(self):
        """
        Loads the CLIP model and processor from Hugging Face.
        """
        if self.initialized:
            return True
        try:
            print(f"Loading CLIP model: {self.model_name} on device: {self.device}")
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
            self.initialized = True
            print("CLIP model loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading CLIP model: {e}")
            return False

    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Generates an embedding for a given PIL image.
        """
        if not self.initialized:
            raise RuntimeError("CLIPAnalyzer is not initialized. Call .initialize() first.")
        
        # Ensure image is in RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)

        # Normalize features
        image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)

        return image_features.cpu().numpy().squeeze()

    def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Generates an embedding for a given text string.
        """
        if not self.initialized:
            raise RuntimeError("CLIPAnalyzer is not initialized. Call .initialize() first.")
        
        inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)

        # Normalize features
        text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

        return text_features.cpu().numpy().squeeze()

    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculates the cosine similarity between two embeddings.
        Assumes embeddings are already normalized.
        """
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        # Ensure embeddings are 1D arrays for dot product
        embedding1 = embedding1.flatten()
        embedding2 = embedding2.flatten()
        
        similarity = np.dot(embedding1, embedding2.T)
        return float(np.clip(similarity, 0.0, 1.0))