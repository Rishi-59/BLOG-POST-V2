# RESTful Blog Website

A Flask blog application built for Day 67 of the 100 Days of Code Python course. The app uses SQLite and SQLAlchemy for persistent blog posts, Flask-WTF forms for validation, CKEditor for rich text editing, and Bootstrap styling through Bootstrap-Flask.

## Features

- View all blog posts on the home page
- Open individual post detail pages
- Create new blog posts with title, subtitle, author, image URL, and rich text content
- Edit existing posts
- Delete posts
- Static About and Contact pages
- SQLite database created automatically on first run

## Tech Stack

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-WTF / WTForms
- Flask-CKEditor
- Bootstrap-Flask
- SQLite

## Project Structure

```text
.
├── main.py              # Flask application, routes, forms, and database model
├── requirements.txt     # pip dependencies
├── pyproject.toml       # project metadata and dependency list
├── templates/           # Jinja templates
├── static/              # CSS, JavaScript, favicon, and images
└── instance/posts.db    # SQLite database, generated locally
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python main.py
```

The development server runs at:

```text
http://127.0.0.1:5003
```

## Routes

| Route | Methods | Description |
| --- | --- | --- |
| `/` | GET | Show all blog posts |
| `/post/<post_id>` | GET | Show one blog post |
| `/post/new` | GET, POST | Create a new post |
| `/post/<post_id>/edit` | GET, POST | Edit an existing post |
| `/post/<post_id>/delete` | GET, POST | Delete a post |
| `/about` | GET | Show the About page |
| `/contact` | GET | Show the Contact page |

## Notes

- The app creates the database tables automatically with `db.create_all()`.
- Blog post data is stored in `instance/posts.db`.
- The Flask `SECRET_KEY` is currently hard-coded for local development. Use an environment variable before deploying this app.
