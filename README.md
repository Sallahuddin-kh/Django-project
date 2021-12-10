# Django-project
Ecommerce Django project.
## Setup Instructions
### Prerequesites
Following utilities should be installed in the system in order to run the application:
- Docker
- Postgres

### Setting Up the container
To set up the containers run the giving commands in command prompt opened in the project folder:
- `docker-compose up --build`
- `docker-compose exec ecommerceproj python manage.py createsuperuser` in another command prompt while the containers are running to make superusers for admin app.
- Search `http://localhost:8000` in the browser for the app and `http://localhost:8000/admin` for the admin site.


That's all. Stay Safe :sunglasses: