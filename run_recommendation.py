import json
import os
from PIL import Image
import numpy as np
import pandas as pd

from utils.image_loader import ImageLoader
from utils.clip_analyzer import CLIPAnalyzer

def get_image(path):
    """Safely open an image, creating a dummy if it fails."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        # Return a dummy image if the file doesn't exist or is empty
        return Image.new('RGB', (224, 224), color = 'gray')
    try:
        image = Image.open(path)
        return image
    except Exception as e:
        print(f"Warning: Could not open image {path}. Using a dummy image. Error: {e}")
        return Image.new('RGB', (224, 224), color = 'gray')

def run_recommendation(user_look_path: str):
    """
    Analyzes a user's look, finds the best style reference, and suggests products.
    """
    print("Starting recommendation process...")

    # 1. Initialize components
    image_loader = ImageLoader()
    clip_analyzer = CLIPAnalyzer()

    print("Initializing CLIP Analyzer (this may take a while)...")
    if not clip_analyzer.initialize():
        print("Failed to initialize CLIP Analyzer. Aborting.")
        return

    # 2. Load images and data
    print("Loading images...")
    user_look_image = get_image(user_look_path)

    style_references = image_loader.load_style_references()
    if not style_references:
        print("No style references found in 'images/style_references/'. Aborting.")
        return

    products_df = image_loader.load_products_from_directory()
    if products_df.empty:
        print("No products found in 'images/products/'. Aborting.")
        return

    # 3. Calculate embeddings
    print("Calculating embeddings for all images...")
    user_look_embedding = clip_analyzer.get_image_embedding(user_look_image)

    # Pre-calculate embeddings for style references
    for ref in style_references:
        ref_image = get_image(ref['path'])
        ref['embedding'] = clip_analyzer.get_image_embedding(ref_image)

    # Pre-calculate embeddings for products
    product_embeddings = []
    for _, row in products_df.iterrows():
        product_image = get_image(row['image_url'])
        embedding = clip_analyzer.get_image_embedding(product_image)
        product_embeddings.append(embedding)
    products_df['embedding'] = product_embeddings

    # 4. Find the best style reference
    print("Finding the best matching style reference...")
    best_style_ref = None
    highest_similarity = -1.0

    for ref in style_references:
        similarity = clip_analyzer.calculate_similarity(user_look_embedding, ref['embedding'])
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_style_ref = ref

    if best_style_ref is None:
        print("Could not find a suitable style reference. Aborting.")
        return

    matched_style_reference_path = best_style_ref['path']
    print(f"Matched style reference: {matched_style_reference_path} with similarity: {highest_similarity:.4f}")

    style_ref_embedding = best_style_ref['embedding']

    # 5. Find the best products for the matched style
    print("Suggesting products based on the matched style...")
    suggested_products = {}
    categories = ['shirt', 'pants', 'jacket', 'shoes', 'accessory']

    for category in categories:
        category_df = products_df[products_df['category'] == category]
        if category_df.empty:
            print(f"No products found for category: {category}")
            continue

        best_product = None
        highest_product_similarity = -1.0

        for _, row in category_df.iterrows():
            product_embedding = row['embedding']
            similarity = clip_analyzer.calculate_similarity(style_ref_embedding, product_embedding)

            if similarity > highest_product_similarity:
                highest_product_similarity = similarity
                best_product = row

        if best_product is not None:
            suggested_products[category] = best_product['image_url']
            print(f"  - Best {category}: {best_product['name']} (Similarity: {highest_product_similarity:.4f})")

    # 6. Format and print the final JSON output
    result = {
        "matched_style_reference": matched_style_reference_path,
        "suggested_products": suggested_products
    }

    print("\n--- Recommendation Complete ---")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    # The user look to analyze. We use the dummy file we created.
    user_look_path = "images/looks/my_inspiration_look.jpg"

    if not os.path.exists(user_look_path):
        print(f"Error: User look image not found at '{user_look_path}'")
    else:
        run_recommendation(user_look_path)
