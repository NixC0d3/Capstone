from app import app
from app.extensions import db
from app.models import Role, Category

with app.app_context():
    db.create_all()

    default_roles = ["general_user", "business_user", "charity_user", "admin"]
    for role_name in default_roles:
        if not Role.query.filter_by(role_name=role_name).first():
            db.session.add(Role(role_name=role_name))

    default_categories = [
        ("Food", "business"),
        ("Education", "charity"),
        ("Health", "both"),
        ("Community Support", "charity"),
        ("Retail", "business"),
    ]
    for category_name, category_type in default_categories:
        if not Category.query.filter_by(category_name=category_name).first():
            db.session.add(Category(category_name=category_name, category_type=category_type))

    db.session.commit()
    print("CivilInfoHub seed data added.")
