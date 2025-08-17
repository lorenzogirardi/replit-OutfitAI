import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.color_analysis import ColorAnalyzer

class OutfitMatcher:
    """Matches clothing items based on color and style analysis"""
    
    def __init__(self):
        self.color_analyzer = ColorAnalyzer()
        self.style_weights = {
            'color_match': 0.4,
            'style_compatibility': 0.3,
            'pattern_harmony': 0.2,
            'color_harmony': 0.1
        }
    
    def find_best_matches(self, inspiration_colors, style_features, clothing_data, threshold=0.6):
        """Find the best clothing matches for reconstructing an outfit"""
        
        # Calculate scores for each clothing item
        scored_items = self._score_all_items(inspiration_colors, style_features, clothing_data)
        
        # Select best items for each category
        outfit = {}
        categories = ['shirt', 'pants', 'shoes', 'jacket', 'accessory']
        
        for category in categories:
            category_items = scored_items[scored_items['category'] == category]
            
            if not category_items.empty and category_items['total_score'].max() >= threshold:
                best_item = category_items.loc[category_items['total_score'].idxmax()]
                
                outfit[category] = {
                    'name': best_item['name'],
                    'image_url': best_item['image_url'],
                    'primary_color': best_item['primary_color'],
                    'style': best_item['style'],
                    'description': best_item['description'],
                    'confidence': best_item['total_score']
                }
        
        # Ensure outfit harmony
        outfit = self._optimize_outfit_harmony(outfit, inspiration_colors)
        
        return outfit
    
    def _score_all_items(self, inspiration_colors, style_features, clothing_data):
        """Score all clothing items against the inspiration"""
        
        scored_data = clothing_data.copy()
        scores = []
        
        for _, item in clothing_data.iterrows():
            # Color matching score
            color_score = self._calculate_color_match_score(
                inspiration_colors, 
                self._parse_item_colors(item)
            )
            
            # Style compatibility score
            style_score = self._calculate_style_score(style_features, item)
            
            # Pattern harmony score
            pattern_score = self._calculate_pattern_score(style_features, item)
            
            # Color harmony score (how well it fits with other selected items)
            harmony_score = self._calculate_harmony_score(item, inspiration_colors)
            
            # Calculate weighted total score
            total_score = (
                color_score * self.style_weights['color_match'] +
                style_score * self.style_weights['style_compatibility'] +
                pattern_score * self.style_weights['pattern_harmony'] +
                harmony_score * self.style_weights['color_harmony']
            )
            
            scores.append({
                'color_score': color_score,
                'style_score': style_score,
                'pattern_score': pattern_score,
                'harmony_score': harmony_score,
                'total_score': total_score
            })
        
        # Add scores to dataframe
        for key in scores[0].keys():
            scored_data[key] = [score[key] for score in scores]
        
        return scored_data
    
    def _parse_item_colors(self, item):
        """Parse colors from clothing item data"""
        # For this implementation, we'll use the primary_color and assume some secondary colors
        primary_color = item['primary_color']
        
        # Map color names to RGB values
        color_map = {
            'black': [0, 0, 0],
            'white': [255, 255, 255],
            'red': [255, 0, 0],
            'blue': [0, 0, 255],
            'green': [0, 255, 0],
            'yellow': [255, 255, 0],
            'brown': [165, 42, 42],
            'gray': [128, 128, 128],
            'navy': [0, 0, 128],
            'beige': [245, 245, 220],
            'pink': [255, 192, 203],
            'purple': [128, 0, 128],
            'orange': [255, 165, 0],
            'maroon': [128, 0, 0],
            'olive': [128, 128, 0],
            'teal': [0, 128, 128]
        }
        
        rgb_color = color_map.get(primary_color.lower(), [128, 128, 128])
        return [rgb_color]
    
    def _calculate_color_match_score(self, inspiration_colors, item_colors):
        """Calculate how well item colors match inspiration colors"""
        if not item_colors or not inspiration_colors:
            return 0.0
        
        max_similarity = 0.0
        
        # Find the best color match
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
        
        # Define style compatibility based on image features
        style_scores = {
            'casual': 0.8 if style_features.get('brightness', 0) > 100 else 0.6,
            'formal': 0.9 if style_features.get('contrast', 0) > 50 else 0.5,
            'business': 0.8 if style_features.get('edge_density', 0) < 0.1 else 0.6,
            'elegant': 0.9 if style_features.get('texture_complexity', 0) < 30 else 0.7,
            'sporty': 0.8 if style_features.get('saturation', 0) > 100 else 0.6,
            'trendy': 0.7,  # Neutral score for trendy items
            'classic': 0.8 if style_features.get('color_variance', 0) < 1000 else 0.6
        }
        
        return style_scores.get(item_style, 0.5)
    
    def _calculate_pattern_score(self, style_features, item):
        """Calculate pattern harmony score"""
        # Simple pattern compatibility based on style features
        edge_density = style_features.get('edge_density', 0)
        texture_complexity = style_features.get('texture_complexity', 0)
        
        # If inspiration has high pattern complexity, favor simpler items
        if edge_density > 0.15 or texture_complexity > 50:
            # Prefer solid colors or simple patterns
            return 0.8 if 'solid' in item['description'].lower() else 0.6
        else:
            # Can accommodate more complex patterns
            return 0.8
    
    def _calculate_harmony_score(self, item, inspiration_colors):
        """Calculate how well the item harmonizes with the color scheme"""
        item_colors = self._parse_item_colors(item)
        
        if not item_colors or not inspiration_colors:
            return 0.5
        
        # Check color harmony using color theory
        harmony_score = 0.0
        
        for item_color in item_colors:
            color_name = self.color_analyzer.get_color_name(item_color)
            color_temp = self.color_analyzer.get_color_temperature(item_color)
            
            # Boost score for neutral colors (they go with everything)
            if color_name in ['black', 'white', 'gray', 'beige']:
                harmony_score += 0.9
            
            # Check temperature harmony
            inspiration_temps = [
                self.color_analyzer.get_color_temperature(color) 
                for color in inspiration_colors
            ]
            
            if color_temp in inspiration_temps or color_temp == 'neutral':
                harmony_score += 0.7
            else:
                harmony_score += 0.4
        
        return min(harmony_score / len(item_colors), 1.0)
    
    def _optimize_outfit_harmony(self, outfit, inspiration_colors):
        """Optimize the overall outfit for color harmony"""
        if len(outfit) < 2:
            return outfit
        
        # Extract colors from selected outfit items
        outfit_colors = []
        for category, item in outfit.items():
            item_colors = self._parse_item_colors(pd.Series({
                'primary_color': item['primary_color'],
                'description': item['description']
            }))
            outfit_colors.extend(item_colors)
        
        # Check overall harmony
        harmony_type = self.color_analyzer.analyze_color_harmony(outfit_colors + inspiration_colors)
        
        # Adjust confidence scores based on overall harmony
        harmony_multipliers = {
            'analogous': 1.1,
            'complementary': 1.05,
            'triadic': 1.0,
            'monochromatic': 1.15,
            'complex': 0.9
        }
        
        multiplier = harmony_multipliers.get(harmony_type, 1.0)
        
        for category in outfit:
            outfit[category]['confidence'] = min(
                outfit[category]['confidence'] * multiplier, 
                1.0
            )
        
        return outfit
    
    def suggest_alternatives(self, outfit, clothing_data, inspiration_colors):
        """Suggest alternative items for each category"""
        alternatives = {}
        
        for category, selected_item in outfit.items():
            category_items = clothing_data[clothing_data['category'] == category]
            
            # Score all items in this category
            scored_items = self._score_all_items(inspiration_colors, {}, category_items)
            
            # Get top 3 alternatives (excluding the selected item)
            alternatives_list = scored_items[
                scored_items['name'] != selected_item['name']
            ].nlargest(3, 'total_score')
            
            alternatives[category] = []
            for _, item in alternatives_list.iterrows():
                alternatives[category].append({
                    'name': item['name'],
                    'image_url': item['image_url'],
                    'primary_color': item['primary_color'],
                    'style': item['style'],
                    'confidence': item['total_score']
                })
        
        return alternatives
