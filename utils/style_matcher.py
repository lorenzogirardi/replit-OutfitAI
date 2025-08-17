import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.color_analysis import ColorAnalyzer
from utils.image_processing import ImageProcessor

class StyleMatcher:
    """Enhanced matching system that uses style references to guide outfit creation"""
    
    def __init__(self):
        self.color_analyzer = ColorAnalyzer()
        self.image_processor = ImageProcessor()
        self.style_weights = {
            'color_match': 0.3,
            'style_compatibility': 0.25,
            'reference_alignment': 0.25,  # New: alignment with style references
            'pattern_harmony': 0.15,
            'color_harmony': 0.05
        }
        self.style_reference_cache = {}
    
    def load_style_references(self, style_references):
        """Preprocess and cache style reference data"""
        self.style_reference_cache = {}
        
        for ref in style_references:
            try:
                from utils.image_loader import ImageLoader
                image_loader = ImageLoader()
                ref_image = image_loader.get_image_from_path(ref['path'])
                
                if ref_image:
                    # Extract features from reference
                    colors = self.color_analyzer.extract_dominant_colors(ref_image, n_colors=5)
                    style_features = self.image_processor.extract_style_features(ref_image)
                    
                    self.style_reference_cache[ref['style_type']] = {
                        'colors': colors,
                        'features': style_features,
                        'name': ref['name']
                    }
            except Exception as e:
                print(f"Error processing style reference {ref['name']}: {e}")
    
    def find_best_matches_with_references(self, inspiration_colors, style_features, 
                                        clothing_data, style_references, threshold=0.6):
        """Enhanced matching that considers style references"""
        
        # Load and process style references
        self.load_style_references(style_references)
        
        # Determine which style reference best matches the inspiration
        best_reference_style = self._find_best_reference_style(inspiration_colors, style_features)
        
        # Calculate scores for each clothing item
        scored_items = self._score_all_items_with_references(
            inspiration_colors, style_features, clothing_data, best_reference_style
        )
        
        # Select best items for each category using enhanced logic
        outfit = self._select_outfit_items(scored_items, threshold, best_reference_style)
        
        # Final harmony optimization
        outfit = self._optimize_outfit_with_references(outfit, inspiration_colors, best_reference_style)
        
        return outfit, best_reference_style
    
    def _find_best_reference_style(self, inspiration_colors, style_features):
        """Find which style reference best matches the inspiration"""
        if not self.style_reference_cache:
            return None
        
        best_match = None
        best_score = 0
        
        for style_type, ref_data in self.style_reference_cache.items():
            # Compare colors
            color_similarity = self._calculate_color_set_similarity(
                inspiration_colors, ref_data['colors']
            )
            
            # Compare style features
            feature_similarity = self._calculate_feature_similarity(
                style_features, ref_data['features']
            )
            
            # Combined score
            total_score = (color_similarity * 0.6) + (feature_similarity * 0.4)
            
            if total_score > best_score:
                best_score = total_score
                best_match = {
                    'style_type': style_type,
                    'score': total_score,
                    'data': ref_data
                }
        
        return best_match
    
    def _calculate_color_set_similarity(self, colors1, colors2):
        """Calculate similarity between two sets of colors"""
        if not colors1 or not colors2:
            return 0.0
        
        similarities = []
        for color1 in colors1:
            max_sim = 0
            for color2 in colors2:
                sim = self.color_analyzer.calculate_color_similarity(color1, color2)
                max_sim = max(max_sim, sim)
            similarities.append(max_sim)
        
        return np.mean(similarities)
    
    def _calculate_feature_similarity(self, features1, features2):
        """Calculate similarity between style features"""
        if not features1 or not features2:
            return 0.0
        
        # Normalize features for comparison
        common_keys = set(features1.keys()) & set(features2.keys())
        if not common_keys:
            return 0.0
        
        similarities = []
        for key in common_keys:
            val1, val2 = features1[key], features2[key]
            # Normalize to 0-1 range and calculate similarity
            max_val = max(abs(val1), abs(val2), 1)  # Avoid division by zero
            normalized_diff = abs(val1 - val2) / max_val
            similarity = 1 - normalized_diff
            similarities.append(similarity)
        
        return np.mean(similarities)
    
    def _score_all_items_with_references(self, inspiration_colors, style_features, 
                                       clothing_data, best_reference):
        """Score items considering style references"""
        scored_data = clothing_data.copy()
        scores = []
        
        for _, item in clothing_data.iterrows():
            # Original scoring components
            color_score = self._calculate_color_match_score(
                inspiration_colors, self._parse_item_colors(item)
            )
            style_score = self._calculate_style_score(style_features, item)
            pattern_score = self._calculate_pattern_score(style_features, item)
            harmony_score = self._calculate_harmony_score(item, inspiration_colors)
            
            # NEW: Reference alignment score
            reference_score = self._calculate_reference_alignment_score(
                item, best_reference
            )
            
            # Calculate weighted total score
            total_score = (
                color_score * self.style_weights['color_match'] +
                style_score * self.style_weights['style_compatibility'] +
                reference_score * self.style_weights['reference_alignment'] +
                pattern_score * self.style_weights['pattern_harmony'] +
                harmony_score * self.style_weights['color_harmony']
            )
            
            scores.append({
                'color_score': color_score,
                'style_score': style_score,
                'reference_score': reference_score,
                'pattern_score': pattern_score,
                'harmony_score': harmony_score,
                'total_score': total_score
            })
        
        # Add scores to dataframe
        for key in scores[0].keys():
            scored_data[key] = [score[key] for score in scores]
        
        return scored_data
    
    def _calculate_reference_alignment_score(self, item, best_reference):
        """Calculate how well an item aligns with the best reference style"""
        if not best_reference:
            return 0.5  # Neutral score if no reference
        
        ref_data = best_reference['data']
        item_colors = self._parse_item_colors(item)
        
        # Color alignment with reference
        color_alignment = self._calculate_color_set_similarity(
            item_colors, ref_data['colors']
        )
        
        # Style type compatibility
        item_style = item['style'].lower()
        ref_style_type = best_reference['style_type']
        
        style_compatibility_map = {
            'formal': {'formal': 1.0, 'business': 0.8, 'elegant': 0.9, 'evening': 0.7},
            'business': {'business': 1.0, 'formal': 0.8, 'smart_casual': 0.7, 'classic': 0.8},
            'casual': {'casual': 1.0, 'smart_casual': 0.6, 'sporty': 0.7, 'trendy': 0.8},
            'smart_casual': {'smart_casual': 1.0, 'business': 0.7, 'casual': 0.6, 'elegant': 0.6},
            'sporty': {'sporty': 1.0, 'casual': 0.7, 'trendy': 0.6},
            'elegant': {'elegant': 1.0, 'formal': 0.9, 'evening': 0.8, 'classic': 0.7},
            'evening': {'evening': 1.0, 'formal': 0.7, 'elegant': 0.8}
        }
        
        style_score = style_compatibility_map.get(ref_style_type, {}).get(item_style, 0.3)
        
        # Combined alignment score
        return (color_alignment * 0.6) + (style_score * 0.4)
    
    def _parse_item_colors(self, item):
        """Parse colors from clothing item data"""
        primary_color = item['primary_color']
        
        color_map = {
            'black': [0, 0, 0], 'white': [255, 255, 255], 'red': [255, 0, 0],
            'blue': [0, 0, 255], 'green': [0, 255, 0], 'yellow': [255, 255, 0],
            'brown': [165, 42, 42], 'gray': [128, 128, 128], 'navy': [0, 0, 128],
            'beige': [245, 245, 220], 'pink': [255, 192, 203], 'purple': [128, 0, 128],
            'orange': [255, 165, 0], 'maroon': [128, 0, 0], 'olive': [128, 128, 0],
            'teal': [0, 128, 128]
        }
        
        rgb_color = color_map.get(primary_color.lower(), [128, 128, 128])
        return [rgb_color]
    
    def _calculate_color_match_score(self, inspiration_colors, item_colors):
        """Calculate color matching score"""
        if not item_colors or not inspiration_colors:
            return 0.0
        
        max_similarity = 0.0
        for item_color in item_colors:
            for inspiration_color in inspiration_colors:
                similarity = self.color_analyzer.calculate_color_similarity(
                    item_color, inspiration_color
                )
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _calculate_style_score(self, style_features, item):
        """Calculate style compatibility score"""
        item_style = item['style'].lower()
        
        style_scores = {
            'casual': 0.8 if style_features.get('brightness', 0) > 100 else 0.6,
            'formal': 0.9 if style_features.get('contrast', 0) > 50 else 0.5,
            'business': 0.8 if style_features.get('edge_density', 0) < 0.1 else 0.6,
            'elegant': 0.9 if style_features.get('texture_complexity', 0) < 30 else 0.7,
            'sporty': 0.8 if style_features.get('saturation', 0) > 100 else 0.6,
            'trendy': 0.7,
            'classic': 0.8 if style_features.get('color_variance', 0) < 1000 else 0.6
        }
        
        return style_scores.get(item_style, 0.5)
    
    def _calculate_pattern_score(self, style_features, item):
        """Calculate pattern harmony score"""
        edge_density = style_features.get('edge_density', 0)
        texture_complexity = style_features.get('texture_complexity', 0)
        
        if edge_density > 0.15 or texture_complexity > 50:
            return 0.8 if 'solid' in item['description'].lower() else 0.6
        else:
            return 0.8
    
    def _calculate_harmony_score(self, item, inspiration_colors):
        """Calculate color harmony score"""
        item_colors = self._parse_item_colors(item)
        
        if not item_colors or not inspiration_colors:
            return 0.5
        
        harmony_score = 0.0
        for item_color in item_colors:
            color_name = self.color_analyzer.get_color_name(item_color)
            
            if color_name in ['black', 'white', 'gray', 'beige']:
                harmony_score += 0.9
            else:
                harmony_score += 0.6
        
        return min(harmony_score / len(item_colors), 1.0)
    
    def _select_outfit_items(self, scored_items, threshold, best_reference):
        """Select best items for outfit with reference-aware logic"""
        outfit = {}
        categories = ['shirt', 'pants', 'shoes', 'jacket', 'accessory']
        
        for category in categories:
            category_items = scored_items[scored_items['category'] == category]
            
            if not category_items.empty:
                # Filter by threshold
                valid_items = category_items[category_items['total_score'] >= threshold]
                
                if not valid_items.empty:
                    best_item = valid_items.loc[valid_items['total_score'].idxmax()]
                    
                    outfit[category] = {
                        'name': best_item['name'],
                        'image_url': best_item['image_url'],
                        'primary_color': best_item['primary_color'],
                        'style': best_item['style'],
                        'description': best_item['description'],
                        'confidence': best_item['total_score'],
                        'reference_score': best_item.get('reference_score', 0)
                    }
        
        return outfit
    
    def _optimize_outfit_with_references(self, outfit, inspiration_colors, best_reference):
        """Final optimization considering reference style"""
        if len(outfit) < 2 or not best_reference:
            return outfit
        
        # Apply reference-based confidence boost
        reference_boost = 1.1 if best_reference['score'] > 0.7 else 1.0
        
        for category in outfit:
            outfit[category]['confidence'] = min(
                outfit[category]['confidence'] * reference_boost,
                1.0
            )
            # Add reference information
            outfit[category]['matched_reference'] = best_reference['data']['name']
            outfit[category]['reference_type'] = best_reference['style_type']
        
        return outfit