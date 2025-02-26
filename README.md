# EventAdmin

A Django application for managing events and user participation.

## Features

- User registration and authentication
- Event creation and management
- User participation in events
- RESTful API for event management

## Setup

### Prerequisites
- Python 3.8+
- Django 5.0+

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd eventadmin
```

2. Create and activate virtual environment
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## Environment Variables

The application uses the following environment variables:

- `DJANGO_SECRET_KEY`: Secret key for Django
- `DJANGO_DEBUG`: Set to 'True' for development, 'False' for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain authentication token

### Events
- `GET /api/users/events/<username>/`: Get all events for a user
- `GET /api/events/<event_id>/`: Get event details
- `POST /api/events/`: Create a new event
- `PUT /api/events/<event_id>/`: Update an event
- `DELETE /api/events/<event_id>/`: Delete an event
- `GET /api/events/<event_id>/participants/`: Get all participants for an event

### Users
- `GET /api/events/users/<event_id>/`: Get all users for an event

## Testing

Run tests with:
```bash
python manage.py test
```

## Docker

You can also run the application with Docker:

```bash
docker-compose up
```