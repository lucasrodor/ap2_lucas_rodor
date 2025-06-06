import streamlit as st

def titulo_centralizado(texto, tamanho="h2", cor="#444"):
    st.markdown(
        f"<{tamanho} style='text-align: center; color:{cor}; margin-bottom: 0.5em;'>{texto}</{tamanho}>",
        unsafe_allow_html=True
    )

def texto_destaque(texto, cor="#444"):
    st.markdown(f"""
    <div style='font-size:17px; color:{cor}; margin-bottom: 1em;'>
        {texto}
    </div>
    """, unsafe_allow_html=True)

def divisor(titulo=None):
    if titulo:
        st.markdown(f"<h4 style='margin-top:2em'>{titulo}</h4>", unsafe_allow_html=True)
    else:
        st.markdown("<hr style='margin-top:2em; margin-bottom:1em;'>", unsafe_allow_html=True)

def espaco(tamanho=2):
    for _ in range(tamanho):
        st.markdown("&nbsp;", unsafe_allow_html=True)

def aviso_personalizado(texto, tipo="info"):
    if tipo == "sucesso":
        st.success(f"✅ {texto}")
    elif tipo == "erro":
        st.error(f"❌ {texto}")
    elif tipo == "aviso":
        st.warning(f"⚠️ {texto}")
    else:
        st.info(f"ℹ️ {texto}")
