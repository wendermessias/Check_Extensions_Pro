import streamlit as st
import os
import io
import pyzipper
from PIL import Image
from moviepy import VideoFileClip

# 1. CONFIGURAÇÃO GLOBAL (Deve ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="Multi-Tool Pro Ultra",
    page_icon="🛠️",
    layout="wide"
)

# --- FUNÇÕES DE APOIO: IMAGENS ---

def imagem_valida(arquivo_bytes):
    try:
        img = Image.open(arquivo_bytes)
        img.verify()
        return True
    except Exception:
        return False


def processar_imagem_unica(arquivo):
    """Converte para JPG com fidelidade máxima (sem alterar dimensões)."""
    arquivo.seek(0)
    img = Image.open(arquivo)
    dpi = img.info.get('dpi')
    img_convertida = img.convert("RGB")
    buffer_img = io.BytesIO()
    # Qualidade 100 e Subsampling 0 garantem a melhor resolução possível
    img_convertida.save(
        buffer_img,
        format="JPEG",
        quality=100,
        subsampling=0,
        optimize=True,
        dpi=dpi if dpi else (72, 72)
    )
    return buffer_img.getvalue()


def processar_zip_imagens(arquivos_carregados, senha):
    """Gera ZIP de imagens com criptografia AES."""
    buffer_zip = io.BytesIO()
    total = len(arquivos_carregados)
    barra = st.progress(0)

    with pyzipper.AESZipFile(
            buffer_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        zipf.setpassword(senha.encode("utf-8"))
        for i, arquivo in enumerate(arquivos_carregados):
            if imagem_valida(arquivo):
                dados_jpg = processar_imagem_unica(arquivo)
                novo_nome = os.path.splitext(arquivo.name)[0] + ".jpg"
                zipf.writestr(novo_nome, dados_jpg)
            barra.progress((i + 1) / total)
    return buffer_zip.getvalue()


def processar_pdf(arquivos_carregados):
    """Junta múltiplas imagens em um único PDF de alta resolução."""
    lista_imagens = []
    for arquivo in arquivos_carregados:
        if imagem_valida(arquivo):
            arquivo.seek(0)
            img = Image.open(arquivo)
            lista_imagens.append(img.convert("RGB"))

    if lista_imagens:
        buffer_pdf = io.BytesIO()
        lista_imagens[0].save(
            buffer_pdf, format="PDF", save_all=True, append_images=lista_imagens[1:], resolution=100.0
        )
        return buffer_pdf.getvalue()
    return None


# --- FUNÇÕES DE APOIO: VÍDEOS ---

def processar_video_unico(arquivo_video):
    """Converte um único vídeo carregado para MP4."""
    with open("temp_input_vid", "wb") as f:
        f.write(arquivo_video.getbuffer())

    output_name = "video_convertido.mp4"
    with VideoFileClip("temp_input_vid") as clip:
        clip.write_videofile(output_name, codec="libx264", audio_codec="aac", verbose=False, logger=None)

    with open(output_name, "rb") as f:
        data = f.read()

    os.remove("temp_input_vid")
    os.remove(output_name)
    return data


def processar_zip_videos(videos_carregados, senha):
    """Converte múltiplos vídeos e empacota em ZIP com senha."""
    buffer_zip = io.BytesIO()
    total = len(videos_carregados)
    barra = st.progress(0)
    status = st.empty()

    with pyzipper.AESZipFile(
            buffer_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        zipf.setpassword(senha.encode("utf-8"))

        for i, vid in enumerate(videos_carregados):
            status.text(f"Convertendo vídeo {i + 1} de {total}: {vid.name}")

            with open("temp_in", "wb") as f:
                f.write(vid.getbuffer())

            temp_out = "temp_out.mp4"
            with VideoFileClip("temp_in") as clip:
                clip.write_videofile(temp_out, codec="libx264", audio_codec="aac", verbose=False, logger=None)

            with open(temp_out, "rb") as f:
                zipf.writestr(os.path.splitext(vid.name)[0] + ".mp4", f.read())

            os.remove("temp_in")
            os.remove(temp_out)
            barra.progress((i + 1) / total)

    status.text("✅ Todos os vídeos foram convertidos e compactados!")
    return buffer_zip.getvalue()


# --- INTERFACES (ABAS) ---

def aba_imagens():
    st.title("🖼️ Conversor de Imagens Ultra HD")
    st.markdown("Conversão para **JPG** ou **PDF** mantendo dimensões originais e máxima nitidez.")

    arquivos = st.file_uploader("Arraste suas imagens aqui", type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "heic"],
                                accept_multiple_files=True)

    if arquivos:
        qtd = len(arquivos)
        senha = ""
        bloquear = False

        with st.sidebar:
            st.header("⚙️ Configurações de Imagem")
            formato = st.selectbox("Formato de Saída", ["JPG (Individual/ZIP)", "PDF (Único Arquivo)"])

            if qtd > 1 and formato == "JPG (Individual/ZIP)":
                st.warning("🔒 Senha Obrigatória para ZIP.")
                senha = st.text_input("Senha do arquivo ZIP", type="password")
                if not senha:
                    st.error("Defina uma senha.")
                    bloquear = True

            nome_sugerido = os.path.splitext(arquivos[0].name)[0] if qtd == 1 else "meu_pacote_imagens"
            nome_final = st.text_input("Nome do arquivo final", value=nome_sugerido)

        if st.button("🚀 Iniciar Processamento de Imagens", disabled=bloquear):
            with st.spinner("Processando imagens..."):
                if formato == "PDF (Único Arquivo)":
                    pdf_data = processar_pdf(arquivos)
                    st.download_button("📥 Baixar PDF", pdf_data, f"{nome_final}.pdf", "application/pdf")
                elif qtd == 1:
                    img_data = processar_imagem_unica(arquivos[0])
                    st.download_button("📥 Baixar JPG", img_data, f"{nome_final}.jpg", "image/jpeg")
                else:
                    zip_data = processar_zip_imagens(arquivos, senha)
                    st.download_button("📥 Baixar ZIP Protegido", zip_data, f"{nome_final}.zip", "application/zip")


def aba_videos():
    st.title("🎬 Conversor de Vídeos para MP4")
    st.markdown("Converta vídeos (até **1 GB**) para MP4 real com alta compatibilidade.")

    arquivos_vid = st.file_uploader("Arraste seus vídeos aqui", type=["avi", "mkv", "mov", "wmv", "flv", "webm"],
                                    accept_multiple_files=True)

    if arquivos_vid:
        qtd = len(arquivos_vid)
        senha_vid = ""
        bloquear_vid = False

        with st.sidebar:
            st.header("⚙️ Configurações de Vídeo")
            if qtd > 1:
                st.warning("🔒 Senha Obrigatória para ZIP de vídeos.")
                senha_vid = st.text_input("Senha para o ZIP de vídeos", type="password")
                if not senha_vid:
                    st.error("Defina uma senha.")
                    bloquear_vid = True

            nome_sugerido = os.path.splitext(arquivos_vid[0].name)[0] if qtd == 1 else "meu_pacote_videos"
            nome_final_vid = st.text_input("Nome do arquivo final", value=nome_sugerido)

        if st.button("🚀 Iniciar Conversão de Vídeos", disabled=bloquear_vid):
            with st.spinner("Processando vídeos... Ficheiros grandes podem levar tempo."):
                if qtd == 1:
                    vid_data = processar_video_unico(arquivos_vid[0])
                    st.success("Conversão concluída!")
                    st.download_button("📥 Baixar MP4", vid_data, f"{nome_final_vid}.mp4", "video/mp4")
                else:
                    zip_vid_data = processar_zip_videos(arquivos_vid, senha_vid)
                    st.download_button("📥 Baixar ZIP de Vídeos", zip_vid_data, f"{nome_final_vid}.zip",
                                       "application/zip")

# --- MENU PRINCIPAL (NAVEGAÇÃO) ---

st.sidebar.title("🛠️ Menu Pro")
escolha = st.sidebar.radio("Escolha a Ferramenta:", ["Imagens Ultra HD", "Vídeos para MP4"])

if escolha == "Imagens Ultra HD":
    aba_imagens()
else:
    aba_videos()

st.sidebar.divider()
st.sidebar.caption("Foco em Qualidade e Segurança.")
st.sidebar.caption("Desenvolvido por [Wendermessias](https://github.com/wendermessias)")