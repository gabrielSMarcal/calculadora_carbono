# Instruções para o Professor Avaliador

1. **Criar e Ativar o Ambiente Virtual:**
    - Abra o terminal e navegue até o diretório do projeto.
    - Execute o comando abaixo para criar o ambiente virtual:
      ```
      python -m venv venv
      ```
    - Em seguida, ative o ambiente virtual:
      ```
      source venv/bin/activate   # Para sistemas Unix
      .\venv\Scripts\activate    # Para Windows
      ```

2. **Instalar os Requirements:**
    - Com o ambiente virtual ativado, instale as dependências do projeto executando:
      ```
      pip install -r requirements.txt
      ```

3. **Executar o Site:**
    - Ainda com o ambiente virtual ativado, inicie o servidor do site com o comando:
      ```
      python manage.py runserver
      ```
    - Acesse o site no navegador através do endereço:
      ```
      http://127.0.0.1:8000/
      ```

