# PhotoFlow

PhotoFlow is a Django-based photography studio booking system. It allows clients to browse studios, services, and photographers, then create and manage photo-session bookings.

## Features

* User registration, login, and logout
* Two user roles: client and photographer
* Studio catalogue with detail pages
* Photographer catalogue with detail pages
* Service catalogue
* Search for studios, services, and photographers
* Pagination for catalogue pages
* Photo-session booking
* Booking validation:

  * bookings cannot be created for past dates
  * the number of people cannot exceed studio capacity
  * studio and photographer time conflicts are prevented
* Role-based booking lists:

  * clients see bookings they created
  * photographers see sessions assigned to them
* Django admin panel
* Responsive Bootstrap interface
* Separate CSS files for individual pages


## Data Models

### User

The project uses a custom user model based on Django's `AbstractUser`.

Available roles:

* `client`
* `photographer`

Users registered through the public signup page are created with the `client` role.

### StudioRoom

Stores information about a photography studio:

* name
* description
* price per hour
* capacity
* image

### Service

Stores information about a photography service:

* name
* description
* price
* duration

### Booking

Connects a client, photographer, studio, and service.

A booking contains:

* client
* photographer
* studio room
* service
* date
* start time
* duration
* number of people
* status
* comment

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lemonch1ks/PhotoFlow.git
cd PhotoFlow
```

To work with the development branch:

```bash
git checkout develop
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an administrator

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

The admin panel is available at:

```text
http://127.0.0.1:8000/admin/
```

## Main Routes

| Route                  | Description             |
| ---------------------- | ----------------------- |
| `/`                    | Home page               |
| `/sign-up/`            | User registration       |
| `/accounts/login/`     | Login                   |
| `/accounts/logout/`    | Logout                  |
| `/studios/list/`       | Studio list             |
| `/studios/<id>/`       | Studio details          |
| `/studios/<id>/book/`  | Create a booking        |
| `/service_list/`       | Service list            |
| `/photographers/`      | Photographer list       |
| `/photographers/<id>/` | Photographer details    |
| `/bookings/`           | Current user's bookings |
| `/admin/`              | Django admin panel      |

## Authentication

Login and logout are provided by Django's built-in authentication views.

The project includes custom templates:

```text
templates/registration/login.html
templates/registration/logged_out.html
templates/registration/sign_up.html
```

After successful signup, the new user is automatically logged in and redirected to the home page.

## Booking Workflow

1. A client signs up or logs in.
2. The client opens the studio catalogue.
3. The client selects a studio.
4. The client chooses a photographer and service.
5. The client selects the date, start time, and number of people.
6. The form validates the booking data and checks for scheduling conflicts.
7. A booking is created with the `Pending` status.
8. The client can view the booking on the **My bookings** page.
9. The selected photographer can view the session in their booking list.

Only users with the `client` role can create bookings.

## Search and Pagination

Search is implemented with the `q` query parameter:

```text
/studios/list/?q=studio
/service_list/?q=portrait
/photographers/?q=alex
```

Catalogue pages display six items per page.

Pagination preserves the active search query.

## Running Tests

Run all Django tests:

```bash
python manage.py test
```

Run tests with pytest:

```bash
pytest
```

Run only view tests:

```bash
pytest flow/tests/tests_views.py
```

## Code Quality

Check the Django configuration:

```bash
python manage.py check
```

Run Flake8:

```bash
flake8
```

## Static and Media Files

Static files are stored in:

```text
static/
```

Uploaded images are stored in:

```text
media/
```

During local development, Django serves media files when `DEBUG=True`.

## Development Notes

* Application views use Django class-based views.
* List pages use `ListView`.
* Detail pages use `DetailView`.
* Registration uses `FormView`.
* Booking creation uses `CreateView`.
* Protected pages use `LoginRequiredMixin`.
* Booking permissions use `UserPassesTestMixin`.

