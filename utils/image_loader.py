import os
import pandas as pd
from PIL import Image
import streamlit as st

class ImageLoader:
    """Handles loading clothing and inspiration images from local directories"""
    
    def __init__(self):
        self.products_dir = "images/products"
        self.style_references_dir = "images/style_references"
        self.user_looks_dir = "images/looks"
        self.clothing_dir = "images/clothing"  # Legacy fallback
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    def load_products_from_directory(self):
        """Load product items from the local directory structure"""
        product_items = []
        
        # Try new products directory first, then fallback to legacy clothing dir
        search_dirs = [self.products_dir, self.clothing_dir]
        
        for base_dir in search_dirs:
            if os.path.exists(base_dir):
                break
        else:
            return pd.DataFrame()
        
        # Map directory names to categories
        category_mapping = {
            'shirts': 'shirt',
            'pants': 'pants', 
            'shoes': 'shoes',
            'jackets': 'jacket',
            'accessories': 'accessory'
        }
        
        for category_dir, category in category_mapping.items():
            dir_path = os.path.join(base_dir, category_dir)
            
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if any(filename.endswith(ext) for ext in self.supported_formats):
                        item_path = os.path.join(dir_path, filename)
                        
                        # Extract basic info from filename
                        name = os.path.splitext(filename)[0].replace('_', ' ').title()
                        
                        # Try to guess color and style from filename
                        color, style = self._extract_info_from_filename(filename.lower())
                        
                        product_items.append({
                            'name': name,
                            'category': category,
                            'primary_color': color,
                            'style': style,
                            'description': f'{name} - {color} {category}',
                            'image_url': item_path,
                            'local_file': True
                        })
        
        return pd.DataFrame(product_items) if product_items else pd.DataFrame()
    
    def load_clothing_from_directory(self):
        """Legacy method - redirects to load_products_from_directory"""
        return self.load_products_from_directory()
    
    def _extract_info_from_filename(self, filename):
        """Extract color and style information from filename"""
        # Common colors
        colors = {
            'black': 'black', 'white': 'white', 'blue': 'blue', 'navy': 'navy',
            'red': 'red', 'green': 'green', 'gray': 'gray', 'brown': 'brown',
            'beige': 'beige', 'pink': 'pink', 'purple': 'purple', 'yellow': 'yellow',
            'orange': 'orange', 'olive': 'olive', 'maroon': 'maroon'
        }
        
        # Common styles
        styles = {
            'formal': 'formal', 'casual': 'casual', 'business': 'business',
            'elegant': 'elegant', 'sporty': 'sporty', 'trendy': 'trendy',
            'classic': 'classic', 'dress': 'formal', 'polo': 'casual',
            'tshirt': 'casual', 'jeans': 'casual', 'suit': 'formal',
            'blazer': 'formal', 'sneakers': 'casual', 'oxford': 'formal'
        }
        
        # Default values
        detected_color = 'unknown'
        detected_style = 'casual'
        
        # Look for color keywords
        for color_key, color_value in colors.items():
            if color_key in filename:
                detected_color = color_value
                break
        
        # Look for style keywords
        for style_key, style_value in styles.items():
            if style_key in filename:
                detected_style = style_value
                break
        
        return detected_color, detected_style
    
    def _extract_style_type_from_filename(self, filename):
        """Extract style type for reference images"""
        style_types = {
            'formal': 'formal',
            'business': 'business', 
            'casual': 'casual',
            'smart': 'smart_casual',
            'sporty': 'sporty',
            'sport': 'sporty',
            'elegant': 'elegant',
            'evening': 'evening'
        }
        
        for style_key, style_value in style_types.items():
            if style_key in filename:
                return style_value
        
        return 'general'
    
    def load_user_looks(self):
        """Load user inspiration look images from directory"""
        looks = []
        
        if not os.path.exists(self.user_looks_dir):
            return []
        
        for filename in os.listdir(self.user_looks_dir):
            if any(filename.endswith(ext) for ext in self.supported_formats):
                look_path = os.path.join(self.user_looks_dir, filename)
                name = os.path.splitext(filename)[0].replace('_', ' ').title()
                
                looks.append({
                    'name': name,
                    'path': look_path,
                    'filename': filename,
                    'type': 'user_inspiration'
                })
        
        return looks
    
    def load_style_references(self):
        """Load style reference images for AI training"""
        references = []
        
        if not os.path.exists(self.style_references_dir):
            return []
        
        for filename in os.listdir(self.style_references_dir):
            if any(filename.endswith(ext) for ext in self.supported_formats):
                ref_path = os.path.join(self.style_references_dir, filename)
                name = os.path.splitext(filename)[0].replace('_', ' ').title()
                
                # Try to extract style type from filename
                style_type = self._extract_style_type_from_filename(filename.lower())
                
                references.append({
                    'name': name,
                    'path': ref_path,
                    'filename': filename,
                    'style_type': style_type,
                    'type': 'style_reference'
                })
        
        return references
    
    def load_inspiration_looks(self):
        """Legacy method - redirects to load_user_looks"""
        return self.load_user_looks()
    
    def get_image_from_path(self, image_path):
        """Load and return PIL Image from local path"""
        try:
            if os.path.exists(image_path):
                return Image.open(image_path)
            else:
                return None
        except Exception as e:
            st.error(f"Errore nel caricamento dell'immagine: {e}")
            return None
    
    def validate_image_directories(self):
        """Check if image directories exist and provide setup instructions"""
        issues = []
        
        # Check main directories
        if not os.path.exists(self.products_dir):
            issues.append(f"Cartella prodotti mancante: {self.products_dir}")
        
        if not os.path.exists(self.style_references_dir):
            issues.append(f"Cartella riferimenti stile mancante: {self.style_references_dir}")
        
        if not os.path.exists(self.user_looks_dir):
            issues.append(f"Cartella look utente mancante: {self.user_looks_dir}")
        
        # Check product subdirectories
        required_subdirs = ['shirts', 'pants', 'shoes', 'jackets', 'accessories']
        for subdir in required_subdirs:
            path = os.path.join(self.products_dir, subdir)
            if not os.path.exists(path):
                issues.append(f"Sottocartella prodotti mancante: {path}")
        
        return issues
    
    def count_images_by_category(self):
        """Count images in each category"""
        counts = {}
        
        category_mapping = {
            'shirts': 'shirt',
            'pants': 'pants', 
            'shoes': 'shoes',
            'jackets': 'jacket',
            'accessories': 'accessory'
        }
        
        # Count products (try new directory first, fallback to legacy)
        product_dir = self.products_dir if os.path.exists(self.products_dir) else self.clothing_dir
        
        for category_dir, category in category_mapping.items():
            dir_path = os.path.join(product_dir, category_dir)
            count = 0
            
            if os.path.exists(dir_path):
                count = len([f for f in os.listdir(dir_path) 
                           if any(f.endswith(ext) for ext in self.supported_formats)])
            
            counts[category] = count
        
        # Count style references
        style_refs_count = 0
        if os.path.exists(self.style_references_dir):
            style_refs_count = len([f for f in os.listdir(self.style_references_dir) 
                                  if any(f.endswith(ext) for ext in self.supported_formats)])
        
        counts['style_references'] = style_refs_count
        
        # Count user looks
        user_looks_count = 0
        if os.path.exists(self.user_looks_dir):
            user_looks_count = len([f for f in os.listdir(self.user_looks_dir) 
                                  if any(f.endswith(ext) for ext in self.supported_formats)])
        
        counts['user_looks'] = user_looks_count
        
        return counts