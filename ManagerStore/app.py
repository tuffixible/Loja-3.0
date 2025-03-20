import streamlit as st
import pandas as pd
import os

# Configuração inicial da página
st.set_page_config(
    page_title="Xible Store Manager",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700&display=swap');

.main-header {
    font-family: 'Roboto', sans-serif;
    color: #1E88E5;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
    background: linear-gradient(120deg, #1E88E5, #1565C0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1E88E5;
}

.metric-label {
    font-size: 1rem;
    color: #666;
    margin-top: 0.5rem;
}

.notification {
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.notification.warning {
    background: #FFF3E0;
    color: #E65100;
    border-left: 4px solid #FF9800;
}

.notification.info {
    background: #E3F2FD;
    color: #1565C0;
    border-left: 4px solid #1E88E5;
}

.sidebar-menu {
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    transition: all 0.3s ease;
}
.sidebar-menu:hover {
    background: #f0f2f6;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# Initialize data directories
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Load data
@st.cache_data(ttl=300)
def load_data():
    try:
        produtos_df = pd.read_csv("data/produtos.csv")
        financeiro_df = pd.read_csv("data/financeiro.csv")
        return produtos_df, financeiro_df
    except Exception:
        return pd.DataFrame(), pd.DataFrame()

produtos_df, financeiro_df = load_data()

# Main interface
st.markdown('<h1 class="main-header">Xible Store Manager</h1>', unsafe_allow_html=True)

# Quick Stats
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    total_produtos = len(produtos_df) if not produtos_df.empty else 0
    st.markdown(f'<div class="metric-value">{total_produtos}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total de Produtos</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    receita_total = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
    st.markdown(f'<div class="metric-value">R$ {receita_total:,.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Receita Total</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5]) if not produtos_df.empty else 0
    st.markdown(f'<div class="metric-value">{produtos_baixo_estoque}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Produtos com Estoque Baixo</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Notifications
if produtos_baixo_estoque > 0:
    st.markdown(
        f'<div class="notification warning">⚠️ {produtos_baixo_estoque} produtos com estoque baixo</div>',
        unsafe_allow_html=True
    )

# Recent Updates
st.subheader("📢 Atualizações Recentes")
st.markdown(
    '<div class="notification info">🆕 Nova versão disponível com melhorias na interface</div>',
    unsafe_allow_html=True
)

# Quick Actions
st.subheader("⚡ Ações Rápidas")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📦 Novo Produto"):
        st.switch_page("pages/1_Produtos.py")
with col2:
    if st.button("💰 Nova Venda"):
        st.switch_page("pages/2_Financeiro.py")
with col3:
    if st.button("📊 Ver Relatórios"):
        st.switch_page("pages/3_Relatorios.py")

# Menu
st.sidebar.title("Menu Principal")
menu_items = {
    'Produtos': '📦',
    'Financeiro': '💰',
    'Relatórios': '📊',
    'Assistente': '🤖',
    'Configurações': '⚙️',
    'Backup': '💾',
    'Loja': '🛍️'
}

for item, icon in menu_items.items():
    st.sidebar.markdown(f"""
    <div class="sidebar-menu">
        <a href="/{item.lower()}" target="_self">{icon} {item}</a>
    </div>
    """, unsafe_allow_html=True)

st.write("""
### 👋 Bem-vindo ao Sistema!
Utilize o menu lateral para acessar todas as funcionalidades disponíveis.
""")