# Simple Social

A simple REST API based social network in Django where Users can sign up and create text posts, as well as view, like,
and unlike other Users’ posts.

### Requirements

[Docker](https://docs.docker.com/install/)

### Set Up Project

```shell
docker-compose up --build
```

### Run the tests

```shell
docker-compose exec web pytest
```

### API description

#### /api/auth/

Auth endpoints for users to register, login, logout, change details, refresh and validate tokens.

#### /api/posts/

CRUD for Posts

#### /api/posts/{post_id}/reactions/

CRUD for reacting (like and dislike) to posts

---

refer to /docs/ enpoint for more details

---

### Environment Variables

For validating the format of user's email address, fetching their geolocation data and identifying if they registered
on a local holiday, [Abstract API](https://www.abstractapi.com/) was used. For these tasks to work, the following keys
are required:

* EMAIL_VALIDATION_API_KEY
* IP_GEOLOCATION_API_KEY
* HOLIDAYS_API_KEY

### Improvements

* Use flake8, black and isort to better format. stylize and organize code.
* Add intergartion tests
