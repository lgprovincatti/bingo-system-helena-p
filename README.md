# Bingo Helena Provinciatti
Sistema de Bingo Web desenvolvido em Python com FastAPI.
Projeto criado para uso local/doméstico, permitindo sorteio em tempo real, acesso via celular na rede local e geração automática de cartelas PDF.
Desenvolvido por Lucas Gorla Provinciatti

---
# Funcionalidades
## Bingo
- Sorteio manual
- Sorteio automático
- Pausar sorteio
- Reiniciar bingo
- Histórico completo dos números
- Destaque animado do último número sorteado
- Grid visual de 1 a 75
- Não repete números

## Cartelas
- Geração automática de cartelas
- Cartelas únicas (sem duplicação)
- Modelo Bingo Americano (1–75)
- Cartelas 5x5
- PDF A4
- 4 cartelas por página
- Geração automática de 40 cartelas

## Interface
- Layout moderno
- Fullscreen
- Responsivo para celular
- Atualização em tempo real com WebSocket
- Funciona na rede local

# Tecnologias
- Python
- FastAPI
- WebSocket
- Jinja2
- ReportLab
- HTML5
- CSS3
- JavaScript

# Instalação
## 1. Clonar repositório
---
## 2. Entrar na pasta
cd bingo-system-helena-provinciatti
---
## 3. Criar ambiente virtual
### Windows
python -m venv venv
---
## 4. Ativar ambiente virtual
### PowerShell
.\venv\Scripts\Activate.ps1
---
## 5. Instalar dependências
pip install -r requirements.txt
---
# Executar Projeto
## Desenvolvimento
uvicorn app.main:app --reload
---
## Execução Completa
python launcher.py

O sistema abrirá automaticamente no navegador.
---
# Acesso pelo Celular
Após iniciar:
http://SEU_IP_LOCAL:8000
Exemplo: http://192.168.0.15:8000

O celular deve estar na mesma rede Wi-Fi.
---

# Gerar Executável (.EXE)
pyinstaller --onefile `
--noconsole `
--collect-all fastapi `
--collect-all uvicorn `
--collect-all starlette `
--collect-all anyio `
--collect-all websockets `
--add-data "app/templates;app/templates" `
--add-data "app/static;app/static" `
launcher.py


O executável será criado em: dist/
---

# Estrutura do Projeto
```txt
app/
│
├── core/
├── routes/
├── services/
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
└── main.py

launcher.py
requirements.txt
README.md
```

---
# Requisitos
- Python 3.11+
- Windows 10/11
---
# Licença
Projeto para uso pessoal/doméstico.