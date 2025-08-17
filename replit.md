# AI Fashion Stylist

## Overview

AI Fashion Stylist is a Streamlit-based web application that analyzes fashion inspiration images and reconstructs similar outfits using available clothing items. The system uses computer vision techniques for color extraction, image processing for style analysis, and machine learning algorithms to match clothing items based on visual similarity and style compatibility.

## User Preferences

Preferred communication style: Simple, everyday language.
Project requirement: Organizzazione locale delle immagini in cartelle strutturate per indumenti singoli e look completi.
Deployment requirement: Progetto deve essere scaricabile e utilizzabile con Docker per distribuzione offline.

## System Architecture

### Frontend Architecture
- **Streamlit Framework**: Single-page web application with interactive widgets for image upload and results display
- **Session State Management**: Maintains user data across interactions including uploaded images, analysis results, and reconstructed outfits
- **Caching Strategy**: Uses `@st.cache_resource` for expensive processor initialization and `@st.cache_data` for static clothing data

### Backend Architecture
- **Modular Design**: Separated into distinct utility modules for specific functionalities
- **Image Processing Pipeline**: Sequential processing through preprocessing, feature extraction, and analysis stages
- **Color Analysis Engine**: K-means clustering for dominant color extraction with color name mapping system
- **Outfit Matching Algorithm**: Multi-criteria scoring system weighing color match, style compatibility, pattern harmony, and color harmony

### Core Components
- **ImageProcessor**: Handles image preprocessing, resizing, and style feature extraction including brightness, contrast, saturation, edge detection, and texture analysis
- **ColorAnalyzer**: Extracts dominant colors using K-means clustering and maps RGB values to human-readable color names
- **OutfitMatcher**: Implements scoring algorithm to match clothing items against inspiration images using weighted criteria
- **CLIPAnalyzer**: Advanced AI system that combines computer vision with NLP for semantic image understanding and cross-modal similarity matching
- **StyleMatcher**: Enhanced algorithm that uses style references to improve matching accuracy

### Data Management
- **Three-Tier Image System**: 
  - Products (images/products/): Individual clothing items for outfit composition
  - Style References (images/style_references/): Template outfits that guide AI matching decisions  
  - User Looks (images/looks/): User-uploaded images to reconstruct
- **Enhanced StyleMatcher**: Advanced algorithm that uses style references to improve matching accuracy
- **ImageLoader**: Utility class for managing local image files with automatic color/style detection
- **Sample Data Fallback**: Fallback to sample clothing data when local images not available
- **Feature Vectors**: Numerical representations of style characteristics for similarity calculations
- **Reference-Aware Scoring**: Multi-dimensional scoring system enhanced with style reference alignment

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for user interface
- **OpenCV (cv2)**: Computer vision library for image processing and analysis
- **PIL (Pillow)**: Python Imaging Library for image format handling
- **NumPy**: Numerical computing for array operations and mathematical calculations
- **Pandas**: Data manipulation and analysis for clothing item management
- **Matplotlib**: Plotting library for data visualization
- **scikit-learn**: Machine learning library providing K-means clustering, TF-IDF vectorization, and similarity metrics

### AI Processing Stack
- **K-means Clustering**: For dominant color extraction from uploaded images
- **Canny Edge Detection**: For pattern and texture analysis
- **Color Space Conversion**: HSV and LAB color spaces for comprehensive color analysis
- **TF-IDF Vectorization**: For semantic text analysis and fashion vocabulary understanding
- **Advanced Feature Extraction**: Multi-dimensional visual feature vectors including color histograms, texture complexity, and style characteristics
- **Cross-Modal Similarity**: AI-powered similarity calculation between images and text descriptions
- **Cosine Similarity**: For comparing feature vectors between inspiration and clothing items

### AI Capabilities
- **Semantic Style Analysis**: AI-powered understanding of fashion styles (formal, casual, business, sporty, elegant)
- **Color Palette Recognition**: Advanced color style categorization (monochrome, bright, pastel, warm, cool)
- **Cross-Modal Understanding**: Ability to match visual characteristics with textual style descriptions
- **Multi-Algorithm Support**: Three analysis modes - AI Advanced, Style References, and Basic Matching

### External Services
- **Placeholder Image Service**: Uses placeholder.com CDN for sample clothing item images
- **Future Integration Points**: Architecture supports integration with fashion databases, e-commerce APIs, and cloud-based image processing services