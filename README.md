🖼️ Check Extensions Ultra & Converter
Este projeto é uma ferramenta web de alta performance desenvolvida em Python com Streamlit. Ele foi desenhado para quem precisa converter imagens de diversos formatos para JPG ou PDF sem perder um único pixel de qualidade, mantendo as dimensões originais e garantindo a máxima fidelidade de cores.


✨ O que há de novo (Versão Ultra)
Diferente de conversores comuns que sacrificam a nitidez para reduzir o tamanho do arquivo, esta ferramenta foca na Fidelidade Máxima:

Qualidade 100%: Sem artefatos de compressão JPEG.

Subsampling 0: Preservação total da nitidez das cores (Chroma Subsampling 4:4:4).

Fidelidade Dimensional: As dimensões de largura e altura são preservadas em 100%, assim como o DPI original.

Conversão para PDF: Agora você pode agrupar todas as suas imagens em um único documento PDF profissional.

🚀 Funcionalidades Principais
Upload Multiformato: Suporte para PNG, WEBP, BMP, TIFF, HEIC e mais.

Validação em Tempo Real: O sistema verifica a integridade do cabeçalho da imagem antes do processamento.

Barra de Progresso Dinâmica: Acompanhe o status da conversão em tempo real, ideal para grandes volumes de arquivos.

Segurança Reforçada (ZIP): Compactação com criptografia AES-256. O sistema possui uma "trava de segurança" que impede o download de ZIPs sem a definição de uma senha.

Interface Inteligente:

1 Imagem: Download direto do arquivo convertido.

Múltiplas Imagens: Opção de empacotamento em ZIP ou fusão em um único PDF.



🚀 Tecnologias Utilizadas

Python - Linguagem base.
Streamlit - Framework para a interface web.
Pillow (PIL) - Processamento e conversão de imagens.
Pyzipper - Compactação de arquivos com criptografia avançada.
In-Memory Buffer (io) - Processamento ultra rápido sem criação de arquivos temporários no servidor.

📖 Como Rodar o Projeto
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/check-extensions.git
Instale as dependências:

Bash
pip install streamlit pillow pyzipper
Execute a aplicação:

Bash
streamlit run app.py

🔒 Segurança e Privacidade
Os arquivos são processados inteiramente na memória RAM. Assim que a sessão é encerrada ou a página é atualizada, os dados são descartados, garantindo que suas imagens não fiquem armazenadas permanentemente no servidor.

Desenvolvido com foco em precisão e segurança. 🚀