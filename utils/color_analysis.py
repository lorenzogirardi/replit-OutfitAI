import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import cv2

class ColorAnalyzer:
    """Handles color extraction and analysis"""
    
    def __init__(self):
        self.color_names = self._load_color_names()
    
    def _load_color_names(self):
        """Load basic color name mappings"""
        return {
            'black': [0, 0, 0],
            'white': [255, 255, 255],
            'red': [255, 0, 0],
            'green': [0, 255, 0],
            'blue': [0, 0, 255],
            'yellow': [255, 255, 0],
            'cyan': [0, 255, 255],
            'magenta': [255, 0, 255],
            'navy': [0, 0, 128],
            'brown': [165, 42, 42],
            'gray': [128, 128, 128],
            'orange': [255, 165, 0],
            'purple': [128, 0, 128],
            'pink': [255, 192, 203],
            'beige': [245, 245, 220],
            'maroon': [128, 0, 0],
            'olive': [128, 128, 0],
            'teal': [0, 128, 128],
            'silver': [192, 192, 192],
            'gold': [255, 215, 0]
        }
    
    def extract_dominant_colors(self, image, n_colors=5):
        """Extract dominant colors from an image using K-means clustering"""
        if isinstance(image, Image.Image):
            # Convert PIL to numpy array
            image_array = np.array(image)
        else:
            image_array = image
            
        # Reshape image to be a list of pixels
        pixels = image_array.reshape((-1, 3))
        
        # Remove any alpha channel
        if pixels.shape[1] > 3:
            pixels = pixels[:, :3]
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Calculate the percentage of each color
        labels = kmeans.labels_
        percentages = []
        for i in range(n_colors):
            percentages.append(np.sum(labels == i) / len(labels) if labels is not None else 0)
        
        # Sort colors by percentage
        color_data = list(zip(colors, percentages))
        color_data.sort(key=lambda x: x[1], reverse=True)
        
        return [color for color, _ in color_data]
    
    def get_color_name(self, rgb_color):
        """Get the closest color name for an RGB value"""
        min_distance = float('inf')
        closest_color = 'unknown'
        
        for color_name, color_rgb in self.color_names.items():
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb_color, color_rgb)))
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        return closest_color
    
    def calculate_color_similarity(self, color1, color2):
        """Calculate similarity between two colors (0-1, higher is more similar)"""
        # Convert to LAB color space for perceptual color difference
        color1_lab = self.rgb_to_lab(np.array(color1))
        color2_lab = self.rgb_to_lab(np.array(color2))
        
        # Calculate deltaE (CIE76)
        delta_e = np.sqrt(
            (color1_lab[0] - color2_lab[0]) ** 2 +
            (color1_lab[1] - color2_lab[1]) ** 2 +
            (color1_lab[2] - color2_lab[2]) ** 2
        )
        
        # Convert to similarity score (0-1)
        # DeltaE of 100 is considered very different, 0 is identical
        similarity = max(0, 1 - (delta_e / 100))
        
        return similarity
    
    def rgb_to_lab(self, rgb):
        """Convert RGB to LAB color space"""
        # Normalize RGB values
        rgb_normalized = np.array(rgb) / 255.0
        
        # Convert to XYZ first
        xyz = self.rgb_to_xyz(rgb_normalized)
        
        # Convert XYZ to LAB
        lab = self.xyz_to_lab(xyz)
        
        return lab
    
    def rgb_to_xyz(self, rgb):
        """Convert RGB to XYZ color space"""
        # Apply gamma correction
        rgb_corrected = []
        for value in rgb:
            if value > 0.04045:
                value = ((value + 0.055) / 1.055) ** 2.4
            else:
                value = value / 12.92
            rgb_corrected.append(value * 100)
        
        r, g, b = rgb_corrected
        
        # Apply transformation matrix
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        
        return [x, y, z]
    
    def xyz_to_lab(self, xyz):
        """Convert XYZ to LAB color space"""
        # Reference white D65
        xn, yn, zn = 95.047, 100.000, 108.883
        
        x, y, z = xyz
        x = x / xn
        y = y / yn
        z = z / zn
        
        # Apply lab transformation
        def f(t):
            if t > 0.008856:
                return t ** (1/3)
            else:
                return (7.787 * t) + (16/116)
        
        fx = f(x)
        fy = f(y)
        fz = f(z)
        
        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)
        
        return [L, a, b]
    
    def analyze_color_harmony(self, colors):
        """Analyze color harmony relationships"""
        if len(colors) < 2:
            return "monochromatic"
        
        # Convert colors to HSV for easier harmony analysis
        hsv_colors = []
        for color in colors:
            color_array = np.uint8([[np.array(color)]])
            hsv = cv2.cvtColor(color_array, cv2.COLOR_RGB2HSV)[0][0]
            hsv_colors.append(hsv)
        
        hues = [hsv[0] for hsv in hsv_colors]
        
        # Analyze hue relationships
        hue_differences = []
        for i in range(len(hues)):
            for j in range(i + 1, len(hues)):
                diff = abs(hues[i] - hues[j])
                # Handle circular nature of hue
                diff = min(diff, 360 - diff)
                hue_differences.append(diff)
        
        avg_hue_diff = np.mean(hue_differences)
        
        # Classify harmony type
        if avg_hue_diff < 30:
            return "analogous"
        elif 60 <= avg_hue_diff <= 120:
            return "triadic"
        elif 150 <= avg_hue_diff <= 210:
            return "complementary"
        else:
            return "complex"
    
    def get_color_temperature(self, rgb_color):
        """Determine if a color is warm or cool"""
        r, g, b = rgb_color
        
        # Simple heuristic: more red/yellow = warm, more blue = cool
        warm_score = (r + (g * 0.5)) - b
        
        if warm_score > 50:
            return "warm"
        elif warm_score < -50:
            return "cool"
        else:
            return "neutral"
    
    def calculate_color_contrast(self, color1, color2):
        """Calculate contrast ratio between two colors"""
        def get_luminance(rgb):
            """Calculate relative luminance"""
            rgb_normalized = [c / 255.0 for c in rgb]
            rgb_corrected = []
            
            for c in rgb_normalized:
                if c <= 0.03928:
                    c = c / 12.92
                else:
                    c = ((c + 0.055) / 1.055) ** 2.4
                rgb_corrected.append(c)
            
            return 0.2126 * rgb_corrected[0] + 0.7152 * rgb_corrected[1] + 0.0722 * rgb_corrected[2]
        
        lum1 = get_luminance(color1)
        lum2 = get_luminance(color2)
        
        # Ensure lighter color is in numerator
        if lum1 > lum2:
            return (lum1 + 0.05) / (lum2 + 0.05)
        else:
            return (lum2 + 0.05) / (lum1 + 0.05)
