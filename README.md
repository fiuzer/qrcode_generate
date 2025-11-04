# Gerador de QR Code Dinâmico com Flask

Este projeto é um **gerador de QR Code online**, construído com **Python** (Flask) e front-end em **HTML, CSS e JavaScript**, que permite criar QR Codes personalizados em tempo real, visualizar prévias e fazer o download da imagem gerada.  

O sistema é totalmente responsivo, moderno e permite escolher cores, fundo transparente e link personalizado para o QR Code.

---

## 🛠 Tecnologias Utilizadas

- **Python 3**: Lógica de backend e geração de QR Codes.  
- **Flask**: Framework web para servir páginas e lidar com requisições HTTP.  
- **qrcode**: Biblioteca Python para geração de QR Codes.  
- **HTML / CSS / JS**: Interface de usuário interativa e responsiva.  
- **AJAX / Fetch API**: Atualização dinâmica da pré-visualização do QR Code sem recarregar a página.  

---

## 🔹 Funcionalidades

1. **Entrada de URL personalizada**  
   - O usuário digita o link que deseja transformar em QR Code.  
   - Caso nenhum link seja informado, o QR Code padrão aponta para `[https://bravus.com.br](https://www.bravuscompany.com/)`.

2. **Customização de cores**  
   - Cor do QR Code (foreground).  
   - Cor de fundo (background).  
   - Opção de fundo transparente.

3. **Pré-visualização em tempo real**  
   - O QR Code é atualizado instantaneamente conforme o usuário altera URL ou cores.

4. **Download do QR Code**  
   - O QR Code gerado pode ser baixado como imagem PNG clicando no botão de download.

5. **Responsividade**  
   - Funciona bem em desktops e dispositivos móveis, adaptando layout e tamanho do QR Code.

---

## ⚙️ Estrutura do Projeto

- `app.py`:  
  - Define rotas para a página principal (`/`), geração de pré-visualização (`/preview`) e download do QR Code (`/download/<filename>`).  
  - Cria diretório `static/qrcodes` caso não exista.  
  - Gera QR Codes com cores personalizadas e opção de fundo transparente usando a biblioteca `qrcode`.

- `index.html`:  
  - Formulário para entrada de URL, seleção de cores e fundo transparente.  
  - Área de pré-visualização do QR Code em tempo real.  
  - Botão de download do QR Code gerado.

- `styles.css`:  
  - Layout moderno com cores preta e laranja.  
  - Estilo responsivo e interativo para inputs, botões e pré-visualização.

---

## 🚀 Como Executar

1. Clone o projeto:  
```bash
git clone https://github.com/fiuzer/qrcode_generate
cd gerador-qrcode
```
2. Instale dependências:
```bash
pip install -r requirements.txt
```
3. Execute a aplicação:
```bash
python app.py
```

4. Acesse no navegador:

```cpp
http://127.0.0.1:5000/
```

## 🔧 Como Usar

1. Digite a URL que deseja converter em QR Code.
2. Personalize a cor do QR Code e a cor de fundo, ou marque a opção de fundo transparente.
3. Veja a pré-visualização em tempo real.
4. Clique em **Baixar QR Code** para salvar a imagem.

---

## 📌 Observações

- Todos os QR Codes gerados são salvos no diretório `static/qrcodes`.
- O arquivo de pré-visualização é sempre `preview.png`, sobrescrevendo a versão anterior.
- O sistema suporta **cores personalizadas** e **transparência parcial** no fundo do QR Code.
