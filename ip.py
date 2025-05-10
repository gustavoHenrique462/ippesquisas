import streamlit as st
import requests
import os
from deep_translator import GoogleTranslator
from dotenv import load_dotenv


load_dotenv()

chave_api = os.getenv("CHAVE_API")

def obter_info_ip(ip, chave_api):
    url = f"https://api.api-ninjas.com/v1/iplookup?address={ip}"
    headers = {'X-Api-Key': st.secrets['chave_api']}
    try:
        resposta = requests.get(url, headers=headers)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter informações do IP: {e}")
        return None


def traduzir_texto(texto, idioma_destino):
    try:
        traduzido = GoogleTranslator(source='auto', target=idioma_destino).translate(texto)
        return traduzido
    except Exception as e:
        st.error(f"Erro ao traduzir o texto: {e}")
        return texto


def main():
    st.title("🕵️ Ferramenta Hacker para pesquisa de IPs 🔍")
    st.write ('IPS públicos para teste:')
    st.write('1.1.1.1: Cloudflare DNS')
    st.write('208.67.222.222: OpenDNS (Cisco)')
    st.write('8.8.4.4: Google DNS secundário')
    st.write('23.22.63.114: Amazon AWS (um dos servidores EC2)')
    st.write('20.36.130.1: Microsoft Azure')

    ip = st.text_input("Digite o endereço IP para encontrar localização e mais informações:", "8.8.8.8")
    idioma_destino = st.selectbox("Escolha o idioma para tradução", ["en", "es", "fr", "de", "pt"])

    if st.button("Consultar"):
        if chave_api:
            info_ip = obter_info_ip(ip, chave_api)
            if info_ip:
                st.subheader(traduzir_texto("Informações do IP", idioma_destino))
                st.write(f"**{traduzir_texto('Endereço IP:', idioma_destino)}** {info_ip.get('address')}")
                st.write(f"**{traduzir_texto('Estado/Região:', idioma_destino)}** {info_ip.get('region')}")
                st.write(f"**{traduzir_texto('País:', idioma_destino)}** {info_ip.get('country')}")
                st.write(f"**{traduzir_texto('Código do País:', idioma_destino)}** {info_ip.get('country_code')}")
                st.write(f"**{traduzir_texto('Código do Estado:', idioma_destino)}** {info_ip.get('region_code')}")
                st.write(f"**{traduzir_texto('Fuso Horário:', idioma_destino)}** {info_ip.get('timezone')}")
            else:
                st.warning(traduzir_texto("Nenhuma informação encontrada para o IP fornecido.", idioma_destino))
        else:
            st.error("A chave da API não foi encontrada. Verifique se a variável de ambiente 'CHAVE_API' está definida.")


if __name__ == "__main__":
    main()

