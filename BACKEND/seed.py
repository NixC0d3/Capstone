from app import app
from app.extensions import db
from app.models import Role, Category, Location

with app.app_context():
    db.create_all()

    default_roles = ["general_user", "business_user", "charity_user", "admin"]
    for role_name in default_roles:
        if not Role.query.filter_by(role_name=role_name).first():
            db.session.add(Role(role_name=role_name))

    default_categories = [
    ("Restaurant", "business"),
    ("Retail", "business"),
    ("Health", "business"),
    ("Beauty", "business"),
    ("Arts and Crafts", "business"),
    ("HomeCenter", "business"),
    ("Repair", "business"),
    ("Tech", "business"),
    ("Dealership and Parts", "business"),
    ("Construction", "business"),
    ("Excursion", "business"),
    ("Farming", "business"),
    ("Marketing", "business"),

    ("Education", "charity"),
    ("Social Safety Net Programmes", "charity"),
    ("Food Drives", "charity"),
    ("Climate Change", "charity"),
    ("Arts", "charity"),
    ("Clean Up", "charity"),
    ("Health Services", "charity"),
    ("Homeless Aid", "charity"),
    ("Faith-Based", "charity")
]
    for category_name, category_type in default_categories:
        if not Category.query.filter_by(category_name=category_name).first():
            db.session.add(Category(category_name=category_name, category_type=category_type))

    default_locations = [
    "Kingston",
    "St. Andrew",
    "St. Thomas",
    "Portland",
    "St. Mary",
    "St. Ann",
    "Trelawny",
    "St. James",
    "Hanover",
    "Westmoreland",
    "St. Elizabeth",
    "Manchester",
    "Clarendon",
    "St. Catherine"
    ]

    for parish_name in default_locations:
        if not Location.query.filter_by(parish=parish_name).first():
            db.session.add(Location(parish=parish_name))

    db.session.commit()
    print("CivilInfoHub seed data added.")
