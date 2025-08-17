import cv2
import numpy as np
from PIL import Image
import io

class ImageProcessor:
    """Handles image processing and feature extraction"""
    
    def __init__(self):
        self.target_size = (224, 224)
    
    def preprocess_image(self, image):
        """Preprocess image for analysis"""
        if isinstance(image, Image.Image):
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            opencv_image = image
            
        # Resize image
        resized = cv2.resize(opencv_image, self.target_size)
        
        return resized
    
    def extract_style_features(self, image):
        """Extract style-related features from the image"""
        opencv_image = self.preprocess_image(image)
        
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2LAB)
        
        features = {}
        
        # Calculate brightness and contrast
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        features['brightness'] = np.mean(gray)
        features['contrast'] = np.std(gray)
        
        # Analyze saturation
        features['saturation'] = np.mean(hsv[:, :, 1])
        
        # Detect edges for pattern analysis
        edges = cv2.Canny(gray, 50, 150)
        features['edge_density'] = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Analyze texture using LBP-like approach
        features['texture_complexity'] = self.calculate_texture_complexity(gray)
        
        # Color distribution analysis
        features['color_variance'] = self.calculate_color_variance(opencv_image)
        
        return features
    
    def calculate_texture_complexity(self, gray_image):
        """Calculate texture complexity using gradient analysis"""
        # Calculate gradients
        grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate magnitude
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        return np.mean(magnitude)
    
    def calculate_color_variance(self, image):
        """Calculate color variance across the image"""
        # Convert to float for calculation
        image_float = image.astype(np.float32)
        
        # Calculate variance for each channel
        variances = []
        for channel in range(3):
            variances.append(np.var(image_float[:, :, channel]))
        
        return np.mean(variances)
    
    def detect_clothing_regions(self, image):
        """Detect potential clothing regions in the image"""
        opencv_image = self.preprocess_image(image)
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2HSV)
        
        # Create masks for different clothing regions
        regions = {}
        
        # Upper body region (shirts, jackets)
        upper_region = opencv_image[0:opencv_image.shape[0]//2, :]
        regions['upper'] = upper_region
        
        # Lower body region (pants)
        lower_region = opencv_image[opencv_image.shape[0]//2:, :]
        regions['lower'] = lower_region
        
        # Foot region (shoes)
        foot_region = opencv_image[int(opencv_image.shape[0]*0.8):, :]
        regions['feet'] = foot_region
        
        return regions
    
    def extract_pattern_features(self, image):
        """Extract pattern-related features"""
        gray = cv2.cvtColor(self.preprocess_image(image), cv2.COLOR_BGR2GRAY)
        
        features = {}
        
        # Detect lines (for stripes)
        lines = cv2.HoughLinesP(
            cv2.Canny(gray, 50, 150), 
            1, 
            np.pi/180, 
            threshold=50, 
            minLineLength=30, 
            maxLineGap=10
        )
        
        features['line_count'] = len(lines) if lines is not None else 0
        
        # Detect circles (for polka dots)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=1,
            maxRadius=30
        )
        
        features['circle_count'] = len(circles[0]) if circles is not None else 0
        
        # Calculate pattern regularity
        features['pattern_regularity'] = self.calculate_pattern_regularity(gray)
        
        return features
    
    def calculate_pattern_regularity(self, gray_image):
        """Calculate how regular/repetitive patterns are in the image"""
        # Use autocorrelation to detect repeating patterns
        fft = np.fft.fft2(gray_image)
        autocorr = np.fft.ifft2(fft * np.conj(fft)).real
        
        # Normalize autocorrelation
        autocorr = autocorr / np.max(autocorr)
        
        # Find peaks in autocorrelation (indicating repeating patterns)
        center_x, center_y = autocorr.shape[0] // 2, autocorr.shape[1] // 2
        
        # Exclude the center peak and look for other significant peaks
        autocorr[center_x-5:center_x+5, center_y-5:center_y+5] = 0
        
        return np.max(autocorr)
