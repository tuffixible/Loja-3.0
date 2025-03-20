
import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(layout="wide", page_title="Xible Store - Loja")

# Custom CSS for modern store layout
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.store-header {
    background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
    padding: 40px 20px;
    color: white;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 40px;
}

.store-subheader {
    font-size: 1.2rem;
    opacity: 0.8;
    margin-top: 10px;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 30px;
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.product-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.product-image-container {
    position: relative;
    padding-top: 100%;
    background: #f8f9fa;
    overflow: hidden;
}

.product-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.product-card:hover .product-image {
    transform: scale(1.1);
}

.product-info {
    padding: 20px;
}

.product-category {
    font-size: 0.85rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.product-name {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2d3436;
    margin-bottom: 12px;
    line-height: 1.4;
}

.product-price {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2d3436;
    margin: 15px 0;
}

.product-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.size-badge {
    background: #f1f2f6;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    color: #2d3436;
}

.stock-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.in-stock {
    background: #c8e6c9;
    color: #1b5e20;
}

.low-stock {
    background: #fff3e0;
    color: #e65100;
}

.buy-button {
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, #141E30 0%, #243B55 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.buy-button:hover {
    opacity: 0.9;
    transform: translateY(-2px);
}

.filters {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

.stSelectbox > div > div {
    background: white;
}
</style>
""", unsafe_allow_html=True)

# Store Header
st.markdown("""
<div class="store-header">
    <h1>Xible Store Collection</h1>
    <p class="store-subheader">Descubra nossa coleção exclusiva de calçados</p>
</div>
""", unsafe_allow_html=True)

# Filters
with st.container():
    st.markdown('<div class="filters">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categoria_filter = st.multiselect("Categoria", ["Todos", "Tênis", "Chinelos", "Sapatos"], default="Todos")
    with col2:
        preco_range = st.slider("Faixa de Preço", 0, 1000, (0, 1000))
    with col3:
        ordem = st.selectbox("Ordenar por", ["Mais Relevantes", "Menor Preço", "Maior Preço"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Load and filter products
produtos_df = load_data("produtos")

if not produtos_df.empty:
    # Apply filters
    if "Todos" not in categoria_filter and categoria_filter:
        produtos_df = produtos_df[produtos_df['categoria'].isin(categoria_filter)]
    produtos_df = produtos_df[
        (produtos_df['preco_venda'] >= preco_range[0]) & 
        (produtos_df['preco_venda'] <= preco_range[1])
    ]
    
    # Apply sorting
    if ordem == "Menor Preço":
        produtos_df = produtos_df.sort_values('preco_venda')
    elif ordem == "Maior Preço":
        produtos_df = produtos_df.sort_values('preco_venda', ascending=False)
    
    # Display products
    st.markdown('<div class="product-grid">', unsafe_allow_html=True)
    
    for _, produto in produtos_df.iterrows():
        stock_status = 'in-stock' if produto['quantidade'] > 5 else 'low-stock'
        stock_text = 'Em Estoque' if produto['quantidade'] > 5 else 'Últimas Unidades'
        
        st.markdown(f"""
        <div class="product-card">
            <div class="product-image-container">
                <img src="uploads/{produto['imagem_path']}" class="product-image" 
                    onerror="this.src='https://via.placeholder.com/400x400?text=Imagem+Indisponível'">
            </div>
            <div class="product-info">
                <div class="product-category">{produto['categoria']}</div>
                <div class="product-name">{produto['nome']}</div>
                <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
                <div class="product-meta">
                    <span class="size-badge">Tam: {produto['tamanho']}</span>
                    <span class="stock-badge {stock_status}">{stock_text}</span>
                </div>
                <button class="buy-button">Adicionar ao Carrinho</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Nenhum produto disponível no momento.")
