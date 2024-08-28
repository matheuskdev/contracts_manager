# ContractsManager

ContractsManager é uma aplicação Django para gerenciamento eficiente de contratos.

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
   python manage.py migrate
   ```

4. Crie um superusuário para acessar o painel de administração:

   ```bash
   python manage.py createsuperuser
   ```
   ou utilize o script `create_superuser.py`:
   ```bash
   python create_superuser.py
   ```

5. Popule o banco de dados com os departamentos iniciais e associe-os ao superusuário:

   ```bash
   python manage.py populate
   ```

6. Execute os testes para garantir que tudo está funcionando corretamente:

   ```bash
   python manage.py test
   ```

7. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

   A aplicação estará disponível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Uso

- Acesse o painel de administração em [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) para gerenciar usuários, contratos e configurações.

- O gerenciamento de departamentos, essencial para a regra de negócio, está disponível exclusivamente no painel de administração.

## Contribuindo

Para contribuir com o projeto, siga os passos abaixo:

1. Faça um fork do repositório.
2. Utilize o comando abaixo para garantir que seu código segue os padrões de lint:
   ```bash
   python manage.py run_code_checks
   ```
3. Crie um branch para sua feature (`git checkout -b feature/nome-da-feature`).
4. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
5. Envie o branch para o repositório remoto (`git push origin feature/nome-da-feature`).
6. Abra um Pull Request.

---

Obrigado por contribuir para o ContractsManager!
