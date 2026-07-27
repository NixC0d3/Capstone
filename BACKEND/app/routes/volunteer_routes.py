from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.extensions import db


volunteer_allocation_bp = Blueprint("volunteer_allocation_bp", __name__)


def get_required_skills(volunteer_need_id):
    result = db.session.execute(
        text("""
            SELECT LOWER(TRIM(skill_name)) AS skill_name
            FROM volunteer_required_skills
            WHERE volunteer_need_id = :volunteer_need_id;
        """),
        {"volunteer_need_id": volunteer_need_id}
    )

    return [row.skill_name for row in result]


def get_user_skills(user_id):
    result = db.session.execute(
        text("""
            SELECT LOWER(TRIM(skill_name)) AS skill_name
            FROM user_skills
            WHERE user_id = :user_id;
        """),
        {"user_id": user_id}
    )

    return [row.skill_name for row in result]


def get_user_preferences(user_id):
    result = db.session.execute(
        text("""
            SELECT category_id
            FROM user_preferences
            WHERE user_id = :user_id;
        """),
        {"user_id": user_id}
    )

    return [row.category_id for row in result]


def get_need_category_ids(organisation_id):
    result = db.session.execute(
        text("""
            SELECT DISTINCT category_id
            FROM (
                SELECT category_id
                FROM organisations
                WHERE organisation_id = :organisation_id
                  AND category_id IS NOT NULL

                UNION

                SELECT category_id
                FROM organisation_categories
                WHERE organisation_id = :organisation_id
            ) categories_for_need;
        """),
        {"organisation_id": organisation_id}
    )

    return [row.category_id for row in result]


def calculate_skill_score(required_skills, user_skills):
    if not required_skills:
        return 0, []

    matched_skills = []

    for skill in required_skills:
        if skill in user_skills:
            matched_skills.append(skill)

    skill_score = (len(matched_skills) / len(required_skills)) * 50

    return skill_score, matched_skills
    
@volunteer_allocation_bp.route("/needs", methods=["POST"])
def create_volunteer_need():
    data = request.get_json() or {}

    charity_user_id = data.get("charity_user_id")
    title = data.get("title")
    description = data.get("description", "")
    urgency_level = data.get("urgency_level", "medium")
    needed_date = data.get("needed_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    volunteers_needed = data.get("volunteers_needed", 1)
    required_skills = data.get("required_skills", [])

    if not charity_user_id:
        return jsonify(error="charity_user_id is required"), 400

    if not title:
        return jsonify(error="title is required"), 400

    # Find the charity organisation owned by the logged-in charity user
    organisation = db.session.execute(
        text("""
            SELECT organisation_id
            FROM organisations
            WHERE owner_user_id = :charity_user_id
              AND LOWER(organisation_type) = 'charity'
            LIMIT 1;
        """),
        {"charity_user_id": charity_user_id}
    ).fetchone()

    if not organisation:
        return jsonify(error="No charity organisation found for this user"), 404

    # Create the volunteer need
    new_need = db.session.execute(
        text("""
            INSERT INTO volunteer_needs
            (
                organisation_id,
                title,
                description,
                urgency_level,
                status,
                created_at,
                needed_date,
                start_time,
                end_time,
                volunteers_needed
            )
            VALUES
            (
                :organisation_id,
                :title,
                :description,
                :urgency_level,
                'open',
                CURRENT_TIMESTAMP,
                :needed_date,
                :start_time,
                :end_time,
                :volunteers_needed
            )
            RETURNING volunteer_need_id;
        """),
        {
            "organisation_id": organisation.organisation_id,
            "title": title,
            "description": description,
            "urgency_level": urgency_level.lower(),
            "needed_date": needed_date,
            "start_time": start_time,
            "end_time": end_time,
            "volunteers_needed": volunteers_needed
        }
    ).fetchone()

    volunteer_need_id = new_need.volunteer_need_id

    # Save required skills
    for skill in required_skills:
        clean_skill = skill.strip()

        if clean_skill:
            db.session.execute(
                text("""
                    INSERT INTO volunteer_required_skills
                    (
                        volunteer_need_id,
                        skill_name
                    )
                    VALUES
                    (
                        :volunteer_need_id,
                        :skill_name
                    );
                """),
                {
                    "volunteer_need_id": volunteer_need_id,
                    "skill_name": clean_skill
                }
            )

    db.session.commit()

    return jsonify({
        "message": "Volunteer need created successfully",
        "volunteer_need_id": volunteer_need_id
    }), 201


@volunteer_allocation_bp.route("/needs", methods=["GET"])
def get_volunteer_needs():
    charity_user_id = request.args.get("charity_user_id", type=int)

    if not charity_user_id:
        return jsonify(error="charity_user_id is required"), 400

    result = db.session.execute(
        text("""
            SELECT
                vn.volunteer_need_id,
                vn.organisation_id,
                o.organisation_name,
                vn.title,
                vn.description,
                vn.needed_date,
                vn.start_time,
                vn.end_time,
                vn.urgency_level,
                vn.volunteers_needed,
                vn.status,
                l.parish,
                l.town
            FROM volunteer_needs vn
            JOIN organisations o
                ON o.organisation_id = vn.organisation_id
            LEFT JOIN locations l
                ON l.location_id = o.location_id
            WHERE o.owner_user_id = :charity_user_id
            ORDER BY vn.volunteer_need_id;
        """),
        {"charity_user_id": charity_user_id}
    )

    needs = []

    for row in result:
        skills_result = db.session.execute(
            text("""
                SELECT skill_name
                FROM volunteer_required_skills
                WHERE volunteer_need_id = :volunteer_need_id
                ORDER BY skill_name;
            """),
            {"volunteer_need_id": row.volunteer_need_id}
        )

        required_skills = [skill.skill_name for skill in skills_result]

        needs.append({
            "volunteer_need_id": row.volunteer_need_id,
            "organisation_id": row.organisation_id,
            "organisation_name": row.organisation_name,
            "title": row.title,
            "description": row.description,
            "needed_date": row.needed_date.isoformat() if row.needed_date else None,
            "start_time": str(row.start_time) if row.start_time else None,
            "end_time": str(row.end_time) if row.end_time else None,
            "urgency_level": row.urgency_level,
            "volunteers_needed": row.volunteers_needed,
            "status": row.status,
            "parish": row.parish,
            "town": row.town,
            "required_skills": required_skills
        })

    return jsonify(needs), 200

@volunteer_allocation_bp.route("/need/<int:volunteer_need_id>/matches", methods=["GET"])
def find_matching_volunteers(volunteer_need_id):
    charity_user_id = request.args.get("charity_user_id", type=int)

    if not charity_user_id:
        return jsonify(error="charity_user_id is required"), 400
    
    need = db.session.execute(
        text("""
            SELECT
                vn.volunteer_need_id,
                vn.organisation_id,
                vn.title,
                vn.description,
                vn.needed_date,
                vn.start_time,
                vn.end_time,
                vn.urgency_level,
                vn.volunteers_needed,
                vn.status,

                o.organisation_name,
                o.location_id,

                l.parish AS need_parish,
                l.town AS need_town
            FROM volunteer_needs vn
            JOIN organisations o
                ON o.organisation_id = vn.organisation_id
            LEFT JOIN locations l
                ON l.location_id = o.location_id
            WHERE vn.volunteer_need_id = :volunteer_need_id
                AND o.owner_user_id = :charity_user_id;
        """),
        {
          "volunteer_need_id": volunteer_need_id,
          "charity_user_id": charity_user_id
        }
    ).fetchone()

    if not need:
        return jsonify(error="Volunteer need not found for this charity"), 404

    required_skills = get_required_skills(volunteer_need_id)
    need_category_ids = get_need_category_ids(need.organisation_id)

    users = db.session.execute(
		text("""
			SELECT
				u.user_id,
				COALESCE(u.display_name, u.first_name || ' ' || u.last_name) AS display_name,
				u.email,
				u.location_id,

				l.parish AS user_parish,
				l.town AS user_town
			FROM users u
			LEFT JOIN locations l
				ON l.location_id = u.location_id
			WHERE u.role_id = 1
			  AND LOWER(COALESCE(u.email, '')) NOT LIKE '%@civilinfohub.test'
			  AND LOWER(COALESCE(u.display_name, '')) NOT LIKE 'demo recommendation user%'
			  AND LOWER(COALESCE(u.display_name, '')) NOT LIKE 'gen% general user';
		""")
	).fetchall()

    matches = []

    for user in users:
        user_skills = get_user_skills(user.user_id)
        user_preferences = get_user_preferences(user.user_id)

        skill_score, matched_skills = calculate_skill_score(
            required_skills,
            user_skills
        )

        cause_score = 0
        for category_id in need_category_ids:
            if category_id in user_preferences:
                cause_score = 25
                break

        location_score = 0
        if need.location_id and user.location_id and need.location_id == user.location_id:
            location_score = 15
        elif need.need_parish and user.user_parish and need.need_parish == user.user_parish:
            location_score = 10

        # Simple version for demo.
        # Later, this can be connected to user_availability.
        availability_score = 10

        total_score = (
            skill_score
            + cause_score
            + location_score
            + availability_score
        )

        matches.append({
            "user_id": user.user_id,
            "display_name": user.display_name,
            "email": user.email,
            "user_parish": user.user_parish,
            "user_town": user.user_town,

            "required_skills": required_skills,
            "user_skills": user_skills,
            "matched_skills": matched_skills,

            "skill_score": round(skill_score, 2),
            "cause_score": cause_score,
            "location_score": location_score,
            "availability_score": availability_score,
            "match_score": round(total_score, 2)
        })

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return jsonify({
        "need": {
            "volunteer_need_id": need.volunteer_need_id,
            "organisation_id": need.organisation_id,
            "organisation_name": need.organisation_name,
            "title": need.title,
            "description": need.description,
            "needed_date": need.needed_date.isoformat() if need.needed_date else None,
            "start_time": str(need.start_time) if need.start_time else None,
            "end_time": str(need.end_time) if need.end_time else None,
            "urgency_level": need.urgency_level,
            "volunteers_needed": need.volunteers_needed,
            "need_parish": need.need_parish,
            "need_town": need.need_town,
            "required_skills": required_skills,
            "category_ids": need_category_ids
        },
        "matches": matches
    }), 200


@volunteer_allocation_bp.route("/need/<int:volunteer_need_id>/allocate", methods=["POST"])
def allocate_volunteer(volunteer_need_id):
    data = request.get_json() or {}

    user_id = data.get("user_id")
    match_score = data.get("match_score", 0)
    charity_user_id = data.get("charity_user_id")

    if not user_id:
        return jsonify(error="user_id is required"), 400

    if not charity_user_id:
        return jsonify(error="charity_user_id is required"), 400

    # Check that this volunteer need belongs to the logged-in charity user
    owner_check = db.session.execute(
        text("""
            SELECT
                o.owner_user_id
            FROM volunteer_needs vn
            JOIN organisations o
                ON o.organisation_id = vn.organisation_id
            WHERE vn.volunteer_need_id = :volunteer_need_id;
        """),
        {"volunteer_need_id": volunteer_need_id}
    ).fetchone()

    if not owner_check:
        return jsonify(error="Volunteer need not found"), 404

    if owner_check.owner_user_id != int(charity_user_id):
        return jsonify(error="You cannot allocate volunteers for another charity's need"), 403

    # Only insert after ownership has been confirmed
    db.session.execute(
        text("""
            INSERT INTO volunteer_allocations
            (
                volunteer_need_id,
                user_id,
                matching_score,
                allocation_status,
                allocated_at
            )
            VALUES
            (
                :volunteer_need_id,
                :user_id,
                :matching_score,
                'allocated',
                CURRENT_TIMESTAMP
            );
        """),
        {
            "volunteer_need_id": volunteer_need_id,
            "user_id": user_id,
            "matching_score": match_score
        }
    )

    db.session.commit()

    return jsonify({
        "message": "Volunteer allocated successfully",
        "volunteer_need_id": volunteer_need_id,
        "user_id": user_id,
        "match_score": match_score
    }), 201
