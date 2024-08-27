# ContractsManager

Contracts Manager é uma aplicação Django para gerenciamento de Contratos.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/matheuskdev/contracts_manager.git .
   ```

2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   # Ou para Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Execute as migrações do banco de dados:

   ```bash
   python manage.py makemigrations
   ```
   ```bash
   python manage.py migrate
   ```

4. Crie um superusuário para acessar o painel de administração:

   ```bash
   python manage.py createsuperuser
   ```
   ou utilize o arquivo de criação create_superuser.py
   ```bash
   python create_superuser.py
   ```

5. Crie os departamentos iniciais e associe com o usuário principal:

   ```bash
   python manage.py populate
   ```

6. Realize os testes para verificar o correto funcionamento do sistema:

   ```bash
   python manage.py test
   ```

7. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

A aplicação estará disponível em http://127.0.0.1:8000/.

## Uso

- Acesse o painel de administração em http://127.0.0.1:8000/admin/ para gerenciar usuários, contratos e outras configurações.

- Os departamentos fazem parte da regra de negócio principal então seu gerenciamento só é possóvel através do painel de administração.

## Contribuindo

Se quiser contribuir, por favor, siga estas etapas:

1. Faça o fork do repositório.
2. Use o padrão de lint com o comando (
    ```bash
   python manage.py run_code_checks
   ```
   )
3. Crie um branch para a sua feature (`git checkout -b feature/sua-feature`).
4. Commit suas mudanças (`git commit -m 'Adiciona alguma funcionalidade'`).
5. Push para o branch (`git push origin feature/sua-feature`).
6. Abra um Pull Request.
