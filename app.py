from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models import db, Project, ProjectImage, Publication, Experience, ProjectCategory, AboutPage, CV
from config import Config
import os
import re
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_slug(title):
    """Generate a URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:200]

def is_admin():
    """Check if user is logged in as admin"""
    return session.get('admin_logged_in', False)

@app.template_filter('asset_url')
def asset_url_filter(path):
    """Template filter to handle both graphics and static paths"""
    if path.startswith('graphics/'):
        filename = path.replace('graphics/', '')
        return url_for('serve_graphics', filename=filename)
    else:
        return url_for('static', filename=path)

def require_admin(f):
    """Decorator to require admin login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Homepage with all sections"""
    # Ensure database is initialized
    try:
        db.create_all()
        if Project.query.count() == 0:
            from seed import seed_database
            seed_database()
    except:
        pass  # Database might already exist
    
    projects_medicine = Project.query.filter_by(category=ProjectCategory.MEDICINE).all()
    projects_creative = Project.query.filter_by(category=ProjectCategory.CREATIVE).all()
    publications = Publication.query.order_by(Publication.publication_date.desc()).all()
    experiences = Experience.query.all()
    
    return render_template('index.html',
                         projects_medicine=projects_medicine,
                         projects_creative=projects_creative,
                         publications=publications,
                         experiences=experiences)

@app.route('/projects')
def projects_archive():
    """Archive page showing all projects in a grid"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects_archive.html', projects=projects)

@app.route('/project/<slug>')
def project_detail(slug):
    """Individual project detail page"""
    project = Project.query.filter_by(slug=slug).first_or_404()
    images = ProjectImage.query.filter_by(project_id=project.id).order_by(ProjectImage.display_order).all()
    
    # Get all projects ordered by creation date (same order as archive)
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    
    # Find current project index and get next project
    next_project = None
    try:
        current_index = next(i for i, p in enumerate(all_projects) if p.id == project.id)
        # Get next project (loop to first if at end)
        next_index = (current_index + 1) % len(all_projects)
        next_project = all_projects[next_index]
    except (StopIteration, IndexError):
        # Fallback if something goes wrong
        if len(all_projects) > 1:
            next_project = all_projects[0] if all_projects[0].id != project.id else (all_projects[1] if len(all_projects) > 1 else None)
    
    return render_template('project_detail.html', project=project, images=images, next_project=next_project)

@app.route('/about')
def about():
    """About page"""
    about_page = AboutPage.query.first()
    # If no about page exists, use default content
    if not about_page:
        default_content = """I am a medical student with a deep passion for leveraging technology to solve complex problems in healthcare. 
My journey combines rigorous medical training with expertise in machine learning, computer vision, and full-stack 
web development.

Through my research and projects, I've developed automated systems for medical image analysis, built predictive 
models for patient outcomes, and created web applications that make healthcare data more accessible. I believe in 
the power of interdisciplinary collaboration to drive innovation in medicine.

When I'm not studying or coding, I enjoy exploring new technologies, contributing to open-source projects, and 
sharing knowledge with the medical and tech communities. My goal is to bridge the gap between clinical practice 
and cutting-edge technology to improve patient care."""
        about_page = AboutPage(content=default_content)
        db.session.add(about_page)
        db.session.commit()
    
    # Split content by double newlines to create paragraphs, and handle single newlines within paragraphs
    # First, normalize different newline formats
    content = about_page.content.replace('\r\n', '\n').replace('\r', '\n')
    # Split by double newlines for paragraphs
    paragraphs = []
    for para in content.split('\n\n'):
        para = para.strip()
        if para:
            # Replace single newlines within paragraphs with <br> tags
            para = para.replace('\n', '<br>')
            paragraphs.append(para)
    
    return render_template('about.html', paragraphs=paragraphs)

@app.route('/download-cv')
def download_cv():
    """Download CV file"""
    cv = CV.query.first()
    if cv:
        # Handle both graphics/ and uploads/ paths
        if cv.file_path.startswith('graphics/'):
            # Graphics folder is at root level
            file_path = cv.file_path
        elif cv.file_path.startswith('uploads/'):
            # Uploads are in static/uploads
            file_path = os.path.join('static', cv.file_path)
        else:
            # Assume it's a relative path from root
            file_path = cv.file_path
        
        # Check if file exists and send it
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=cv.download_name)
    
    # Fallback to default if no CV in database or file not found
    default_path = 'graphics/my_cv.pdf'
    if os.path.exists(default_path):
        return send_file(default_path, as_attachment=True, download_name='CV_Sundeep_Chakladar.pdf')
    else:
        # If default also doesn't exist, return 404
        from flask import abort
        abort(404)

@app.route('/graphics/<path:filename>')
def serve_graphics(filename):
    """Serve graphics files"""
    return send_from_directory('graphics', filename)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        # Check against hardcoded password (in production, use hashed version)
        if password == 'sundeepchakladar2003':
            session['admin_logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@require_admin
def admin_dashboard():
    """Admin dashboard"""
    project_count = Project.query.count()
    publication_count = Publication.query.count()
    experience_count = Experience.query.count()
    
    return render_template('admin/dashboard.html',
                         project_count=project_count,
                         publication_count=publication_count,
                         experience_count=experience_count)

# ==================== ADMIN: PROJECTS ====================

@app.route('/admin/projects')
@require_admin
def admin_projects():
    """List all projects"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects/list.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@require_admin
def admin_project_new():
    """Create new project"""
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        preview_summary = request.form.get('preview_summary')
        page_intro_text = request.form.get('page_intro_text', '')
        
        # Generate slug
        slug = generate_slug(title)
        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while Project.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Handle preview image upload
        preview_image_path = 'graphics/test_image.png'  # Default
        if 'preview_image' in request.files:
            file = request.files['preview_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{slug}-preview-{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                preview_image_path = f"uploads/{filename}"
        
        project = Project(
            title=title,
            slug=slug,
            category=ProjectCategory[category.upper()],
            preview_summary=preview_summary,
            preview_image_path=preview_image_path,
            page_intro_text=page_intro_text
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Handle gallery images
        if 'gallery_images' in request.files:
            files = request.files.getlist('gallery_images')
            for idx, file in enumerate(files):
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{slug}-gallery-{idx}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    image = ProjectImage(
                        project_id=project.id,
                        image_path=f"uploads/{filename}",
                        display_order=idx
                    )
                    db.session.add(image)
        
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/projects/form.html', project=None)

@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@require_admin
def admin_project_edit(project_id):
    """Edit existing project"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        try:
            project.title = request.form.get('title')
            category_value = request.form.get('category')
            if category_value:
                project.category = ProjectCategory[category_value.upper()]
            project.preview_summary = request.form.get('preview_summary')
            project.page_intro_text = request.form.get('page_intro_text', '')
            
            # Update slug if title changed
            new_slug = generate_slug(project.title)
            if new_slug != project.slug:
                base_slug = new_slug
                counter = 1
                while Project.query.filter_by(slug=new_slug).first() and Project.query.filter_by(slug=new_slug).first().id != project.id:
                    new_slug = f"{base_slug}-{counter}"
                    counter += 1
                project.slug = new_slug
            
            # Handle preview image update
            if 'preview_image' in request.files:
                file = request.files['preview_image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{project.slug}-preview-{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    project.preview_image_path = f"uploads/{filename}"
            
            # Handle new gallery images
            if 'gallery_images' in request.files:
                files = request.files.getlist('gallery_images')
                existing_count = ProjectImage.query.filter_by(project_id=project.id).count()
                for idx, file in enumerate(files):
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filename = f"{project.slug}-gallery-{existing_count + idx}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        image = ProjectImage(
                            project_id=project.id,
                            image_path=f"uploads/{filename}",
                            display_order=existing_count + idx
                        )
                        db.session.add(image)
            
            project.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin_projects'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'error')
            # Continue to render the form with error message
    
    images = ProjectImage.query.filter_by(project_id=project.id).order_by(ProjectImage.display_order).all()
    return render_template('admin/projects/form.html', project=project, images=images)

@app.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
@require_admin
def admin_project_delete(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/projects/<int:project_id>/images/<int:image_id>/delete', methods=['POST'])
@require_admin
def admin_project_image_delete(project_id, image_id):
    """Delete project image"""
    image = ProjectImage.query.get_or_404(image_id)
    if image.project_id != project_id:
        flash('Invalid image.', 'error')
        return redirect(url_for('admin_project_edit', project_id=project_id))
    
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('admin_project_edit', project_id=project_id))

# ==================== ADMIN: PUBLICATIONS ====================

@app.route('/admin/publications')
@require_admin
def admin_publications():
    """List all publications"""
    publications = Publication.query.order_by(Publication.publication_date.desc()).all()
    return render_template('admin/publications/list.html', publications=publications)

@app.route('/admin/publications/new', methods=['GET', 'POST'])
@require_admin
def admin_publication_new():
    """Create new publication"""
    if request.method == 'POST':
        publication = Publication(
            title=request.form.get('title'),
            journal=request.form.get('journal'),
            publication_date=request.form.get('publication_date'),
            authors=request.form.get('authors'),
            url=request.form.get('url')
        )
        db.session.add(publication)
        db.session.commit()
        flash('Publication created successfully!', 'success')
        return redirect(url_for('admin_publications'))
    
    return render_template('admin/publications/form.html', publication=None)

@app.route('/admin/publications/<int:pub_id>/edit', methods=['GET', 'POST'])
@require_admin
def admin_publication_edit(pub_id):
    """Edit existing publication"""
    publication = Publication.query.get_or_404(pub_id)
    
    if request.method == 'POST':
        publication.title = request.form.get('title')
        publication.journal = request.form.get('journal')
        publication.publication_date = request.form.get('publication_date')
        publication.authors = request.form.get('authors')
        publication.url = request.form.get('url')
        publication.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Publication updated successfully!', 'success')
        return redirect(url_for('admin_publications'))
    
    return render_template('admin/publications/form.html', publication=publication)

@app.route('/admin/publications/<int:pub_id>/delete', methods=['POST'])
@require_admin
def admin_publication_delete(pub_id):
    """Delete publication"""
    publication = Publication.query.get_or_404(pub_id)
    db.session.delete(publication)
    db.session.commit()
    flash('Publication deleted successfully!', 'success')
    return redirect(url_for('admin_publications'))

# ==================== ADMIN: EXPERIENCES ====================

@app.route('/admin/experiences')
@require_admin
def admin_experiences():
    """List all experiences"""
    experiences = Experience.query.order_by(Experience.created_at.desc()).all()
    return render_template('admin/experiences/list.html', experiences=experiences)

@app.route('/admin/experiences/new', methods=['GET', 'POST'])
@require_admin
def admin_experience_new():
    """Create new experience"""
    if request.method == 'POST':
        experience = Experience(
            title=request.form.get('title'),
            description=request.form.get('description')
        )
        db.session.add(experience)
        db.session.commit()
        flash('Experience created successfully!', 'success')
        return redirect(url_for('admin_experiences'))
    
    return render_template('admin/experiences/form.html', experience=None)

@app.route('/admin/experiences/<int:exp_id>/edit', methods=['GET', 'POST'])
@require_admin
def admin_experience_edit(exp_id):
    """Edit existing experience"""
    experience = Experience.query.get_or_404(exp_id)
    
    if request.method == 'POST':
        experience.title = request.form.get('title')
        experience.description = request.form.get('description')
        experience.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('admin_experiences'))
    
    return render_template('admin/experiences/form.html', experience=experience)

@app.route('/admin/experiences/<int:exp_id>/delete', methods=['POST'])
@require_admin
def admin_experience_delete(exp_id):
    """Delete experience"""
    experience = Experience.query.get_or_404(exp_id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('admin_experiences'))

# ==================== ADMIN: ABOUT PAGE ====================

@app.route('/admin/about/edit', methods=['GET', 'POST'])
@require_admin
def admin_about_edit():
    """Edit about page content"""
    about_page = AboutPage.query.first()
    
    if request.method == 'POST':
        content = request.form.get('content', '')
        if about_page:
            about_page.content = content
            about_page.updated_at = datetime.utcnow()
        else:
            about_page = AboutPage(content=content)
            db.session.add(about_page)
        db.session.commit()
        flash('About page updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # If no about page exists, use default content
    if not about_page:
        default_content = """I am a medical student with a deep passion for leveraging technology to solve complex problems in healthcare. 
My journey combines rigorous medical training with expertise in machine learning, computer vision, and full-stack 
web development.

Through my research and projects, I've developed automated systems for medical image analysis, built predictive 
models for patient outcomes, and created web applications that make healthcare data more accessible. I believe in 
the power of interdisciplinary collaboration to drive innovation in medicine.

When I'm not studying or coding, I enjoy exploring new technologies, contributing to open-source projects, and 
sharing knowledge with the medical and tech communities. My goal is to bridge the gap between clinical practice 
and cutting-edge technology to improve patient care."""
        content = default_content
    else:
        content = about_page.content
    
    return render_template('admin/about/form.html', content=content)

# ==================== ADMIN: CV MANAGEMENT ====================

@app.route('/admin/cv/edit', methods=['GET', 'POST'])
@require_admin
def admin_cv_edit():
    """Edit CV file and download name"""
    cv = CV.query.first()
    
    if request.method == 'POST':
        download_name = request.form.get('download_name', '').strip()
        
        if not download_name:
            flash('Download name is required.', 'error')
            return render_template('admin/cv/form.html', cv=cv)
        
        # Ensure download name ends with .pdf
        if not download_name.lower().endswith('.pdf'):
            download_name += '.pdf'
        
        # Handle file upload
        file_path = None
        if 'cv_file' in request.files:
            file = request.files['cv_file']
            if file and file.filename:
                # Check if it's a PDF
                if not file.filename.lower().endswith('.pdf'):
                    flash('Only PDF files are allowed.', 'error')
                    return render_template('admin/cv/form.html', cv=cv)
                
                # Save the file
                filename = secure_filename(file.filename)
                filename = f"cv-{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                file_path = f"uploads/{filename}"
        
        # Update or create CV record
        if cv:
            if file_path:
                # Delete old file if it's in uploads/ (not graphics/)
                if cv.file_path.startswith('uploads/'):
                    old_file_path = os.path.join('static', cv.file_path)
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except:
                            pass  # Ignore errors when deleting old file
                cv.file_path = file_path
            cv.download_name = download_name
            cv.updated_at = datetime.utcnow()
        else:
            # Use existing file path if no new file uploaded, otherwise use default
            if not file_path:
                file_path = 'graphics/my_cv.pdf'
            cv = CV(file_path=file_path, download_name=download_name)
            db.session.add(cv)
        
        db.session.commit()
        flash('CV updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/cv/form.html', cv=cv)

# ==================== INITIALIZATION ====================

def init_db():
    """Initialize database tables and seed data if needed"""
    with app.app_context():
        db.create_all()
        # Check if database is empty and seed if needed
        if Project.query.count() == 0:
            from seed import seed_database
            seed_database()

if __name__ == '__main__':
    init_db()
    # Use PORT environment variable for Render, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    # Only run in debug mode if not in production
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

