# GitHub Copilot Instructions for Ecommerce Site

## Overview

This project is a Flask-based ecommerce site that allows users to register, log in, and manage products in a shopping cart. The application uses SQLAlchemy for database interactions and Flask-Mail for email notifications.

## Architecture

- **app.py**: The main entry point of the application. It initializes the Flask app, configures settings, and defines routes for user authentication and product management.
- **models.py**: Contains the database models, including `User`, `Product`, and `Order`. This file defines the structure of the database and relationships between entities.
- **templates/**: Contains HTML templates for rendering views. The `base.html` file serves as the layout for all pages, ensuring a consistent look and feel.
- **static/**: Holds static files such as CSS and JavaScript. The `style.css` file is used for styling the application.

## Developer Workflows

- **Running the Application**: Use the command `python app.py` to start the server. Ensure that the required environment variables are set for database and email configurations.
- **Testing**: Implement tests in a separate `tests/` directory (not included in the current structure). Use `pytest` for running tests.
- **Debugging**: Utilize Flask's built-in debugger by setting `app.debug = True` in `app.py` during development.

## Project Conventions

- **Naming Conventions**: Use snake_case for variable names and PascalCase for class names.
- **Database Migrations**: Use Flask-Migrate for handling database migrations. Run `flask db migrate` and `flask db upgrade` to apply changes.

## Integration Points

- **Database**: The application uses SQLite for local development. Ensure the database file is created in the `instance/` directory.
- **Email Notifications**: Configure SMTP settings in `app.py` for sending emails. Use environment variables for sensitive information like usernames and passwords.

## External Dependencies

- **Flask**: The core framework for building the web application.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-Login**: Manages user sessions and authentication.
- **Flask-Mail**: Handles email sending functionality.

## Examples

- **User Registration**: The registration form is handled in the `/register` route, where user data is validated and stored in the database.
- **Product Management**: Admin users can manage products through specific routes (not detailed in the current structure).

## Conclusion

This document provides a foundational understanding of the ecommerce site structure and workflows. For further details, refer to the specific files mentioned above.
