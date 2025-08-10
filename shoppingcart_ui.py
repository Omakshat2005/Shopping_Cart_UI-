import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="ShopVibe - Modern Shopping Cart",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, colorful design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
        border-left: 5px solid;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    .price-low {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .price-medium {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .price-high {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .cart-summary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .checkout-option {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .checkout-option:hover {
        border-color: #667eea;
        transform: scale(1.02);
    }
    
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'order_confirmed' not in st.session_state:
    st.session_state.order_confirmed = False

# Sample products data
products_data = [
    {"id": 1, "name": "Wireless Headphones", "price": 299, "emoji": "🎧", "category": "Electronics"},
    {"id": 2, "name": "Smart Watch", "price": 799, "emoji": "⌚", "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 1299, "emoji": "☕", "category": "Appliances"},
    {"id": 4, "name": "Book Set", "price": 450, "emoji": "📚", "category": "Books"},
    {"id": 5, "name": "Gaming Mouse", "price": 350, "emoji": "🖱️", "category": "Electronics"},
    {"id": 6, "name": "Backpack", "price": 899, "emoji": "🎒", "category": "Fashion"},
    {"id": 7, "name": "Smartphone", "price": 15999, "emoji": "📱", "category": "Electronics"},
    {"id": 8, "name": "Sunglasses", "price": 199, "emoji": "🕶️", "category": "Fashion"},
]

products_df = pd.DataFrame(products_data)

def get_price_class(price):
    if price < 500:
        return "price-low"
    elif price <= 1000:
        return "price-medium"
    else:
        return "price-high"

def get_price_color(price):
    if price < 500:
        return "#4CAF50"
    elif price <= 1000:
        return "#FF9800"
    else:
        return "#f44336"

def add_to_cart(product):
    # Check if product already exists in cart
    for item in st.session_state.cart:
        if item['id'] == product['id']:
            item['quantity'] += 1
            return
    
    # Add new product to cart
    product['quantity'] = 1
    st.session_state.cart.append(product)

def remove_from_cart(product_id):
    st.session_state.cart = [item for item in st.session_state.cart if item['id'] != product_id]

def update_quantity(product_id, quantity):
    for item in st.session_state.cart:
        if item['id'] == product_id:
            item['quantity'] = max(1, quantity)
            break

def get_cart_total():
    return sum(item['price'] * item['quantity'] for item in st.session_state.cart)

def get_total_items():
    return sum(item['quantity'] for item in st.session_state.cart)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🛍️ ShopVibe Navigation")
    
    # Cart summary in sidebar
    total_items = get_total_items()
    if total_items > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50, #45a049); 
                    color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <h4>🛒 Cart: {total_items} items</h4>
            <h3>₹{get_cart_total():,}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.order_confirmed = False
        st.rerun()
    
    if st.button("🛍️ Products", use_container_width=True):
        st.session_state.current_page = 'products'
        st.session_state.order_confirmed = False
        st.rerun()
    
    if st.button(f"🛒 Cart ({total_items})", use_container_width=True):
        st.session_state.current_page = 'cart'
        st.session_state.order_confirmed = False
        st.rerun()
    
    if st.button("💳 Checkout", use_container_width=True, disabled=total_items == 0):
        st.session_state.current_page = 'checkout'
        st.session_state.order_confirmed = False
        st.rerun()

# Main content based on current page
if st.session_state.current_page == 'home':
    # Home Screen
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 4rem; margin: 0;">🛍️ ShopVibe</h1>
        <h2 style="margin: 0.5rem 0; font-weight: 300;">Your Favorite Shopping Destination</h2>
        <p style="font-size: 1.2rem; opacity: 0.9;">Discover amazing products with great deals!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Shopping", use_container_width=True, type="primary"):
            st.session_state.current_page = 'products'
            st.rerun()
    
    with col2:
        if st.button("📱 View Categories", use_container_width=True):
            st.session_state.current_page = 'products'
            st.rerun()
    
    with col3:
        if st.button(f"🛒 My Cart ({total_items})", use_container_width=True):
            st.session_state.current_page = 'cart'
            st.rerun()
    
    # Feature highlights
    st.markdown("---")
    st.markdown("### ✨ Why Choose ShopVibe?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">⚡</div>
            <h4>Fast Delivery</h4>
            <p>Quick and reliable shipping</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🔒</div>
            <h4>Secure Payment</h4>
            <p>Safe and encrypted transactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">💯</div>
            <h4>Quality Products</h4>
            <p>Carefully curated items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🎁</div>
            <h4>Great Deals</h4>
            <p>Unbeatable prices daily</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'products':
    # Products Screen
    st.markdown("# 🛍️ Our Products")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_category = st.selectbox("Filter by Category", ["All"] + list(products_df['category'].unique()))
    with col2:
        sort_by = st.selectbox("Sort by", ["Name", "Price (Low to High)", "Price (High to Low)"])
    
    # Filter and sort products
    filtered_products = products_df.copy()
    if selected_category != "All":
        filtered_products = filtered_products[filtered_products['category'] == selected_category]
    
    if sort_by == "Price (Low to High)":
        filtered_products = filtered_products.sort_values('price')
    elif sort_by == "Price (High to Low)":
        filtered_products = filtered_products.sort_values('price', ascending=False)
    else:
        filtered_products = filtered_products.sort_values('name')
    
    # Display products in grid
    cols = st.columns(3)
    
    for idx, (_, product) in enumerate(filtered_products.iterrows()):
        col = cols[idx % 3]
        
        with col:
            border_color = get_price_color(product['price'])
            
            st.markdown(f"""
            <div class="product-card" style="border-left-color: {border_color};">
                <div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">
                    {product['emoji']}
                </div>
                <h3 style="color: #333; margin-bottom: 0.5rem;">{product['name']}</h3>
                <p style="color: #666; margin-bottom: 1rem;">{product['category']}</p>
                <div class="{get_price_class(product['price'])}" style="margin-bottom: 1rem;">
                    ₹{product['price']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🛒 Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                add_to_cart(product.to_dict())
                st.success(f"✅ {product['name']} added to cart!")
                st.rerun()

elif st.session_state.current_page == 'cart':
    # Cart Screen
    st.markdown("# 🛒 Shopping Cart")
    
    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 5rem;">🛒</div>
            <h2>Your cart is empty</h2>
            <p style="font-size: 1.2rem; color: #666;">Add some amazing products to get started!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🛍️ Continue Shopping", type="primary", use_container_width=True):
            st.session_state.current_page = 'products'
            st.rerun()
    
    else:
        for item in st.session_state.cart:
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
            
            with col1:
                st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{item['emoji']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{item['name']}**")
                st.markdown(f"<span class='{get_price_class(item['price'])}'>₹{item['price']:,} each</span>", unsafe_allow_html=True)
            
            with col3:
                new_quantity = st.number_input(f"Qty", min_value=1, value=item['quantity'], key=f"qty_{item['id']}")
                if new_quantity != item['quantity']:
                    update_quantity(item['id'], new_quantity)
                    st.rerun()
            
            with col4:
                st.markdown(f"**₹{item['price'] * item['quantity']:,}**")
            
            with col5:
                if st.button("🗑️", key=f"remove_{item['id']}", help="Remove item"):
                    remove_from_cart(item['id'])
                    st.rerun()
        
        # Cart summary
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="cart-summary">
                <h3>Order Summary</h3>
                <p>Items: {get_total_items()}</p>
                <h2>Total: ₹{get_cart_total():,}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 Proceed to Checkout", type="primary", use_container_width=True):
                st.session_state.current_page = 'checkout'
                st.rerun()

elif st.session_state.current_page == 'checkout':
    # Checkout Screen
    if st.session_state.order_confirmed:
        st.markdown("""
        <div class="success-message">
            <div style="font-size: 4rem;">✅</div>
            <h1>Order Confirmed!</h1>
            <p style="font-size: 1.2rem;">Thank you for shopping with ShopVibe!</p>
            <p>Your order will be delivered soon.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", type="primary", use_container_width=True):
            st.session_state.current_page = 'home'
            st.session_state.cart = []
            st.session_state.order_confirmed = False
            st.rerun()
    
    else:
        st.markdown("# 💳 Checkout")
        
        if not st.session_state.cart:
            st.warning("Your cart is empty. Add some products first!")
            if st.button("🛍️ Go to Products", type="primary"):
                st.session_state.current_page = 'products'
                st.rerun()
        
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📋 Order Summary")
                
                for item in st.session_state.cart:
                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; 
                                display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{item['emoji']}</span>
                            <strong>{item['name']}</strong> x {item['quantity']}
                        </div>
                        <div style="font-weight: bold;">₹{item['price'] * item['quantity']:,}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 💳 Payment Options")
                
                payment_method = st.radio(
                    "Choose payment method:",
                    ["💳 Credit/Debit Card", "📱 UPI Payment", "🚚 Cash on Delivery"],
                    key="payment_method"
                )
                
                if payment_method == "💳 Credit/Debit Card":
                    st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                    col_exp, col_cvv = st.columns(2)
                    with col_exp:
                        st.text_input("Expiry Date", placeholder="MM/YY")
                    with col_cvv:
                        st.text_input("CVV", placeholder="123")
                
                elif payment_method == "📱 UPI Payment":
                    st.text_input("UPI ID", placeholder="your-upi@bank")
                    st.info("You will be redirected to your UPI app to complete the payment.")
                
                else:
                    st.info("You can pay in cash when your order is delivered.")
                
                st.markdown("### 📍 Delivery Information")
                st.text_area("Delivery Address", placeholder="Enter your full address...")
                st.text_input("Phone Number", placeholder="Enter your mobile number")
            
            with col2:
                st.markdown(f"""
                <div class="cart-summary">
                    <h3>💰 Payment Details</h3>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Items ({get_total_items()}):</span>
                        <span>₹{get_cart_total():,}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Delivery:</span>
                        <span>₹50</span>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.3);">
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                        <strong>Total:</strong>
                        <strong>₹{get_cart_total() + 50:,}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎉 Confirm Purchase", type="primary", use_container_width=True):
                    with st.spinner("Processing your order..."):
                        time.sleep(2)
                    st.session_state.order_confirmed = True
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🛍️ <strong>ShopVibe</strong> - Your favorite shopping destination</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)