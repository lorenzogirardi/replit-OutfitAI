import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from utils.image_processing import ImageProcessor
from utils.color_analysis import ColorAnalyzer
from utils.outfit_matcher import OutfitMatcher
from utils.style_matcher import StyleMatcher
from utils.clip_analyzer import CLIPAnalyzer
from utils.image_loader import ImageLoader
from data.sample_clothing import get_sample_clothing_data
import io

# Configure page
st.set_page_config(
    page_title="AI Fashion Stylist",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'reconstructed_outfit' not in st.session_state:
    st.session_state.reconstructed_outfit = None

# Initialize processors
@st.cache_resource
def load_processors():
    """Load and cache the processing components"""
    image_processor = ImageProcessor()
    color_analyzer = ColorAnalyzer()
    outfit_matcher = OutfitMatcher()
    style_matcher = StyleMatcher()
    clip_analyzer = CLIPAnalyzer()
    return image_processor, color_analyzer, outfit_matcher, style_matcher, clip_analyzer

@st.cache_data
def load_clothing_data():
    """Load clothing data from local images or fallback to sample data"""
    image_loader = ImageLoader()
    
    # Try to load from local products directory first
    local_data = image_loader.load_products_from_directory()
    
    if not local_data.empty:
        return local_data
    else:
        # Fallback to sample data if no local images
        return get_sample_clothing_data()

def main():
    st.title("🎨 AI-Powered Fashion Stylist")
    st.markdown("Upload an inspiration look and let AI reconstruct it using available clothing items!")
    
    # Load components
    image_processor, color_analyzer, outfit_matcher, style_matcher, clip_analyzer = load_processors()
    clothing_data = load_clothing_data()
    image_loader = ImageLoader()
    
    # Initialize CLIP model
    with st.spinner("Caricamento modello CLIP LAION..."):
        clip_ready = clip_analyzer.initialize()
    
    # Sidebar for controls
    with st.sidebar:
        st.header("📸 Upload Inspiration")
        
        # Option to upload file or select from local looks
        upload_mode = st.radio(
            "Modalità di caricamento:",
            ["Carica file", "Seleziona da cartella looks"],
            help="Scegli se caricare un'immagine o selezionare da quelle salvate"
        )
        
        if upload_mode == "Carica file":
            uploaded_file = st.file_uploader(
                "Choose an inspiration look image",
                type=['png', 'jpg', 'jpeg'],
                help="Upload an image of a complete outfit for AI analysis"
            )
            if uploaded_file is not None:
                st.session_state.uploaded_image = uploaded_file
                st.session_state.image_source = "upload"
        else:
            # Load from local directory
            user_looks = image_loader.load_user_looks()
            if user_looks:
                selected_look = st.selectbox(
                    "Seleziona un look:",
                    options=[look['name'] for look in user_looks],
                    help="Scegli un look dalla cartella images/looks/"
                )
                if selected_look:
                    selected_path = next(look['path'] for look in user_looks if look['name'] == selected_look)
                    st.session_state.uploaded_image = selected_path
                    st.session_state.image_source = "local"
            else:
                st.info("Nessun look trovato in images/looks/. Aggiungi alcune immagini per utilizzare questa funzione.")
        
        st.header("⚙️ Impostazioni Analisi")
        color_clusters = st.slider("Colori Dominanti", 3, 10, 5, help="Numero di colori dominanti da estrarre")
        match_threshold = st.slider("Soglia di Corrispondenza", 0.1, 1.0, 0.7, help="Similarità minima per abbinamenti")
        
        # Algorithm selection
        algorithm_mode = st.radio(
            "Modalità di analisi:",
            ["AI Avanzato", "Riferimenti di stile", "Algoritmo base"],
            index=0 if clip_ready else 1,
            help="Scegli il metodo di analisi delle immagini"
        )
        
        use_clip = algorithm_mode == "AI Avanzato" and clip_ready
        use_style_references = algorithm_mode == "Riferimenti di stile"
        
        if st.button("🔍 Analizza e Ricostruisci", disabled=st.session_state.uploaded_image is None):
            analyze_and_reconstruct(image_processor, color_analyzer, outfit_matcher, style_matcher, clip_analyzer,
                                  clothing_data, image_loader, color_clusters, match_threshold, 
                                  use_clip, use_style_references)
        
        # Image management section
        st.header("📁 Gestione Immagini")
        show_image_stats(image_loader)
        
        # Style references info
        if st.expander("ℹ️ Riferimenti di Stile"):
            style_refs = image_loader.load_style_references()
            if style_refs:
                st.write(f"**{len(style_refs)} riferimenti di stile caricati:**")
                for ref in style_refs[:5]:  # Show first 5
                    st.text(f"• {ref['name']} ({ref['style_type']})")
                if len(style_refs) > 5:
                    st.text(f"... e altri {len(style_refs) - 5}")
            else:
                st.info("Aggiungi immagini di riferimento in images/style_references/ per guidare gli abbinamenti")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📷 Immagine di Ispirazione")
        if st.session_state.uploaded_image is not None:
            # Load image based on source
            if st.session_state.get('image_source') == 'local':
                image = image_loader.get_image_from_path(st.session_state.uploaded_image)
            else:
                image = Image.open(st.session_state.uploaded_image)
            
            if image:
                st.image(image, caption="Look di Ispirazione", use_column_width=True)
                
                # Show color analysis
                if st.session_state.analysis_complete:
                    show_color_analysis(image, color_analyzer, color_clusters)
            else:
                st.error("Errore nel caricamento dell'immagine")
        else:
            st.info("👆 Carica un'immagine di ispirazione per iniziare")
    
    with col2:
        st.header("✨ AI Reconstructed Outfit")
        if st.session_state.reconstructed_outfit is not None:
            show_reconstructed_outfit(st.session_state.reconstructed_outfit)
        else:
            st.info("🤖 AI reconstruction will appear here after analysis")
    
    # Available clothing items
    st.header("👕 Indumenti Disponibili")
    show_clothing_inventory(clothing_data, image_loader)

def analyze_and_reconstruct(image_processor, color_analyzer, outfit_matcher, style_matcher, clip_analyzer,
                          clothing_data, image_loader, color_clusters, match_threshold, 
                          use_clip, use_style_references):
    """Analyze the uploaded image and reconstruct the outfit"""
    
    with st.spinner("🧠 L'AI sta analizzando il look di ispirazione..."):
        # Load and process image
        if st.session_state.get('image_source') == 'local':
            image_loader = ImageLoader()
            image = image_loader.get_image_from_path(st.session_state.uploaded_image)
        else:
            image = Image.open(st.session_state.uploaded_image)
        
        if not image:
            st.error("Errore nel caricamento dell'immagine")
            return
        
        # Extract colors
        colors = color_analyzer.extract_dominant_colors(image, n_colors=color_clusters)
        
        # Analyze style patterns
        style_features = image_processor.extract_style_features(image)
        
        # Match clothing items
        if use_clip:
            # Use CLIP AI analysis
            st.info("🤖 Usando AI avanzato per analisi semantica")
            
            # Get semantic description
            semantic_desc = clip_analyzer.get_semantic_description(image)
            st.info(f"🎨 Analisi AI: {semantic_desc}")
            
            # Find matches using CLIP
            clothing_list = clothing_data.to_dict('records')
            clip_matches = clip_analyzer.find_best_clothing_matches(
                image, clothing_list, threshold=match_threshold
            )
            
            # Convert to outfit format
            matched_outfit = {}
            categories = ['shirt', 'pants', 'shoes', 'jacket', 'accessory']
            
            for category in categories:
                category_matches = [item for item in clip_matches if item['category'] == category]
                if category_matches:
                    best_match = category_matches[0]  # Already sorted by score
                    matched_outfit[category] = {
                        'name': best_match['name'],
                        'image_url': best_match['image_url'],
                        'primary_color': best_match['primary_color'],
                        'style': best_match['style'],
                        'description': best_match['description'],
                        'confidence': best_match['clip_score'],
                        'ai_detected_style': best_match.get('detected_style', 'unknown'),
                        'ai_color_style': best_match.get('detected_color_style', 'unknown'),
                        'clip_analysis': True
                    }
            
            st.session_state.best_reference = None
            
        elif use_style_references:
            # Load style references
            style_references = image_loader.load_style_references()
            
            if style_references:
                matched_outfit, best_reference = style_matcher.find_best_matches_with_references(
                    colors, style_features, clothing_data, style_references, threshold=match_threshold
                )
                st.session_state.best_reference = best_reference
                st.info(f"🎯 Stile di riferimento rilevato: {best_reference['data']['name'] if best_reference else 'Nessuno'}")
            else:
                # Fallback to basic matching if no references
                matched_outfit = outfit_matcher.find_best_matches(
                    colors, style_features, clothing_data, threshold=match_threshold
                )
                st.session_state.best_reference = None
                st.warning("⚠️ Nessun riferimento di stile trovato. Usando algoritmo base.")
        else:
            # Use basic matching
            matched_outfit = outfit_matcher.find_best_matches(
                colors, style_features, clothing_data, threshold=match_threshold
            )
            st.session_state.best_reference = None
        
        st.session_state.reconstructed_outfit = matched_outfit
        st.session_state.analysis_complete = True
        
    st.success("✅ Analisi completata! Controlla l'outfit ricostruito.")
    st.rerun()

def show_color_analysis(image, color_analyzer, n_colors):
    """Display color analysis results"""
    st.subheader("🎨 Color Analysis")
    
    colors = color_analyzer.extract_dominant_colors(image, n_colors=n_colors)
    
    # Create color palette visualization
    fig, ax = plt.subplots(1, 1, figsize=(8, 2))
    color_patches = []
    for i, color in enumerate(colors):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor=np.array(color)/255.0)
        ax.add_patch(rect)
        color_patches.append(f"RGB{tuple(color)}")
    
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.set_xticks(range(len(colors)))
    ax.set_xticklabels([f"Color {i+1}" for i in range(len(colors))], rotation=45)
    ax.set_title("Dominant Colors")
    ax.set_aspect('equal')
    
    st.pyplot(fig)
    plt.close()

def show_reconstructed_outfit(reconstructed_outfit):
    """Display the reconstructed outfit"""
    
    if not reconstructed_outfit or len(reconstructed_outfit) == 0:
        st.warning("⚠️ No suitable matches found. Try adjusting the match threshold.")
        return
    
    st.subheader("🎯 Best Matches")
    
    for category, item in reconstructed_outfit.items():
        if item:
            with st.expander(f"{category.title()}: {item['name']}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(item['image_url'], caption=item['name'], width=150)
                
                with col2:
                    st.metric("Match Score", f"{item['confidence']:.1%}")
                    st.write(f"**Colore:** {item['primary_color']}")
                    st.write(f"**Stile:** {item['style']}")
                    
                    # Show AI analysis if available
                    if item.get('clip_analysis', False):
                        st.write(f"**AI Stile rilevato:** {item.get('ai_detected_style', 'N/A')}")
                        st.write(f"**AI Colori:** {item.get('ai_color_style', 'N/A')}")
                        st.caption("🤖 Analizzato con AI avanzato")
                    
                    # Show reference information if available
                    elif 'matched_reference' in item:
                        st.write(f"**Riferimento:** {item['reference_type']}")
                        st.caption(f"Basato su: {item['matched_reference']}")
                    
                    st.write(f"**Descrizione:** {item['description']}")

def show_clothing_inventory(clothing_data, image_loader):
    """Display available clothing items in a grid"""
    
    # Group by category
    categories = clothing_data['category'].unique()
    category_names = {
        'shirt': 'Camicie',
        'pants': 'Pantaloni', 
        'shoes': 'Scarpe',
        'jacket': 'Giacche',
        'accessory': 'Accessori'
    }
    
    for category in categories:
        st.subheader(f"{category_names.get(category, category.title())}")
        
        items = clothing_data[clothing_data['category'] == category]
        
        # Create columns for grid layout
        cols = st.columns(min(4, len(items)))
        
        for idx, (_, item) in enumerate(items.iterrows()):
            with cols[idx % 4]:
                # Check if it's a local file
                if item.get('local_file', False):
                    image = image_loader.get_image_from_path(item['image_url'])
                    if image:
                        st.image(image, caption=item['name'], width=120)
                    else:
                        st.error("Immagine non trovata")
                else:
                    st.image(item['image_url'], caption=item['name'], width=120)
                
                st.caption(f"Stile: {item['style']}")
                st.caption(f"Colore: {item['primary_color']}")

def show_image_stats(image_loader):
    """Show statistics about loaded images"""
    counts = image_loader.count_images_by_category()
    issues = image_loader.validate_image_directories()
    
    if issues:
        st.warning("⚠️ Configurazione cartelle:")
        for issue in issues:
            st.text(f"• {issue}")
        
        if st.button("📁 Crea cartelle mancanti"):
            import os
            os.makedirs("images/products/shirts", exist_ok=True)
            os.makedirs("images/products/pants", exist_ok=True)
            os.makedirs("images/products/shoes", exist_ok=True)
            os.makedirs("images/products/jackets", exist_ok=True)
            os.makedirs("images/products/accessories", exist_ok=True)
            os.makedirs("images/style_references", exist_ok=True)
            os.makedirs("images/looks", exist_ok=True)
            st.success("✅ Cartelle create!")
            st.rerun()
    
    st.write("📊 **Immagini caricate:**")
    category_names = {
        'shirt': 'Camicie',
        'pants': 'Pantaloni',
        'shoes': 'Scarpe', 
        'jacket': 'Giacche',
        'accessory': 'Accessori'
    }
    
    for category, count in counts.items():
        if category == 'style_references':
            st.text(f"• Riferimenti di stile: {count}")
        elif category == 'user_looks':
            st.text(f"• Look utente: {count}")
        else:
            name = category_names.get(category, category.title())
            st.text(f"• {name}: {count}")
    
    total_products = sum(count for key, count in counts.items() if key not in ['style_references', 'user_looks'])
    if total_products == 0:
        st.info("💡 Aggiungi i tuoi prodotti in images/products/ per utilizzare i tuoi vestiti!")
    
    if counts.get('style_references', 0) == 0:
        st.warning("⚠️ Aggiungi riferimenti di stile in images/style_references/ per migliorare gli abbinamenti")

if __name__ == "__main__":
    main()
