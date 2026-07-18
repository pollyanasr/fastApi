# Books API

API REST de catálogo de livros construída com FastAPI. Os dados ficam em memória — não há banco de dados, então tudo o que for criado ou alterado se perde ao reiniciar o servidor.

## Requisitos

- Python 3.10 ou superior (o projeto usa a sintaxe `str | None`)
- Git

Confira sua versão:

```bash
python --version
```

## 1. Baixar o projeto

```bash
git clone https://github.com/<seu-usuario>/fastApi.git
cd fastApi
```

## 2. Criar o ambiente virtual

O ambiente virtual isola as dependências deste projeto das que você tem instaladas na máquina.

```bash
python -m venv .venv
```

Ative-o:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate
```

Você saberá que funcionou porque o prompt passa a exibir `(.venv)` no início.

> Se o PowerShell recusar a ativação com um erro de execução de scripts, rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Rodar o servidor

```bash
uvicorn books:app --reload
```

Lendo o comando: `books` é o arquivo `books.py`, `app` é a variável `app = FastAPI(...)` dentro dele, e `--reload` reinicia o servidor sozinho a cada alteração salva — use apenas em desenvolvimento.

A saída deve ser parecida com:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Para parar, pressione `Ctrl+C`.

## 5. Testar

Abra <http://127.0.0.1:8000/docs> no navegador. É a documentação interativa gerada automaticamente pelo FastAPI: dá para disparar qualquer requisição pelo botão **Try it out**, sem precisar de Postman ou curl.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/books` | Lista os livros, com filtros opcionais |
| `POST` | `/books` | Cria um livro |
| `GET` | `/books/{book_id}` | Busca um livro pelo id |
| `PUT` | `/books/{book_id}` | Atualiza um livro |
| `DELETE` | `/books/{book_id}` | Remove um livro |

### Filtros da listagem

`title`, `author` e `category` são todos opcionais e podem ser combinados livremente. A comparação ignora maiúsculas e minúsculas.

```
GET /books                                     todos os livros
GET /books?category=math                       só os de matemática
GET /books?author=Author Two                   só os de um autor
GET /books?author=Author Two&category=math     os dois filtros juntos
```

Quando nada corresponde, a resposta é uma lista vazia `[]` com status `200`.

### Criando um livro

O `id` é gerado pelo servidor — não envie esse campo, ele seria ignorado.

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert Martin", "category": "software"}'
```

Resposta (`201 Created`):

```json
{ "title": "Clean Code", "author": "Robert Martin", "category": "software", "id": 7 }
```

### Atualizando

O id vai na URL e o corpo traz os dados novos — inclusive um título diferente, se quiser renomear.

```bash
curl -X PUT http://127.0.0.1:8000/books/7 \
  -H "Content-Type: application/json" \
  -d '{"title": "Clean Architecture", "author": "Robert Martin", "category": "software"}'
```

### Removendo

```bash
curl -X DELETE http://127.0.0.1:8000/books/7
```

Retorna `204 No Content` — sucesso, sem corpo na resposta.

## Códigos de status

| Código | Quando acontece |
|---|---|
| `200` | Requisição bem-sucedida com retorno |
| `201` | Livro criado |
| `204` | Livro removido (sem corpo) |
| `404` | O id informado não existe |
| `422` | Dados inválidos: campo faltando, título vazio ou id não numérico |

## Estrutura

```
fastApi/
├── books.py          # toda a aplicação: modelos e rotas
├── requirements.txt
└── README.md
```

`books.py` define dois modelos Pydantic: `BookRequest` é o que o cliente envia (título, autor, categoria) e `Book` herda dele acrescentando o `id` gerado pelo servidor. Essa separação é o que impede o cliente de escolher o próprio id.
