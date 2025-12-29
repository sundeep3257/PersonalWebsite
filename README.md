# Personal Portfolio Website

A production-quality Flask portfolio website with a dark, creative theme featuring automated content management through an admin dashboard.

## Features

- **Dark Theme Design**: Modern dark UI with custom color palette
- **Responsive Layout**: Mobile-friendly design with smooth animations
- **Content Management**: Admin dashboard for managing projects, publications, and experiences
- **Interactive Elements**: 
  - Project carousels with navigation
  - Scroll-snap publication viewer (vinyl record style)
  - Flip cards for experiences
- **Database-Driven**: SQLite database with SQLAlchemy ORM
- **Auto-Seeding**: Automatically populates with example content on first run

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite + SQLAlchemy
- **Templating**: Jinja2
- **Styling**: Plain CSS (no frameworks)
- **JavaScript**: Vanilla JS only

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Installation

1. Clone or navigate to the project directory:
```bash
cd PersonalWebsite
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

The database will be automatically created and seeded with example data on first run.

## Admin Access

### Login

1. Navigate to the **About** page (`/about`)
2. Click on the letter **"p"** in "Sundeep" (it's a hidden link)
3. Enter the password: `sundeepchakladar2003`

Alternatively, go directly to: `http://localhost:5000/admin/login`

### Admin Dashboard

Once logged in, you can:
- **Manage Projects**: Add, edit, or delete projects with image uploads
- **Manage Publications**: Add, edit, or delete publications
- **Manage Experiences**: Add, edit, or delete experiences

### Admin Features

- **Projects**: 
  - Support for two categories: Medicine and Creative
  - Preview images and gallery images
  - Auto-generated URL slugs
  - Rich text intro sections

- **Publications**:
  - Title, journal, date, authors, and external URL
  - Displayed in scroll-snap viewer on homepage

- **Experiences**:
  - Title and description
  - Displayed as flip cards on homepage

## Database Management

### Reseed Database

To clear and reseed the database with example content:

1. Delete the `portfolio.db` file (if it exists)
2. Restart the Flask application
3. The database will be automatically recreated and seeded

Or manually run the seed script:
```python
from app import app
from models import db
from seed import seed_database

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_database()
```

### Database Location

The SQLite database file (`portfolio.db`) is created in the project root directory.

## File Structure

```
PersonalWebsite/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── seed.py                # Database seeding script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── portfolio.db          # SQLite database (created on first run)
├── graphics/             # Static images and assets
│   ├── Favicon - Personal Website.png
│   ├── Hero Image - Personal Website.png
│   ├── LinkedIn Logo.png
│   ├── Intragram Logo.png
│   ├── ResearchGate Logo.png
│   ├── test_image.png
│   └── my_cv.pdf
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   ├── carousels.js  # Project carousel functionality
│   │   ├── publications.js # Publication scroll-snap viewer
│   │   └── flip-cards.js # Experience flip card animations
│   └── uploads/           # User-uploaded images (created automatically)
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage
    ├── about.html         # About page
    ├── projects_archive.html # All projects page
    ├── project_detail.html  # Individual project page
    └── admin/
        ├── login.html     # Admin login
        ├── dashboard.html # Admin dashboard
        ├── projects/      # Project management templates
        ├── publications/  # Publication management templates
        └── experiences/   # Experience management templates
```

## Color Palette

- **Dark Base**: `#15141f` (primary background)
- **Secondary Dark**: `#4f4254` (panels, gradients, borders)
- **Text**: `#ffffff` (white)
- **Accent**: `#d69b8d` (primary accent)
- **Accent 2**: `#eee3a8` (secondary accent)

## Typography

- **Headers**: Libre Baskerville (bold) - Google Fonts
- **Code/UI Text**: Courier New (monospace)
- **Body**: System fonts (San Francisco, Segoe UI, etc.)

## Routes

### Public Routes
- `/` - Homepage
- `/projects` - Projects archive
- `/project/<slug>` - Individual project detail
- `/about` - About page
- `/download-cv` - Download CV PDF

### Admin Routes
- `/admin/login` - Admin login
- `/admin` - Admin dashboard
- `/admin/logout` - Logout
- `/admin/projects` - Manage projects
- `/admin/projects/new` - Create project
- `/admin/projects/<id>/edit` - Edit project
- `/admin/publications` - Manage publications
- `/admin/publications/new` - Create publication
- `/admin/publications/<id>/edit` - Edit publication
- `/admin/experiences` - Manage experiences
- `/admin/experiences/new` - Create experience
- `/admin/experiences/<id>/edit` - Edit experience

## Development Notes

- The application uses Flask's development server by default. For production, use a proper WSGI server like Gunicorn or uWSGI.
- Uploaded images are stored in `static/uploads/` and paths are saved in the database.
- The admin password is currently hardcoded. For production, consider using environment variables and proper password hashing.
- The database auto-seeds on first run if empty.

## Troubleshooting

### Database Issues
- If you encounter database errors, delete `portfolio.db` and restart the app
- Ensure you have write permissions in the project directory

### Image Upload Issues
- Ensure the `static/uploads/` directory exists and is writable
- Check file size limits (default: 16MB)
- Supported formats: PNG, JPG, JPEG, GIF

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

## License

Personal project - All rights reserved.

## Contact

Sundeep Chakladar
- LinkedIn: [sundeep-chakladar-37b467252](https://www.linkedin.com/in/sundeep-chakladar-37b467252/)
- Instagram: [@sundeepchakladar](https://www.instagram.com/sundeepchakladar/?hl=en)
- ResearchGate: [Sundeep Chakladar](https://www.researchgate.net/profile/Sundeep-Chakladar)

