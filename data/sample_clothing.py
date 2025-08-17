import pandas as pd

def get_sample_clothing_data():
    """Return sample clothing data for demonstration"""
    
    # Sample clothing items - you can replace these with your own images
    # Place your clothing images in: images/clothing/{category}/
    # Supported formats: JPG, JPEG, PNG
    clothing_items = [
        # Shirts
        {
            'name': 'Classic White Dress Shirt',
            'category': 'shirt',
            'primary_color': 'white',
            'style': 'formal',
            'description': 'Crisp white cotton dress shirt with solid color design',
            'image_url': 'https://picsum.photos/300/400?random=1'
        },
        {
            'name': 'Navy Blue Polo Shirt',
            'category': 'shirt',
            'primary_color': 'navy',
            'style': 'casual',
            'description': 'Navy blue cotton polo with solid color design',
            'image_url': 'https://picsum.photos/300/400?random=2'
        },
        {
            'name': 'Black T-Shirt',
            'category': 'shirt',
            'primary_color': 'black',
            'style': 'casual',
            'description': 'Basic black cotton t-shirt with solid color design',
            'image_url': 'https://picsum.photos/300/400?random=3'
        },
        {
            'name': 'Light Blue Oxford Shirt',
            'category': 'shirt',
            'primary_color': 'blue',
            'style': 'business',
            'description': 'Light blue oxford cotton shirt with subtle texture',
            'image_url': 'https://picsum.photos/300/400?random=4'
        },
        {
            'name': 'Striped Button-Down',
            'category': 'shirt',
            'primary_color': 'white',
            'style': 'casual',
            'description': 'White shirt with navy blue stripes pattern',
            'image_url': 'https://picsum.photos/300/400?random=5'
        },
        
        # Pants
        {
            'name': 'Dark Blue Jeans',
            'category': 'pants',
            'primary_color': 'navy',
            'style': 'casual',
            'description': 'Classic dark blue denim jeans with solid color',
            'image_url': 'https://picsum.photos/300/400?random=6'
        },
        {
            'name': 'Black Dress Pants',
            'category': 'pants',
            'primary_color': 'black',
            'style': 'formal',
            'description': 'Tailored black wool dress pants with solid color',
            'image_url': 'https://picsum.photos/300/400?random=7'
        },
        {
            'name': 'Khaki Chinos',
            'category': 'pants',
            'primary_color': 'beige',
            'style': 'business',
            'description': 'Khaki cotton chinos with solid color design',
            'image_url': 'https://picsum.photos/300/400?random=8'
        },
        {
            'name': 'Gray Wool Trousers',
            'category': 'pants',
            'primary_color': 'gray',
            'style': 'formal',
            'description': 'Light gray wool trousers with solid color',
            'image_url': 'https://picsum.photos/300/400?random=9'
        },
        {
            'name': 'Blue Athletic Shorts',
            'category': 'pants',
            'primary_color': 'blue',
            'style': 'sporty',
            'description': 'Royal blue athletic shorts with solid color',
            'image_url': 'https://picsum.photos/300/400?random=10'
        },
        
        # Shoes
        {
            'name': 'Black Leather Oxfords',
            'category': 'shoes',
            'primary_color': 'black',
            'style': 'formal',
            'description': 'Classic black leather oxford shoes with solid color',
            'image_url': 'https://picsum.photos/300/200?random=11'
        },
        {
            'name': 'Brown Leather Loafers',
            'category': 'shoes',
            'primary_color': 'brown',
            'style': 'business',
            'description': 'Brown leather penny loafers with solid color',
            'image_url': 'https://picsum.photos/300/200?random=12'
        },
        {
            'name': 'White Sneakers',
            'category': 'shoes',
            'primary_color': 'white',
            'style': 'casual',
            'description': 'Clean white leather sneakers with solid color',
            'image_url': 'https://picsum.photos/300/200?random=13'
        },
        {
            'name': 'Navy Canvas Shoes',
            'category': 'shoes',
            'primary_color': 'navy',
            'style': 'casual',
            'description': 'Navy blue canvas sneakers with solid color',
            'image_url': 'https://picsum.photos/300/200?random=14'
        },
        {
            'name': 'Running Shoes',
            'category': 'shoes',
            'primary_color': 'gray',
            'style': 'sporty',
            'description': 'Gray and white athletic running shoes',
            'image_url': 'https://picsum.photos/300/200?random=15'
        },
        
        # Jackets
        {
            'name': 'Navy Blazer',
            'category': 'jacket',
            'primary_color': 'navy',
            'style': 'formal',
            'description': 'Classic navy blue wool blazer with solid color',
            'image_url': 'https://picsum.photos/300/400?random=16'
        },
        {
            'name': 'Black Suit Jacket',
            'category': 'jacket',
            'primary_color': 'black',
            'style': 'formal',
            'description': 'Elegant black wool suit jacket with solid color',
            'image_url': 'https://picsum.photos/300/400?random=17'
        },
        {
            'name': 'Gray Cardigan',
            'category': 'jacket',
            'primary_color': 'gray',
            'style': 'casual',
            'description': 'Soft gray knit cardigan with solid color',
            'image_url': 'https://picsum.photos/300/400?random=18'
        },
        {
            'name': 'Brown Leather Jacket',
            'category': 'jacket',
            'primary_color': 'brown',
            'style': 'trendy',
            'description': 'Brown leather motorcycle jacket with solid color',
            'image_url': 'https://picsum.photos/300/400?random=19'
        },
        {
            'name': 'Blue Denim Jacket',
            'category': 'jacket',
            'primary_color': 'blue',
            'style': 'casual',
            'description': 'Classic blue denim jacket with solid color',
            'image_url': 'https://picsum.photos/300/400?random=20'
        },
        
        # Accessories
        {
            'name': 'Black Leather Belt',
            'category': 'accessory',
            'primary_color': 'black',
            'style': 'formal',
            'description': 'Classic black leather belt with solid color',
            'image_url': 'https://picsum.photos/300/100?random=21'
        },
        {
            'name': 'Brown Leather Belt',
            'category': 'accessory',
            'primary_color': 'brown',
            'style': 'business',
            'description': 'Brown leather belt with solid color design',
            'image_url': 'https://picsum.photos/300/100?random=22'
        },
        {
            'name': 'Silver Watch',
            'category': 'accessory',
            'primary_color': 'gray',
            'style': 'elegant',
            'description': 'Silver stainless steel watch with solid color',
            'image_url': 'https://picsum.photos/200/200?random=23'
        },
        {
            'name': 'Navy Tie',
            'category': 'accessory',
            'primary_color': 'navy',
            'style': 'formal',
            'description': 'Navy blue silk tie with solid color design',
            'image_url': 'https://picsum.photos/150/300?random=24'
        },
        {
            'name': 'Black Sunglasses',
            'category': 'accessory',
            'primary_color': 'black',
            'style': 'trendy',
            'description': 'Black frame sunglasses with solid color',
            'image_url': 'https://picsum.photos/250/150?random=25'
        }
    ]
    
    return pd.DataFrame(clothing_items)

def get_sample_inspiration_looks():
    """Return sample inspiration look data"""
    
    inspiration_looks = [
        {
            'name': 'Business Casual Look',
            'description': 'Navy blazer with khaki chinos and brown loafers',
            'style_tags': ['business', 'professional', 'classic'],
            'dominant_colors': ['navy', 'beige', 'brown'],
            'image_url': 'https://via.placeholder.com/400x600/000080,f5f5dc,8b4513/ffffff?text=Business+Look'
        },
        {
            'name': 'Casual Weekend',
            'description': 'Blue jeans with white t-shirt and sneakers',
            'style_tags': ['casual', 'relaxed', 'everyday'],
            'dominant_colors': ['blue', 'white'],
            'image_url': 'https://via.placeholder.com/400x600/1e3a8a,ffffff/000000?text=Casual+Look'
        },
        {
            'name': 'Formal Evening',
            'description': 'Black suit with white dress shirt and black oxfords',
            'style_tags': ['formal', 'elegant', 'evening'],
            'dominant_colors': ['black', 'white'],
            'image_url': 'https://via.placeholder.com/400x600/000000,ffffff/808080?text=Formal+Look'
        },
        {
            'name': 'Smart Casual',
            'description': 'Gray trousers with light blue shirt and brown belt',
            'style_tags': ['smart', 'versatile', 'modern'],
            'dominant_colors': ['gray', 'blue', 'brown'],
            'image_url': 'https://via.placeholder.com/400x600/808080,87ceeb,8b4513/ffffff?text=Smart+Casual'
        }
    ]
    
    return pd.DataFrame(inspiration_looks)
