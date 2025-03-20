import streamlit as st 
import pandas as pd
from auth import check_password
import os
import shutil

if not check_password():
    st.stop()

st.title("⚙️ Configurações do Sistema")

if st.session_state.user_level == 'admin':
    # User Permissions Management
    st.subheader("🔐 Gerenciamento de Permissões")
    
    usuarios_df = pd.read_csv("data/usuarios.csv")
    for _, user in usuarios_df.iterrows():
        if user['usuario'] != 'admin':  # Skip admin user
            st.write(f"### 👤 {user['usuario']}")
            user_perms = user['permissoes'].split(',') if isinstance(user['permissoes'], str) else []
            
            col1, col2 = st.columns(2)
            with col1:
                new_perms = []
                if st.checkbox("Produtos", value='produtos' in user_perms):
                    new_perms.append('produtos')
                if st.checkbox("Financeiro", value='financeiro' in user_perms):
                    new_perms.append('financeiro')
                if st.checkbox("Relatórios", value='relatorios' in user_perms):
                    new_perms.append('relatorios')
                
            with col2:
                if st.checkbox("Assistente IA", value='assistente' in user_perms):
                    new_perms.append('assistente')
                if st.checkbox("Configurações", value='configuracoes' in user_perms):
                    new_perms.append('configuracoes')
                if st.checkbox("Backup", value='backup' in user_perms):
                    new_perms.append('backup')
            
            # Loja is always included
            new_perms.append('loja')
            
            # Update permissions if changed
            new_perms_str = ','.join(new_perms)
            if new_perms_str != user['permissoes']:
                usuarios_df.loc[usuarios_df['usuario'] == user['usuario'], 'permissoes'] = new_perms_str
                usuarios_df.to_csv("data/usuarios.csv", index=False)
                st.success(f"✅ Permissões atualizadas para {user['usuario']}")

# Gerenciamento de Usuários
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("👥 Gerenciamento de Usuários")

usuarios_df = pd.read_csv("data/usuarios.csv")
if not usuarios_df.empty:
    st.write("### Usuários Cadastrados")
    edited_df = st.data_editor(
        usuarios_df,
        column_config={
            "usuario": "Usuário",
            "nivel": st.column_config.SelectboxColumn(
                "Nível",
                options=["admin", "gerente", "vendedor"],
            )
        },
        hide_index=True,
    )
    
    if st.button("💾 Salvar Alterações"):
        edited_df.to_csv("data/usuarios.csv", index=False)
        st.success("✅ Alterações salvas com sucesso!")

# Adicionar novo usuário
with st.expander("➕ Adicionar Novo Usuário"):
    with st.form("novo_usuario"):
        novo_usuario = st.text_input("👤 Nome de Usuário")
        nova_senha = st.text_input("🔑 Senha", type="password")
        nivel = st.selectbox("🎖️ Nível", ["admin", "gerente", "vendedor"])
        if st.form_submit_button("Cadastrar"):
            sucesso, msg = create_user(novo_usuario, nova_senha, nivel)
            if sucesso:
                st.success(msg)
            else:
                st.error(msg)

st.markdown('</div>', unsafe_allow_html=True)

# Estilo para cards
st.markdown("""
<style>
.config-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Upload da Logo
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🖼️ Logo da Empresa")
uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    with open("logo.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Logo atualizada com sucesso!")
    st.image("logo.png", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Upload do Vídeo de Fundo
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🎥 Vídeo de Fundo")
st.info("O vídeo será usado como plano de fundo na tela de login")
video_file = st.file_uploader("Upload do Vídeo de Fundo", type=['mp4'])
if video_file is not None:
    with open("background.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    st.success("✅ Vídeo de fundo atualizado com sucesso!")
    st.video(video_file)
st.markdown('</div>', unsafe_allow_html=True)

# Configurações de Usuário
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("👤 Configurações de Usuário")
with st.expander("🔐 Alterar Senha"):
    with st.form("alterar_senha"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        if st.form_submit_button("Alterar Senha"):
            if nova_senha == confirmar_senha:
                st.success("✅ Senha alterada com sucesso!")
            else:
                st.error("❌ As senhas não conferem!")
st.markdown('</div>', unsafe_allow_html=True)
# Configurações de Notificações WhatsApp
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("📱 Configurações de WhatsApp")
whatsapp_number = st.text_input("Número do WhatsApp (com DDD)", placeholder="Ex: 11999999999")
enable_notifications = st.checkbox("Ativar notificações de atualizações")

if st.button("Salvar Configurações de WhatsApp"):
    # Aqui você pode implementar a lógica para salvar as configurações
    st.success("✅ Configurações de WhatsApp salvas com sucesso!")
st.markdown('</div>', unsafe_allow_html=True)

# Easter Egg Settings
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🎮 Easter Eggs")
if 'show_easter_egg' not in st.session_state:
    st.session_state.show_easter_egg = True

show_easter_egg = st.toggle("Mostrar pássaro voador", value=st.session_state.show_easter_egg)
if show_easter_egg != st.session_state.show_easter_egg:
    st.session_state.show_easter_egg = show_easter_egg
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)