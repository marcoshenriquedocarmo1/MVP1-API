# meu_app_api

Este pequeno projeto faz parte do material didático da disciplina **Desenvolvimento Full Stack Básico**.

O objetivo aqui é ilustrar o conteúdo apresentado ao longo das três aulas da disciplina, com foco na construção de uma API REST utilizando Flask e SQLAlchemy.

---

## Como executar

Será necessário ter todas as bibliotecas Python listadas no arquivo `requirements.txt` instaladas. Após clonar o repositório, acesse o diretório raiz pelo terminal para executar os comandos abaixo.

É fortemente recomendado o uso de ambientes virtuais, como o `virtualenv`.

```bash
(env)$ pip install -r requirements.txt
```

### Executando a API

Para iniciar a API, utilize o comando:

```bash
(env)$ flask run --host 0.0.0.0 --port 5000
```

Durante o desenvolvimento, é recomendado utilizar o parâmetro --reload, que reinicia o servidor automaticamente ao detectar alterações no código fonte:

```bash
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

### Acessando a API
Abra o navegador e acesse:
```bash
http://localhost:5000/#/
```
Você verá a interface de documentação da API em execução, com os endpoints disponíveis para teste.