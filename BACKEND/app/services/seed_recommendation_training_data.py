import random
from datetime import datetime, timedelta

import psycopg2


DB_NAME = "capstone"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

DEMO_USER_COUNT = 40

PERSONAS = [
    ["Beauty", "Salon", "Health"],
    ["Restaurant", "Wholesale and Grocery", "Retail"],
    ["Construction", "Repair", "HomeCenter"],
    ["Fashion", "Arts", "Arts and Crafts"],
    ["Tech", "Marketing", "Finance"],
    ["Farming", "Construction", "Repair"],
    ["Education", "Food Drives", "Social Safety Net Programmes"],
    ["Climate Change", "Clean Up", "Animal Welfare"],
]

REVIEW_COMMENTS = [
    "Very helpful and professional service.",
    "I had a good experience with this organisation.",
    "The service was useful and easy to access.",
    "I would recommend this to other users.",
    "Good communication and reliable support.",
    "The organisation matched what I was looking for.",
    "Very responsive and helpful.",
    "I enjoyed the service and would use it again.",
]


def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def make_sure_review_is_allowed(cursor):
    cursor.execute("""
        ALTER TABLE engagement_logs
        DROP CONSTRAINT IF EXISTS engagement_logs_engagement_type_check;
    """)

    cursor.execute("""
        ALTER TABLE engagement_logs
        ADD CONSTRAINT engagement_logs_engagement_type_check
        CHECK (
            engagement_type IN (
                'profile_view',
                'save',
                'message',
                'rating',
                'review',
                'volunteer_signup'
            )
        );
    """)


def create_demo_users(cursor):
    for i in range(1, DEMO_USER_COUNT + 1):
        email = f"demo_rec_user_{i}@civilinfohub.test"
        first_name = f"DemoRec{i}"
        last_name = "GeneralUser"
        display_name = f"Demo Recommendation User {i}"

        cursor.execute("""
            INSERT INTO users
            (
                role_id,
                first_name,
                last_name,
                email,
                password_hash,
                display_name,
                created_at
            )
            SELECT
                1,
                %s,
                %s,
                %s,
                %s,
                %s,
                CURRENT_TIMESTAMP
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE email = %s
            );
        """, (
            first_name,
            last_name,
            email,
            "password",
            display_name,
            email,
        ))


def get_general_users(cursor):
    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE role_id = 1
        ORDER BY user_id;
    """)

    return [row[0] for row in cursor.fetchall()]


def get_categories(cursor):
    cursor.execute("""
        SELECT category_id, category_name
        FROM categories;
    """)

    categories = {}

    for category_id, category_name in cursor.fetchall():
        categories[category_name.lower()] = category_id

    return categories


def get_orgs_for_categories(cursor, category_ids):
    if not category_ids:
        return []

    cursor.execute("""
        SELECT DISTINCT o.organisation_id
        FROM organisations o
        LEFT JOIN organisation_categories oc
            ON oc.organisation_id = o.organisation_id
        WHERE o.category_id = ANY(%s)
           OR oc.category_id = ANY(%s);
    """, (category_ids, category_ids))

    return [row[0] for row in cursor.fetchall()]


def insert_user_preference(cursor, user_id, category_id, weight):
    cursor.execute("""
        INSERT INTO user_preferences
        (
            user_id,
            category_id,
            preference_weight
        )
        SELECT
            %s,
            %s,
            %s
        WHERE NOT EXISTS (
            SELECT 1
            FROM user_preferences
            WHERE user_id = %s
              AND category_id = %s
        );
    """, (
        user_id,
        category_id,
        weight,
        user_id,
        category_id,
    ))


def insert_engagement(cursor, user_id, organisation_id, engagement_type):
    random_days = random.randint(1, 60)
    random_minutes = random.randint(1, 1440)
    created_at = datetime.now() - timedelta(days=random_days, minutes=random_minutes)

    cursor.execute("""
        INSERT INTO engagement_logs
        (
            organisation_id,
            user_id,
            engagement_type,
            created_at
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        );
    """, (
        organisation_id,
        user_id,
        engagement_type,
        created_at,
    ))


def insert_rating_review(cursor, user_id, organisation_id):
    rating = random.choice([4, 4, 4, 5, 5, 3])
    review_text = random.choice(REVIEW_COMMENTS)
    created_at = datetime.now() - timedelta(
        days=random.randint(1, 60),
        minutes=random.randint(1, 1440)
    )

    cursor.execute("""
        INSERT INTO ratings_reviews
        (
            organisation_id,
            user_id,
            rating,
            review_text,
            created_at,
            is_hidden
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            FALSE
        );
    """, (
        organisation_id,
        user_id,
        rating,
        review_text,
        created_at,
    ))


def seed_training_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        make_sure_review_is_allowed(cursor)

        create_demo_users(cursor)

        users = get_general_users(cursor)
        categories = get_categories(cursor)

        if not users:
            print("No general users found.")
            return

        print(f"General users found: {len(users)}")

        for index, user_id in enumerate(users):
            persona = PERSONAS[index % len(PERSONAS)]

            category_ids = []

            for category_name in persona:
                category_id = categories.get(category_name.lower())

                if category_id:
                    category_ids.append(category_id)
                    insert_user_preference(
                        cursor,
                        user_id,
                        category_id,
                        random.choice([1, 2, 3])
                    )

            matching_orgs = get_orgs_for_categories(cursor, category_ids)

            if not matching_orgs:
                continue

            sample_size = min(len(matching_orgs), random.randint(6, 12))
            selected_orgs = random.sample(matching_orgs, sample_size)

            for organisation_id in selected_orgs:
                # Profile views are low-strength activity
                for _ in range(random.randint(1, 3)):
                    insert_engagement(
                        cursor,
                        user_id,
                        organisation_id,
                        "profile_view"
                    )

                # Saves are stronger activity
                if random.random() < 0.55:
                    insert_engagement(
                        cursor,
                        user_id,
                        organisation_id,
                        "save"
                    )

                # Messages are also strong activity
                if random.random() < 0.35:
                    insert_engagement(
                        cursor,
                        user_id,
                        organisation_id,
                        "message"
                    )

                # Ratings/reviews create actual records
                # Your trigger should also log rating and review.
                if random.random() < 0.45:
                    insert_rating_review(
                        cursor,
                        user_id,
                        organisation_id
                    )

        connection.commit()

        print("Recommendation training data seeded successfully.")

    except Exception as error:
        connection.rollback()
        print("Error seeding recommendation training data:")
        print(error)

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    seed_training_data()
