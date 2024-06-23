## Overview

The Contact Identifier is a Django-based web service designed to manage and link customer contact information. It provides an endpoint `/identify` that receives HTTP POST requests with JSON data containing either an email or phone number, and returns a consolidated contact information response. The service handles linking contacts, including scenarios where primary contacts can turn into secondary contacts.

## Features

- Identify and link customer contacts based on email and phone number.
- Consolidate contact information with primary and secondary precedence.
- Automatically updates the precedence of contacts when necessary.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ankitshaw09/Bitespeed_django.git
   cd Bitespeed_django
   ```

2. **Create a virtual environment** and activate it:

   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

6. **Create a superuser** (optional, for accessing the Django admin interface):

   ```bash
   python manage.py createsuperuser
   ```

## Usage

The main endpoint of this service is `/contacts/identify/`. Here’s how to use it:

### Endpoint: `/contacts/identify/`

**Method**: POST

**Request Body**: JSON

```json
{
  "email": "mcfly@hillvalley.edu",
  "phoneNumber": "123456"
}
```

**Response**: JSON

```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
    "phoneNumbers": ["123456"],
    "secondaryContactIds": [23]
  }
}
```

### Example Request with `curl`

```bash
curl -X POST http://127.0.0.1:8000/contacts/identify/ \
     -H "Content-Type: application/json" \
     -d '{"phoneNumber": "123456", "email": "mcfly@hillvalley.edu"}'
```

## Project Structure

```
contact-identifier/
├── bitespeed/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── contacts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
```
