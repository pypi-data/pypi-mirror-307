
# Login Canaimé

Este projeto fornece um sistema de login automatizado para o sistema Canaimé, permitindo a autenticação por meio de uma interface gráfica (GUI) ou um login direto com JavaScript e imagens desativadas para eficiência. A biblioteca usa `playwright` para automação do navegador, permitindo fácil navegação após o login.

## Funcionalidades

- **Interface Gráfica (GUI)** para login, onde o usuário pode inserir suas credenciais manualmente.
- **Login Automatizado** sem interface gráfica, com JavaScript e imagens desativadas.
- **Controle de Navegação**: Capacidade de navegar entre páginas com `playwright` após o login.
- **Opção de Teste**: Quando `test=True`, o navegador é aberto em modo visível (não headless) e as credenciais são exibidas no console.

## Requisitos

 - **Python 3.7+**
  - **Playwright**: Para instalar o Playwright e o navegador Chromium, execute o seguinte comando:

  ```bash
  pip install playwright
  playwright install
  ```

## Instalação

Clone este repositório e instale as dependências:

```bash
git clone https://github.com/username/login-canaime.git
cd login-canaime
pip install -r requirements.txt
```

> **Nota**: Certifique-se de instalar o Chromium com `playwright install` se ele ainda não estiver instalado.

## Uso

### Login com Interface Gráfica (GUI)

O login com GUI permite que você insira manualmente o usuário e senha:

```
from login_canaime import run_canaime_login

username, password = run_canaime_login(test_mode=True)
print(f"Credenciais: {username}, {password}")
```

### Login Automatizado sem Interface Gráfica

Para realizar o login diretamente, desativando JavaScript e imagens, use a função `Login()`:

```
from login_canaime import Login

page = Login(test=False)  # Defina test=True para abrir em modo visível

page.goto("https://www.google.com.br")

# Feche o navegador e o Playwright ao terminar
browser.close()
playwright.stop()
```

### Função `Login` Detalhada

A função `Login(test=False)` usa as credenciais da GUI e realiza o login automaticamente com JavaScript e imagens desativadas, retornando o navegador (`browser`) e a página (`page`) para operações adicionais.

-   **Parâmetros**:
    
    -   `test` (bool): Se `True`, abre o navegador em modo visível. Se `False`, abre em modo headless (oculto).
        
-   **Retorno**:
    
    -   `page`: Página logada, pronta para navegação.        
    -   `browser`: Instância do navegador, que deve ser fechada manualmente.        
    -   `playwright`: Contexto do Playwright, que deve ser encerrado ao final.
        

## Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo `LICENSE` para mais detalhes.
