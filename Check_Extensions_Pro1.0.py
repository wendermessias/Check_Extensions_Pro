import io
import os
import uuid

import imageio
import pyzipper
import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image

# --------------------------
# CONFIGURAÇÃO GLOBAL
# --------------------------
st.set_page_config(
    page_title="Multi-Tool Pro Ultra",
    page_icon="🛠️",
    layout="wide"
)

# --------------------------
# FUNÇÕES DE APOIO: IMAGENS
# --------------------------
def imagem_valida(arquivo_bytes):
    try:
        img = Image.open(arquivo_bytes)
        img.verify()
        arquivo_bytes.seek(0)
        return True
    except Exception:
        return False

def eh_formato_jpg(nome_arquivo):
    ext = os.path.splitext(nome_arquivo)[1].lower()
    return ext in ('.jpg', '.jpeg')

def processar_imagem_unica(arquivo):
    arquivo.seek(0)
    if eh_formato_jpg(arquivo.name):
        st.info(f"✅ {arquivo.name} já é JPG — mantendo original.")
        arquivo.seek(0)
        return arquivo.read()
    
    img = Image.open(arquivo)
    dpi = img.info.get('dpi')
    img_convertida = img.convert("RGB")
    buffer_img = io.BytesIO()
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

# --------------------------
# FUNÇÕES DE APOIO: VÍDEOS — CORRIGIDAS
# --------------------------
def processar_video_unico(arquivo_video):
    id_unico = str(uuid.uuid4())[:8]
    temp_in = f"temp_vid_in_{id_unico}.tmp"
    temp_out = f"temp_vid_out_{id_unico}.mp4"
    
    try:
        with open(temp_in, "wb") as f:
            f.write(arquivo_video.getbuffer())
        
        with VideoFileClip(temp_in) as clip:
            clip.write_videofile(
                temp_out,
                codec="libx264",
                audio_codec="aac",
                logger=None
            )
        
        with open(temp_out, "rb") as f:
            return f.read()
    finally:
        for arq in [temp_in, temp_out]:
            if os.path.exists(arq):
                try: os.remove(arq)
                except: pass

def processar_zip_videos(videos_carregados, senha):
    buffer_zip = io.BytesIO()
    total = len(videos_carregados)
    barra = st.progress(0)
    status = st.empty()
    id_lote = str(uuid.uuid4())[:8]
    
    with pyzipper.AESZipFile(
            buffer_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        zipf.setpassword(senha.encode("utf-8"))
        for i, vid in enumerate(videos_carregados):
            status.text(f"Convertendo vídeo {i + 1} de {total}: {vid.name}")
            temp_in = f"vid_{id_lote}_{i}.tmp"
            temp_out = f"vid_{id_lote}_{i}.mp4"
            
            try:
                with open(temp_in, "wb") as f:
                    f.write(vid.getbuffer())
                with VideoFileClip(temp_in) as clip:
                    clip.write_videofile(
                        temp_out,
                        codec="libx264",
                        audio_codec="aac",
                        logger=None 
                    )
                with open(temp_out, "rb") as f:
                    zipf.writestr(os.path.splitext(vid.name)[0] + ".mp4", f.read())
            finally:
                for arq in [temp_in, temp_out]:
                    if os.path.exists(arq):
                        try: os.remove(arq)
                        except: pass
            barra.progress((i + 1) / total)
    
    status.text("✅ Todos os vídeos foram convertidos e compactados!")
    return buffer_zip.getvalue()

# --------------------------
# FUNÇÕES DE APOIO: QUADROS
# --------------------------
def extrair_quadros_gif(arquivo_gif, intervalo=1):
    quadros_jpg = []
    arquivo_gif.seek(0)
    leitor = imageio.get_reader(arquivo_gif, format="gif")
    total_quadros = leitor.get_length()
    for idx in range(0, total_quadros, intervalo):
        quadro = leitor.get_data(idx)
        img = Image.fromarray(quadro).convert("RGB")
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=100, subsampling=0)
        quadros_jpg.append((idx, buffer.getvalue()))
    return quadros_jpg

def extrair_quadros_video(arquivo_video, intervalo_segundos=1):
    quadros_jpg = []
    id_tmp = str(uuid.uuid4())[:8]
    temp_vid = f"quadros_{id_tmp}.tmp"
    try:
        with open(temp_vid, "wb") as f:
            f.write(arquivo_video.getbuffer())
        with VideoFileClip(temp_vid) as clip:
            duracao = int(clip.duration)
            for t in range(0, duracao + 1, intervalo_segundos):
                quadro = clip.get_frame(t)
                img = Image.fromarray(quadro).convert("RGB")
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=100, subsampling=0)
                quadros_jpg.append((t, buffer.getvalue()))
    finally:
        if os.path.exists(temp_vid):
            os.remove(temp_vid)
    return quadros_jpg

def gerar_zip_quadros(quadros, senha, nome_base="quadro"):
    buffer_zip = io.BytesIO()
    with pyzipper.AESZipFile(
            buffer_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES
    ) as zipf:
        zipf.setpassword(senha.encode("utf-8"))
        for idx, dados in quadros:
            zipf.writestr(f"{nome_base}_{idx:04d}.jpg", dados)
    return buffer_zip.getvalue()

# --------------------------
# INTERFACES
# --------------------------
def aba_imagens():
    st.title("🖼️ Conversor de Imagens Ultra HD")
    st.markdown("Conversão para **JPG** ou **PDF** mantendo dimensões originais e máxima nitidez.")
    arquivos = st.file_uploader(
        "Arraste suas imagens aqui",
        type=["png", "jpg", "jpeg", "webp", "bmp", "tiff", "heic"],
        accept_multiple_files=True,
        key="upload_imagens"
    )
    if arquivos:
        qtd = len(arquivos)
        senha = ""
        bloquear = False
        with st.sidebar:
            st.header("⚙️ Configurações de Imagem")
            formato = st.selectbox(
                "Formato de Saída",
                ["JPG (Individual/ZIP)", "PDF (Único Arquivo)"],
                key="formato_saida"
            )
            if qtd > 1 and formato == "JPG (Individual/ZIP)":
                st.warning("🔒 Senha Obrigatória para ZIP.")
                senha = st.text_input("Senha do arquivo ZIP", type="password", key="senha_img")
                if not senha:
                    st.error("Defina uma senha.")
                    bloquear = True
            nome_sugerido = os.path.splitext(arquivos[0].name)[0] if qtd == 1 else "meu_pacote_imagens"
            nome_final = st.text_input("Nome do arquivo final", value=nome_sugerido, key="nome_img")
        if st.button("🚀 Iniciar Processamento de Imagens", disabled=bloquear, key="btn_img"):
            with st.spinner("Processando imagens..."):
                if formato == "PDF (Único Arquivo)":
                    pdf_data = processar_pdf(arquivos)
                    st.download_button("📥 Baixar PDF", pdf_data, f"{nome_final}.pdf", "application/pdf", key="dl_pdf")
                elif qtd == 1:
                    img_data = processar_imagem_unica(arquivos[0])
                    st.download_button("📥 Baixar JPG", img_data, f"{nome_final}.jpg", "image/jpeg", key="dl_jpg")
                else:
                    zip_data = processar_zip_imagens(arquivos, senha)
                    st.download_button("📥 Baixar ZIP Protegido", zip_data, f"{nome_final}.zip", "application/zip", key="dl_zip_img")

def aba_videos():
    st.title("🎬 Conversor de Vídeos para MP4")
    st.markdown("Converta vídeos (até **1 GB**) para MP4 real com alta compatibilidade.")
    arquivos_vid = st.file_uploader(
        "Arraste seus vídeos aqui",
        type=["avi", "mkv", "mov", "wmv", "flv", "webm", "mp4", "mpeg4"],
        accept_multiple_files=True,
        key="upload_videos"
    )
    if arquivos_vid:
        qtd = len(arquivos_vid)
        senha_vid = ""
        bloquear_vid = False
        with st.sidebar:
            st.header("⚙️ Configurações de Vídeo")
            if qtd > 1:
                st.warning("🔒 Senha Obrigatória para ZIP de vídeos.")
                senha_vid = st.text_input("Senha para o ZIP de vídeos", type="password", key="senha_vid")
                if not senha_vid:
                    st.error("Defina uma senha.")
                    bloquear_vid = True
            nome_sugerido = os.path.splitext(arquivos_vid[0].name)[0] if qtd == 1 else "meu_pacote_videos"
            nome_final_vid = st.text_input("Nome do arquivo final", value=nome_sugerido, key="nome_vid")
        if st.button("🚀 Iniciar Conversão de Vídeos", disabled=bloquear_vid, key="btn_vid"):
            with st.spinner("Processando vídeos... Arquivos grandes podem levar tempo."):
                try:
                    if qtd == 1:
                        vid_data = processar_video_unico(arquivos_vid[0])
                        st.success("✅ Conversão concluída!")
                        st.download_button(
                            "📥 Baixar MP4", vid_data,
                            f"{nome_final_vid}.mp4", "video/mp4", key="dl_mp4"
                        )
                    else:
                        zip_vid_data = processar_zip_videos(arquivos_vid, senha_vid)
                        st.download_button(
                            "📥 Baixar ZIP de Vídeos", zip_vid_data,
                            f"{nome_final_vid}.zip", "application/zip", key="dl_zip_vid"
                        )
                except Exception as e:
                    st.error(f"❌ Erro: {str(e)}")
                    st.info("💡 Dica: tente reduzir o tamanho do arquivo ou use formato mais comum.")

def aba_quadros():
    st.title("📸 Extrair Quadros para JPG")
    st.markdown("Transforme **GIFs** ou **vídeos** em imagens JPG de alta qualidade.")
    tipo_arquivo = st.radio("Tipo de Arquivo", ["GIF (.gif)", "Vídeo (.mp4, .avi, .mkv, ...)"], key="tipo_quadro")
    ext = ["gif"] if "GIF" in tipo_arquivo else ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"]
    arquivo = st.file_uploader("Faça o upload", type=ext, accept_multiple_files=False, key="upload_quadros")
    if arquivo:
        with st.sidebar:
            st.header("⚙️ Configurações de Extração")
            if "GIF" in tipo_arquivo:
                intervalo = st.slider("Extrair a cada quantos quadros?", 1, 10, 1, key="intervalo_gif")
            else:
                intervalo = st.slider("Extrair a cada quantos segundos?", 1, 30, 1, key="intervalo_vid")
            modo = st.radio("Modo de Download", ["Último quadro apenas", "Todos os quadros em ZIP"], key="modo_quadro")
            senha_quadros = ""
            bloquear_q = False
            if modo == "Todos os quadros em ZIP":
                st.warning("🔒 Senha obrigatória para ZIP.")
                senha_quadros = st.text_input("Senha do ZIP", type="password", key="senha_q")
                if not senha_quadros:
                    st.error("Defina uma senha.")
                    bloquear_q = True
            nome_base = st.text_input("Nome base dos arquivos", value=os.path.splitext(arquivo.name)[0], key="nome_quadro")
        if st.button("🚀 Extrair Quadros", disabled=bloquear_q, key="btn_quadro"):
            with st.spinner("Extraindo quadros..."):
                try:
                    if "GIF" in tipo_arquivo:
                        quadros = extrair_quadros_gif(arquivo, intervalo)
                    else:
                        quadros = extrair_quadros_video(arquivo, intervalo)
                    if not quadros:
                        st.warning("Nenhum quadro encontrado.")
                        return
                    st.success(f"✅ {len(quadros)} quadro(s) extraído(s)!")
                    if modo == "Último quadro apenas":
                        idx, dados = quadros[-1]
                        st.download_button(
                            "📥 Baixar Último Quadro (JPG)",
                            dados, f"{nome_base}_quadro_{idx}.jpg", "image/jpeg", key="dl_quadro"
                        )
                    else:
                        zip_dados = gerar_zip_quadros(quadros, senha_quadros, nome_base)
                        st.download_button(
                            "📥 Baixar ZIP com Todos os Quadros",
                            zip_dados, f"{nome_base}_quadros.zip", "application/zip", key="dl_zip_quadro"
                        )
                except Exception as e:
                    st.error(f"❌ Erro no processamento: {str(e)}")

# --------------------------
# MENU PRINCIPAL
# --------------------------
st.sidebar.title("🛠️ Menu Pro")
escolha = st.sidebar.radio(
    "Escolha a Ferramenta:",
    ["Imagens Ultra HD", "Vídeos para MP4", "Extrair Quadros para JPG"],
    key="menu_principal"
)

if escolha == "Imagens Ultra HD":
    aba_imagens()
elif escolha == "Vídeos para MP4":
    aba_videos()
else:
    aba_quadros()

st.sidebar.divider()
st.sidebar.caption("Foco em Qualidade e Segurança.")
st.sidebar.caption("Desenvolvido por [Wendermessias](https://github.com/wendermessias)")