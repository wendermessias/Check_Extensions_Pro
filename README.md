# 🛠️ Check Extensions Ultra & Converter

---

## ✨ O que há de novo (Versão Ultra)

Mantivemos tudo que já era excelente e ampliamos para muito mais:

### 🖼️ Imagens — Fidelidade Máxima

Diferente de conversores comuns que sacrificam a nitidez para reduzir o tamanho do arquivo, esta ferramenta foca na **Fidelidade Máxima** :

- Qualidade 100%: Sem artefatos de compressão JPEG
- Subsampling 0: Preservação total da nitidez das cores (Chroma Subsampling 4:4:4)
- Fidelidade Dimensional: As dimensões de largura e altura são preservadas em 100%, assim como o DPI original
- **Inteligência de Formato:** Arquivos já em JPG/JPEG não são reprocessados — o sistema detecta automaticamente e mantém o original, evitando conversões desnecessárias
- Conversão para PDF: Agora você pode agrupar todas as suas imagens em um único documento PDF profissional

### 🎬 Vídeos — Conversão para MP4

- Conversão Universal: Transforma AVI, MKV, MOV, WMV, FLV, WebM e outros formatos em MP4 (H.264 + AAC)
- Suporte a arquivos de até 1 GB
- Lote Protegido: Vários vídeos convertidos e empacotados em ZIP protegido por senha
- Gerenciamento Seguro: Arquivos temporários com nomes únicos e limpeza automática, sem conflitos

### 📸 Extração de Quadros

- Extrai quadros de **GIFs** e de **vídeos**
- Controle de Intervalo: Defina quantos quadros extrair por segundo ou por passos
- Flexibilidade de Download: Salve apenas o último quadro ou todos em ZIP protegido
- Qualidade Preservada: Cada quadro salvo como JPG em resolução máxima

---

## 🚀 Tecnologias Utilizadas

- **Python** — Linguagem base
- **Streamlit** — Framework para a interface web
- **Pillow (PIL)** — Processamento e conversão de imagens
- **MoviePy** — Conversão e edição de vídeos
- **ImageIO** — Leitura e extração de quadros de GIFs
- **Pyzipper** — Compactação com criptografia AES-256
- **In-Memory Buffer (io)** — Processamento ultra rápido sem criação de arquivos permanentes
- **UUID** — Nomes únicos para arquivos temporários, sem conflitos

---

## 🔒 Segurança e Privacidade

Os arquivos são processados inteiramente na memória RAM. Assim que a sessão é encerrada ou a página é atualizada, os dados são descartados, garantindo que suas imagens e vídeos não fiquem armazenados permanentemente no servidor.

- ✅ Processamento em memória — sem deixar rastros
- ✅ Limpeza automática de arquivos temporários
- ✅ Criptografia forte em todos os ZIPs
- ✅ Senha obrigatória para empacotamento

Desenvolvido com foco em precisão, velocidade e segurança. 🚀
Desenvolvido por Wendermessias
