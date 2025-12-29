"""
Seed script to populate database with example content
"""
from models import db, Project, ProjectImage, Publication, Experience, ProjectCategory

def seed_database():
    """Seed the database with example data"""
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # db.session.query(ProjectImage).delete()
    # db.session.query(Project).delete()
    # db.session.query(Publication).delete()
    # db.session.query(Experience).delete()
    
    # Seed Projects
    projects_data = [
        {
            'category': ProjectCategory.MEDICINE,
            'title': 'Automated Retinal Disease Detection',
            'slug': 'automated-retinal-disease-detection',
            'preview_summary': 'AI-powered system for early detection of diabetic retinopathy using deep learning',
            'page_intro_text': 'This project leverages convolutional neural networks to analyze retinal images and identify early signs of diabetic retinopathy. The system achieves 94% accuracy in detecting microaneurysms and hemorrhages, enabling earlier intervention and treatment.',
            'preview_image': 'graphics/test_image.png'
        },
        {
            'category': ProjectCategory.MEDICINE,
            'title': 'Surgical Tool Recognition System',
            'slug': 'surgical-tool-recognition-system',
            'preview_summary': 'Computer vision system for real-time identification of surgical instruments during procedures',
            'page_intro_text': 'A real-time computer vision system that identifies and tracks surgical instruments during operations. This helps reduce errors and improve surgical workflow efficiency.',
            'preview_image': 'graphics/test_image.png'
        },
        {
            'category': ProjectCategory.MEDICINE,
            'title': 'Patient Risk Prediction Model',
            'slug': 'patient-risk-prediction-model',
            'preview_summary': 'Machine learning model predicting patient outcomes using clinical data',
            'page_intro_text': 'A survival analysis model that predicts patient outcomes based on clinical variables. The model uses gradient boosting and has been validated on a dataset of over 10,000 patients.',
            'preview_image': 'graphics/test_image.png'
        },
        {
            'category': ProjectCategory.CREATIVE,
            'title': 'Interactive Data Visualization Platform',
            'slug': 'interactive-data-visualization-platform',
            'preview_summary': 'Web-based tool for creating beautiful, interactive data visualizations',
            'page_intro_text': 'A full-stack web application that allows users to upload datasets and create interactive visualizations. Built with modern web technologies and featuring a responsive design.',
            'preview_image': 'graphics/test_image.png'
        },
        {
            'category': ProjectCategory.CREATIVE,
            'title': 'Personal Portfolio Website',
            'slug': 'personal-portfolio-website',
            'preview_summary': 'Custom-built portfolio site showcasing projects and experiences',
            'page_intro_text': 'A responsive portfolio website built from scratch with Flask and vanilla JavaScript. Features custom animations, dark theme, and a content management system.',
            'preview_image': 'graphics/test_image.png'
        },
        {
            'category': ProjectCategory.CREATIVE,
            'title': 'Music Recommendation Engine',
            'slug': 'music-recommendation-engine',
            'preview_summary': 'Algorithm that suggests music based on listening patterns and preferences',
            'page_intro_text': 'A collaborative filtering system that analyzes user listening patterns to recommend new music. Uses matrix factorization techniques to find similar users and songs.',
            'preview_image': 'graphics/test_image.png'
        }
    ]
    
    for proj_data in projects_data:
        project = Project(
            category=proj_data['category'],
            title=proj_data['title'],
            slug=proj_data['slug'],
            preview_summary=proj_data['preview_summary'],
            preview_image_path=proj_data['preview_image'],
            page_intro_text=proj_data['page_intro_text']
        )
        db.session.add(project)
        db.session.flush()  # Get the project ID
        
        # Add a gallery image for each project
        gallery_image = ProjectImage(
            project_id=project.id,
            image_path='graphics/test_image.png',
            display_order=0
        )
        db.session.add(gallery_image)
    
    # Seed Publications
    publications_data = [
        {
            'title': 'Deep Learning for Medical Image Analysis: A Comprehensive Review',
            'journal': 'Journal of Medical AI',
            'publication_date': '2024-01-15',
            'authors': 'Sundeep Chakladar, Jane Smith, John Doe',
            'url': 'https://example.com/publication1'
        },
        {
            'title': 'Automated Detection of Pathological Features in Retinal Images',
            'journal': 'IEEE Transactions on Biomedical Engineering',
            'publication_date': '2023-11-20',
            'authors': 'Sundeep Chakladar, Alice Johnson',
            'url': 'https://example.com/publication2'
        },
        {
            'title': 'Machine Learning Approaches to Patient Outcome Prediction',
            'journal': 'Nature Medicine',
            'publication_date': '2023-08-10',
            'authors': 'Sundeep Chakladar, Bob Williams, Carol Brown',
            'url': 'https://example.com/publication3'
        },
        {
            'title': 'Computer Vision in Surgical Applications: Current State and Future Directions',
            'journal': 'Surgical Innovation',
            'publication_date': '2023-05-22',
            'authors': 'Sundeep Chakladar, David Lee',
            'url': 'https://example.com/publication4'
        },
        {
            'title': 'Unsupervised Clustering of Clinical Data for Patient Stratification',
            'journal': 'Journal of Clinical Informatics',
            'publication_date': '2023-03-14',
            'authors': 'Sundeep Chakladar, Emma Davis, Frank Miller',
            'url': 'https://example.com/publication5'
        },
        {
            'title': 'Risk Prediction Models in Emergency Medicine: A Comparative Study',
            'journal': 'Emergency Medicine Journal',
            'publication_date': '2022-12-05',
            'authors': 'Sundeep Chakladar, Grace Wilson',
            'url': 'https://example.com/publication6'
        }
    ]
    
    for pub_data in publications_data:
        publication = Publication(
            title=pub_data['title'],
            journal=pub_data['journal'],
            publication_date=pub_data['publication_date'],
            authors=pub_data['authors'],
            url=pub_data['url']
        )
        db.session.add(publication)
    
    # Seed Experiences
    experiences_data = [
        {
            'title': 'Medical Research Intern',
            'description': 'Conducted research on machine learning applications in medical imaging. Developed and validated deep learning models for disease detection, achieving state-of-the-art results. Collaborated with clinical teams to ensure model interpretability and clinical relevance.'
        },
        {
            'title': 'Full-Stack Developer',
            'description': 'Built and deployed web applications for healthcare organizations. Designed user interfaces, implemented backend APIs, and managed database systems. Worked with modern frameworks and cloud deployment platforms.'
        },
        {
            'title': 'Data Science Consultant',
            'description': 'Provided data analysis and machine learning consulting services to medical institutions. Developed predictive models, performed statistical analysis, and created data visualizations to support clinical decision-making.'
        },
        {
            'title': 'Teaching Assistant - Medical Informatics',
            'description': 'Assisted in teaching medical informatics courses. Helped students understand machine learning concepts, supervised lab sessions, and graded assignments. Developed educational materials and tutorials.'
        },
        {
            'title': 'Open Source Contributor',
            'description': 'Contributed to open-source medical imaging libraries. Fixed bugs, added features, and improved documentation. Collaborated with international developers on projects used by thousands of researchers worldwide.'
        },
        {
            'title': 'Conference Presenter',
            'description': 'Presented research findings at multiple international conferences. Delivered talks on machine learning in healthcare, participated in panel discussions, and networked with researchers and industry professionals.'
        }
    ]
    
    for exp_data in experiences_data:
        experience = Experience(
            title=exp_data['title'],
            description=exp_data['description']
        )
        db.session.add(experience)
    
    db.session.commit()
    print("Database seeded successfully!")

