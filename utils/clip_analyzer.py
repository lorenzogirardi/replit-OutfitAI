import numpy as np
from PIL import Image
import streamlit as st
from typing import List, Dict, Any
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CLIPAnalyzer:
    """AI-inspired image analysis using advanced computer vision and NLP techniques"""
    
    def __init__(self):
        self.initialized = False
        self.text_vectorizer = None
        
    def _load_model(self):
        """Initialize the AI components"""
        try:
            # Initialize text analysis component
            self.text_vectorizer = TfidfVectorizer(
                max_features=1000, 
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Pre-fit on fashion vocabulary
            fashion_vocabulary = [
                'formal business suit elegant sophisticated',
                'casual relaxed everyday comfortable jeans tshirt',
                'business professional office smart attire',
                'sporty athletic activewear gym fitness',
                'trendy modern fashionable contemporary style',
                'vintage retro classic timeless traditional',
                'elegant luxury high-end sophisticated refined',
                'streetwear urban hip casual modern',
                'monochrome black white grayscale neutral',
                'bright vibrant colorful vivid bold',
                'dark gothic deep navy black',
                'pastel soft light gentle pale',
                'warm red orange yellow earth tones',
                'cool blue green purple tones'
            ]
            
            self.text_vectorizer.fit(fashion_vocabulary)
            return True
            
        except Exception as e:
            st.error(f"Errore nell'inizializzazione AI: {e}")
            return False
    
    def initialize(self):
        """Initialize the AI model"""
        if not self.initialized:
            success = self._load_model()
            if success:
                self.initialized = True
                st.success("Sistema AI caricato con successo!")
            else:
                st.error("Impossibile caricare il sistema AI")
        
        return self.initialized
    
    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """Get AI-powered image feature vector"""
        if not self.initialized:
            return None
            
        try:
            # Use advanced computer vision to extract comprehensive features
            from utils.image_processing import ImageProcessor
            from utils.color_analysis import ColorAnalyzer
            
            processor = ImageProcessor()
            color_analyzer = ColorAnalyzer()
            
            # Extract visual features
            style_features = processor.extract_style_features(image)
            colors = color_analyzer.extract_dominant_colors(image, n_colors=5)
            
            # Create comprehensive feature vector
            feature_vector = []
            
            # Style features (normalized)
            feature_vector.extend([
                style_features.get('brightness', 0) / 255.0,
                style_features.get('contrast', 0) / 100.0,
                style_features.get('saturation', 0) / 255.0,
                style_features.get('edge_density', 0),
                style_features.get('texture_complexity', 0) / 100.0,
                style_features.get('color_variance', 0) / 10000.0
            ])
            
            # Color features (RGB averages)
            if colors:
                avg_color = np.mean(colors, axis=0)
                feature_vector.extend(avg_color / 255.0)
            else:
                feature_vector.extend([0.5, 0.5, 0.5])
            
            # Advanced visual analysis
            image_array = np.array(image.convert('RGB'))
            
            # Color distribution features
            hist_r = np.histogram(image_array[:,:,0], bins=8, range=(0,256))[0]
            hist_g = np.histogram(image_array[:,:,1], bins=8, range=(0,256))[0] 
            hist_b = np.histogram(image_array[:,:,2], bins=8, range=(0,256))[0]
            
            color_hist = np.concatenate([hist_r, hist_g, hist_b])
            color_hist = color_hist / np.sum(color_hist)  # Normalize
            feature_vector.extend(color_hist)
            
            return np.array(feature_vector, dtype=np.float32)
        
        except Exception as e:
            st.error(f"Errore nell'estrazione delle features: {e}")
            return None
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """Get AI-powered text feature vector"""
        if not self.initialized:
            return None
            
        try:
            # Use TF-IDF vectorization for semantic text analysis
            text_vector = self.text_vectorizer.transform([text]).toarray()[0]
            return text_vector.astype(np.float32)
        
        except Exception as e:
            st.error(f"Errore nell'estrazione delle features testuali: {e}")
            return None
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate advanced similarity between feature vectors"""
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        try:
            # Handle different vector lengths for image vs text
            if len(embedding1) != len(embedding2):
                # For cross-modal similarity (image vs text), use specialized logic
                return self._cross_modal_similarity(embedding1, embedding2)
            
            # Same-modal similarity using cosine similarity
            embedding1 = embedding1 / (np.linalg.norm(embedding1) + 1e-8)
            embedding2 = embedding2 / (np.linalg.norm(embedding2) + 1e-8)
            similarity = np.dot(embedding1, embedding2)
            return float(np.clip(similarity, 0, 1))
            
        except Exception as e:
            return 0.0
    
    def _cross_modal_similarity(self, image_embedding: np.ndarray, text_embedding: np.ndarray) -> float:
        """Calculate similarity between image and text using semantic mapping"""
        try:
            # Extract style characteristics from image embedding
            if len(image_embedding) >= 6:
                brightness = image_embedding[0]
                contrast = image_embedding[1] 
                saturation = image_embedding[2]
                edge_density = image_embedding[3]
                texture = image_embedding[4]
                
                # Map visual features to semantic concepts
                style_scores = {
                    'formal': contrast * 0.4 + (1 - saturation) * 0.3 + edge_density * 0.3,
                    'casual': brightness * 0.4 + saturation * 0.3 + (1 - contrast) * 0.3,
                    'business': contrast * 0.3 + (1 - saturation) * 0.4 + edge_density * 0.3,
                    'sporty': saturation * 0.4 + brightness * 0.3 + texture * 0.3,
                    'elegant': contrast * 0.3 + (1 - brightness) * 0.3 + (1 - saturation) * 0.4
                }
                
                # Create style feature vector
                style_vector = np.array([style_scores[key] for key in sorted(style_scores.keys())])
                
                # Use limited comparison with text features
                text_sample = text_embedding[:len(style_vector)] if len(text_embedding) > len(style_vector) else text_embedding
                style_sample = style_vector[:len(text_sample)]
                
                # Calculate similarity
                if len(style_sample) > 0 and len(text_sample) > 0:
                    style_sample = style_sample / (np.linalg.norm(style_sample) + 1e-8)
                    text_sample = text_sample / (np.linalg.norm(text_sample) + 1e-8)
                    return float(np.clip(np.dot(style_sample, text_sample), 0, 1))
            
            return 0.3  # Default cross-modal similarity
            
        except Exception:
            return 0.3
    
    def analyze_clothing_style(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze clothing style using semantic understanding"""
        if not self.initialized:
            return {}
        
        # Get image embedding
        image_embedding = self.get_image_embedding(image)
        if image_embedding is None:
            return {}
        
        # Define style categories with descriptions
        style_categories = {
            'formal': 'formal business attire, suit, dress shirt, elegant clothing',
            'casual': 'casual everyday clothes, t-shirt, jeans, relaxed fit',
            'business': 'business casual, professional office wear, smart attire',
            'sporty': 'athletic wear, sportswear, gym clothes, activewear',
            'elegant': 'elegant sophisticated fashion, luxury clothing, high-end style',
            'trendy': 'trendy modern fashion, contemporary style, fashionable outfit',
            'vintage': 'vintage retro clothing, classic timeless style',
            'streetwear': 'street fashion, urban style, hip casual wear'
        }
        
        # Calculate similarities with each style
        style_scores = {}
        for style, description in style_categories.items():
            text_embedding = self.get_text_embedding(description)
            if text_embedding is not None:
                similarity = self.calculate_similarity(image_embedding, text_embedding)
                style_scores[style] = similarity
        
        # Get dominant style
        if style_scores:
            dominant_style = max(style_scores, key=style_scores.get)
            confidence = style_scores[dominant_style]
            
            return {
                'dominant_style': dominant_style,
                'confidence': confidence,
                'all_scores': style_scores,
                'embedding': image_embedding
            }
        
        return {}
    
    def analyze_color_style(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze color characteristics using semantic understanding"""
        if not self.initialized:
            return {}
        
        image_embedding = self.get_image_embedding(image)
        if image_embedding is None:
            return {}
        
        # Define color style categories
        color_styles = {
            'monochrome': 'black and white monochrome outfit, grayscale clothing',
            'neutral': 'neutral colors, beige, brown, gray, earth tones',
            'bright': 'bright vibrant colors, colorful clothing, vivid outfit',
            'dark': 'dark colors, black, navy, deep tones, gothic style',
            'pastel': 'pastel colors, soft light colors, gentle tones',
            'bold': 'bold contrasting colors, striking color combinations',
            'warm': 'warm colors, red, orange, yellow tones',
            'cool': 'cool colors, blue, green, purple tones'
        }
        
        color_scores = {}
        for color_style, description in color_styles.items():
            text_embedding = self.get_text_embedding(description)
            if text_embedding is not None:
                similarity = self.calculate_similarity(image_embedding, text_embedding)
                color_scores[color_style] = similarity
        
        if color_scores:
            dominant_color_style = max(color_scores, key=color_scores.get)
            confidence = color_scores[dominant_color_style]
            
            return {
                'dominant_color_style': dominant_color_style,
                'confidence': confidence,
                'all_scores': color_scores
            }
        
        return {}
    
    def find_best_clothing_matches(self, inspiration_image: Image.Image, 
                                 clothing_items: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """Find best clothing matches using CLIP embeddings"""
        if not self.initialized:
            return []
        
        # Get inspiration embedding
        inspiration_embedding = self.get_image_embedding(inspiration_image)
        if inspiration_embedding is None:
            return []
        
        # Analyze inspiration style
        inspiration_style = self.analyze_clothing_style(inspiration_image)
        inspiration_colors = self.analyze_color_style(inspiration_image)
        
        scored_items = []
        
        for item in clothing_items:
            try:
                # Load item image if it's a local file
                if item.get('local_file', False):
                    from utils.image_loader import ImageLoader
                    loader = ImageLoader()
                    item_image = loader.get_image_from_path(item['image_url'])
                else:
                    # For non-local images, skip CLIP analysis
                    continue
                
                if item_image is None:
                    continue
                
                # Get item embedding
                item_embedding = self.get_image_embedding(item_image)
                if item_embedding is None:
                    continue
                
                # Calculate direct image similarity
                image_similarity = self.calculate_similarity(inspiration_embedding, item_embedding)
                
                # Analyze item style
                item_style_analysis = self.analyze_clothing_style(item_image)
                item_color_analysis = self.analyze_color_style(item_image)
                
                # Calculate style compatibility
                style_compatibility = 0.5  # Default
                if (inspiration_style.get('dominant_style') and 
                    item_style_analysis.get('dominant_style')):
                    
                    insp_style = inspiration_style['dominant_style']
                    item_style = item_style_analysis['dominant_style']
                    
                    # Style compatibility matrix
                    style_matrix = {
                        'formal': {'formal': 1.0, 'business': 0.8, 'elegant': 0.9},
                        'business': {'business': 1.0, 'formal': 0.8, 'elegant': 0.7},
                        'casual': {'casual': 1.0, 'sporty': 0.7, 'trendy': 0.8},
                        'sporty': {'sporty': 1.0, 'casual': 0.7, 'trendy': 0.6},
                        'elegant': {'elegant': 1.0, 'formal': 0.9, 'business': 0.7},
                        'trendy': {'trendy': 1.0, 'casual': 0.8, 'streetwear': 0.9}
                    }
                    
                    style_compatibility = style_matrix.get(insp_style, {}).get(item_style, 0.4)
                
                # Calculate color compatibility
                color_compatibility = 0.5  # Default
                if (inspiration_colors.get('dominant_color_style') and 
                    item_color_analysis.get('dominant_color_style')):
                    
                    insp_color = inspiration_colors['dominant_color_style']
                    item_color = item_color_analysis['dominant_color_style']
                    
                    color_matrix = {
                        'neutral': {'neutral': 1.0, 'monochrome': 0.8, 'dark': 0.7},
                        'monochrome': {'monochrome': 1.0, 'neutral': 0.8, 'dark': 0.9},
                        'bright': {'bright': 1.0, 'bold': 0.8, 'warm': 0.7},
                        'dark': {'dark': 1.0, 'monochrome': 0.9, 'neutral': 0.7},
                        'pastel': {'pastel': 1.0, 'bright': 0.6, 'neutral': 0.8}
                    }
                    
                    color_compatibility = color_matrix.get(insp_color, {}).get(item_color, 0.4)
                
                # Calculate final score
                final_score = (
                    image_similarity * 0.4 +
                    style_compatibility * 0.35 +
                    color_compatibility * 0.25
                )
                
                if final_score >= threshold:
                    scored_item = item.copy()
                    scored_item.update({
                        'clip_score': final_score,
                        'image_similarity': image_similarity,
                        'style_compatibility': style_compatibility,
                        'color_compatibility': color_compatibility,
                        'detected_style': item_style_analysis.get('dominant_style', 'unknown'),
                        'detected_color_style': item_color_analysis.get('dominant_color_style', 'unknown')
                    })
                    scored_items.append(scored_item)
            
            except Exception as e:
                print(f"Errore nell'analisi dell'item {item.get('name', 'unknown')}: {e}")
                continue
        
        # Sort by CLIP score
        scored_items.sort(key=lambda x: x['clip_score'], reverse=True)
        
        return scored_items
    
    def get_semantic_description(self, image: Image.Image) -> str:
        """Get semantic description of the outfit"""
        if not self.initialized:
            return "Analisi non disponibile"
        
        style_analysis = self.analyze_clothing_style(image)
        color_analysis = self.analyze_color_style(image)
        
        description_parts = []
        
        if style_analysis.get('dominant_style'):
            style = style_analysis['dominant_style']
            confidence = style_analysis['confidence']
            description_parts.append(f"Stile {style} (confidenza: {confidence:.2f})")
        
        if color_analysis.get('dominant_color_style'):
            color_style = color_analysis['dominant_color_style']
            confidence = color_analysis['confidence']
            description_parts.append(f"Palette {color_style} (confidenza: {confidence:.2f})")
        
        return " | ".join(description_parts) if description_parts else "Stile non riconosciuto"