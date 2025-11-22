# Secret Santa Generator

Secret Santa Generator is a Django-based web application designed to help users easily organize and manage Secret Santa gift exchanges. With this tool, users can create groups, randomly assign gift givers and receivers, and share the details of their exchange in a secure and seamless way. This project streamlines the Secret Santa process by automating the matching and ensuring a smooth experience for everyone involved.

---

## Table of Contents

1. [About This Repository](#about-this-repository)
2. [How to Use](#how-to-use)
    - [Cloning the Repository](#cloning-the-repository)
    - [Recreate the Repository](#recreate-the-repository)
3. [Contributing](#contributing)
4. [License](#license)

---

## About This Repository

This repository is a clone of my general django project setup code: [Original Repository](https://github.com/josuehernandezz/general_django_project.git). I have created this new repository to:

- **Customize the code** for my specific use case.
- **Track personal changes**.
- **Use the existing code as a foundation** for a new project.

This project does **not** directly edit the original repository. Any changes made here are independent and do not affect the original codebase.

---

## How to Use

### Django Project Setup

1. **Create python virtual environment:**

    ```bash
    python3 -m venv venv

2. **Activate virtual environment:**

    ```bash
    source venv/bin/activate

3. **Install dependencies for python:**

   ```bash
    pip install -r requirements.txt

4. **Navigate into the node directory:**

   ```bash
   cd node

5. **Install dependencies for node (if applicable):**

   ```bash
    npm install

6. **Create environment variables file:**

    ```bash
    cd ..
    touch .env
    ```

7. **Generate a secure SECRET_KEY and add it to .env file:**

    ```bash
    echo "SECRET_KEY = '$(openssl rand -base64 64 | tr -d '\n')'" > .env

8. **Add DEBUG setting to True for development:**

    ```bash
    echo "DEBUG = 'True'" >> .env

9. **Navigate into the django directory:**

    ```bash
   cd ../django

10. **Start the development server:**

   ```bash
    python manage.py runserver

11. **Restore from old database**

   ```bash
   docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < ~/uci-server-backup/server-backup/secret_santa_backup.sql
