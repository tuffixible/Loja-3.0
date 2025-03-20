
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from auth import check_password

if not check_password():
    st.stop()

st.title("📥 Backup e Restauração")

if st.button("Gerar Backup"):
    try:
        data = {
            "produtos": pd.read_csv("data/produtos.csv").to_dict(),
            "financeiro": pd.read_csv("data/financeiro.csv").to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        st.download_button(
            "⬇️ Download Backup",
            data=json.dumps(data, indent=2),
            file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        st.success("Backup gerado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao gerar backup: {str(e)}")

uploaded_file = st.file_uploader("Restaurar Backup", type=['json'])
if uploaded_file:
    if st.button("Confirmar Restauração"):
        try:
            data = json.loads(uploaded_file.getvalue())
            pd.DataFrame(data["produtos"]).to_csv("data/produtos.csv", index=False)
            pd.DataFrame(data["financeiro"]).to_csv("data/financeiro.csv", index=False)
            st.success("Backup restaurado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao restaurar backup: {str(e)}")
