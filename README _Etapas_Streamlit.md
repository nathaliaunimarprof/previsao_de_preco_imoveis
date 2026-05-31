# Deploy do Aplicativo Streamlit

Este documento apresenta o passo a passo para publicar o aplicativo desenvolvido em Streamlit utilizando o **Streamlit Community Cloud** e um repositório do GitHub.

## Pré-requisitos

Antes de iniciar o deploy, verifique se você possui:

- Uma conta no GitHub.
- O projeto salvo em um repositório público no GitHub.
- O arquivo principal da aplicação Streamlit, por exemplo: `app.py`.
- O arquivo `requirements.txt` com as bibliotecas necessárias para executar o projeto.

## Passo a passo para publicar o app no Streamlit

### 1. Acessar o site do Streamlit

Acesse:

```text
https://streamlit.io/
```

Na parte superior do site, localize a seção:

```text
Deploying? Try:
```

Em seguida, na opção **Free**, selecione a opção para realizar login com o **GitHub**.

---

### 2. Fazer login com o GitHub

Siga os passos solicitados pela plataforma e autorize o login da sua conta do GitHub com o Streamlit.

Após a autorização, finalize o cadastro da sua conta no Streamlit, preenchendo as informações necessárias.

---

### 3. Acessar o Streamlit Community Cloud

Depois de concluir o cadastro, acesse:

```text
https://share.streamlit.io/
```

---

### 4. Criar um novo aplicativo

Na página inicial do Streamlit Community Cloud, clique em:

```text
Create app
```

Em seguida, selecione:

```text
Deploy a public app from GitHub
```

---

### 5. Configurar o deploy do aplicativo

Na página **Deploy an app**, configure as informações do projeto:

- **Repository:** selecione o repositório do GitHub onde está o aplicativo.
- **Branch:** selecione a branch principal do projeto, geralmente `main` ou `master`.
- **Main file path:** selecione o arquivo principal do aplicativo, por exemplo:

```text
app.py
```

Caso o arquivo esteja dentro de uma pasta, informe o caminho completo.

Exemplo:

```text
smartcar-fipe/app.py
```

---

### 6. Finalizar a publicação

Após preencher as informações necessárias, clique em:

```text
Deploy
```

O Streamlit irá instalar as dependências do projeto e publicar o aplicativo.

Ao final do processo, será gerado um link público para acessar o app.

## Observação importante

Caso o deploy apresente erro, verifique principalmente:

- Se o arquivo `requirements.txt` existe no repositório.
- Se todas as bibliotecas usadas no projeto estão listadas no `requirements.txt`.
- Se o caminho informado em **Main file path** está correto.
- Se o arquivo principal realmente contém a aplicação Streamlit.
- Se o repositório está público.

## Exemplo de estrutura mínima do projeto

```text
nome-do-projeto/
│
├── app.py
├── requirements.txt
└── README.md
```

## Comando para executar localmente

Antes de publicar, é recomendável testar o aplicativo localmente com:

```bash
streamlit run app.py
```

Se o aplicativo abrir corretamente no navegador, ele estará mais preparado para ser publicado no Streamlit Community Cloud.
