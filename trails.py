from flask import jsonify, request
from sql_connection import get_db_connection
from flask import g, jsonify
from middleware import authorize_user
import logging

logging.basicConfig(level=logging.DEBUG)

# Get all trails (accessible by all authenticated users)
@authorize_user('General_user', 'Admin')  # Ensure only authenticated users with 'General_user' role can access
def get_trails():
    logging.debug(f"User accessing trails: {g.user_email}")  # Log the authenticated user's email

    try:
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the stored procedure to fetch all trails
        logging.debug("Executing stored procedure: CW2.GetAllTrails")
        cursor.execute("EXEC CW2.GetAllTrails")
        rows = cursor.fetchall()

        # Extract column names and zip with row data to form dictionaries
        if rows:
            trails = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            logging.debug(f"Fetched {len(trails)} trails successfully.")
        else:
            trails = []
            logging.debug("No trails found in the database.")

        # Close the connection
        conn.close()

        # Return the list of trails as JSON
        return jsonify(trails), 200

    except Exception as e:
        # Log the exception with detailed information
        logging.error(f"Error fetching trails: {str(e)}", exc_info=True)

        # Close the connection in case of an error
        if conn:
            conn.close()

        # Return an error response
        return jsonify({"error": "An error occurred while fetching trails."}), 500

# Get a trail by ID (accessible by all authenticated users)
@authorize_user('General_user', 'Admin')
def get_trail(trail_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC CW2.GetTrail @TrailID = ?", (trail_id,))
        row = cursor.fetchone()
        if row:
            trail = dict(zip([column[0] for column in cursor.description], row))
        else:
            trail = None
        conn.close()
        return jsonify(trail) if trail else ('Not Found', 404)
    except Exception as e:
        logging.error(f"Error fetching trail ID {trail_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Create a trail (accessible only by Admins)
@authorize_user('Admin')
def create_trail():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO CW2.Trail (
                Trail_name, Trail_summary, Trail_description, Difficulty, Location,
                Length, Elevation_gain, Route_type, OwnerID, Pt1_Lat, Pt1_Long, Pt1_Desc,
                Pt2_Lat, Pt2_Long, Pt2_Desc, Pt3_Lat, Pt3_Long, Pt3_Desc, Pt4_Lat, Pt4_Long,
                Pt4_Desc, Pt5_Lat, Pt5_Long, Pt5_Desc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data['Trail_name'], data.get('Trail_summary'), data.get('Trail_description'),
            data.get('Difficulty'), data.get('Location'), data.get('Length'),
            data.get('Elevation_gain'), data.get('Route_type'), data.get('OwnerID'),
            data.get('Pt1_Lat'), data.get('Pt1_Long'), data.get('Pt1_Desc'),
            data.get('Pt2_Lat'), data.get('Pt2_Long'), data.get('Pt2_Desc'),
            data.get('Pt3_Lat'), data.get('Pt3_Long'), data.get('Pt3_Desc'),
            data.get('Pt4_Lat'), data.get('Pt4_Long'), data.get('Pt4_Desc'),
            data.get('Pt5_Lat'), data.get('Pt5_Long'), data.get('Pt5_Desc')
        )

        cursor.execute(insert_query, params)
        conn.commit()

        fetch_query = "SELECT SCOPE_IDENTITY()"
        cursor.execute(fetch_query)
        new_trail_id = cursor.fetchone()[0]

        return jsonify({"message": "Trail created successfully", "TrailID": new_trail_id}), 201
    except Exception as e:
        logging.error(f"Error creating trail: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Update a trail (accessible only by Admins)
@authorize_user('Admin')
def update_trail(trail_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            EXEC CW2.UpdateTrail 
            @TrailID = ?, 
            @Trail_name = ?, 
            @Trail_summary = ?, 
            @Trail_description = ?, 
            @Difficulty = ?, 
            @Location = ?, 
            @Length = ?, 
            @Elevation_gain = ?, 
            @Route_type = ?, 
            @OwnerID = ?, 
            @Pt1_Lat = ?, 
            @Pt1_Long = ?, 
            @Pt1_Desc = ?, 
            @Pt2_Lat = ?, 
            @Pt2_Long = ?, 
            @Pt2_Desc = ?, 
            @Pt3_Lat = ?, 
            @Pt3_Long = ?, 
            @Pt3_Desc = ?, 
            @Pt4_Lat = ?, 
            @Pt4_Long = ?, 
            @Pt4_Desc = ?, 
            @Pt5_Lat = ?, 
            @Pt5_Long = ?, 
            @Pt5_Desc = ?
        """, (
            trail_id, data['Trail_name'], data['Trail_summary'], data['Trail_description'],
            data['Difficulty'], data['Location'], data['Length'], data['Elevation_gain'],
            data['Route_type'], data['OwnerID'], data.get('Pt1_Lat'), data.get('Pt1_Long'),
            data.get('Pt1_Desc'), data.get('Pt2_Lat'), data.get('Pt2_Long'), data.get('Pt2_Desc'),
            data.get('Pt3_Lat'), data.get('Pt3_Long'), data.get('Pt3_Desc'), 
            data.get('Pt4_Lat'), data.get('Pt4_Long'), data.get('Pt4_Desc'), 
            data.get('Pt5_Lat'), data.get('Pt5_Long'), data.get('Pt5_Desc')
        ))
        conn.commit()
        return ('Updated', 200)
    except Exception as e:
        if conn:
            conn.rollback()
        return (f"Error updating trail: {str(e)}", 500)
    finally:
        if conn:
            conn.close()

# Delete a trail (accessible only by Admins)
@authorize_user('Admin')
def delete_trail(trail_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC CW2.DeleteTrail @TrailID = ?", (trail_id,))
        conn.commit()
        return ('Deleted', 200)
    except Exception as e:
        return (f"Error deleting trail: {str(e)}", 500)
    finally:
        conn.close()
