☀️ Photography Journey: Seu Mentor AI & Espaço Criativo
Photography Journey é uma ferramenta pensada para fotógrafos que buscam evoluir sua visão artística. Utilizando a inteligência do Google Gemini, o projeto analisa suas capturas (Canon T5i, iPhone 14 Pro ou qualquer outra câmera) para oferecer feedbacks construtivos sobre composição, técnica e edição.


--- 

🎨 O que você encontra aqui?
* Mentoria Artística: Feedback humanizado e encorajador focado em composição, luz e enquadramento.

* Análise Técnica (EXIF): Leitura detalhada de ISO, Abertura, Velocidade do Obturador e Distância Focal.

* Receitas de Lightroom: Sugestões práticas de sliders (Exposição, Sombras, HSL) para levar sua edição ao próximo nível.

* Desafios Diários: Teste suas habilidades com temas novos todos os dias (Regra dos Terços, Linhas de Condução, Minimalism, etc.).

* Quadro de Medalhas: Acompanhe suas conquistas em um calendário visual integrado.

* Diário de Aprendizado: Um espaço persistente para anotar suas descobertas e insights sobre fotografia.


---
🚀 Como começar sua jornada
O projeto foi construído para rodar de forma simples e isolada. Siga os passos abaixo:

1. Pré-requisitos
* Uma chave de API do Google AI Studio (Gemini).
* Docker instalado no seu computador.

2. Configuração
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave:

```Plaintext
GOOGLE_API_KEY=sua_chave_aqui
```

3. Rodando o App
No terminal, dentro da pasta do projeto, execute:

```Bash
docker compose up --build
```

Após o carregamento, acesse http://localhost:8501 no seu navegador.

📂 Estrutura do Projeto
```Plaintext
.
├── app/
│   ├── app.py              # Interface visual e lógica do mentor
│   ├── utils.py            # Processamento de metadados EXIF
│   ├── journal.md          # Seu diário pessoal (gerado automaticamente)
│   └── challenges_history.json # Suas conquistas (gerado automaticamente)
├── Dockerfile              # Configuração do container
└── docker-compose.yml      # Orquestração do ambiente
```
✨ Design & Vibe
A interface foi personalizada para ser alegre e acolhedora, utilizando tons de pôr do sol (Golden Hour) para manter a inspiração sempre em alta.

* Fundo: Off-white suave para não cansar a vista.

* Botões: Laranja solar para destacar as ações criativas.

* Feedback: Organizado em Cards para facilitar a leitura.


## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Interface:** Streamlit
- **Cérebro:** Google Gemini AI (Modelo 1.5 Flash)
- **Infraestrutura:** Docker & Docker Compose

---

## ✨ Créditos & Inspiração

Este projeto foi desenvolvido com a ajuda do **Gemini (Google AI)**, que atuou como co-autor no desenvolvimento da lógica do mentor, design da interface e processamento de metadados. 

A jornada de aprendizado continua a cada clique! 📸

