# Sistema de Tarefas

Este é um sistema de gerenciamento de tarefas desenvolvido com HTML, CSS, JavaScript e Flask no backend. O projeto permite criar, visualizar, editar, excluir e concluir tarefas, além de adicionar comentários.

## 🧰 Tecnologias utilizadas

- HTML, CSS, JavaScript (Frontend)
- Python com Flask (Backend)
- SQLite (padrão) ou MySQL (opcional)
- Flask-CORS (para requisições entre frontend e backend)

## 📦 Instalação

### 1. Clone o repositório (ou descompacte o .zip)
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### 2. Acesse a pasta do projeto
```bash
cd nome-da-pasta
```

### 3. Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

## 🗄️ Banco de Dados

Por padrão, o sistema usa **SQLite** e cria o banco de dados automaticamente na primeira execução.

Se quiser usar **MySQL**, configure o arquivo `config.py` com suas credenciais e adapte o `app.py` para usar `mysql.connector`.

## ▶️ Executando a aplicação

```bash
python app.py
```

Acesse o sistema no navegador:

```
http://localhost:5000
```

## ✨ Funcionalidades

- Criar, listar, editar, excluir e concluir tarefas
- Adicionar comentários às tarefas
- Interface simples e responsiva

---

## 📁 Estrutura do projeto

```
/static/
    /css/
    /js/
    /img/ (opcional)

/templates/
    index.html
    detalhes.html

app.py
config.py (opcional para MySQL)
requirements.txt
README.md
```

---

Desenvolvido por Hector Scocha
