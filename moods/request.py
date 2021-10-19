import sqlite3
import json
from models import Mood 


def get_all_moods():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT * FROM moods 
        """)

        # Initialize an empty list to hold all mood representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an mood instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # mood class above.
            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)


# # Function with a single parameter
# def get_single_mood(id):
#     with sqlite3.connect("./dailyjournal.db") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         # Use a ? parameter to inject a variable's value
#         # into the SQL statement.
#         db_cursor.execute("""
#         SELECT
#             a.id,
#             a.concept,
#             a.mood,
#             a.mood_id,
#             a.date
#         FROM mood a
#         WHERE a.id = ?
#         """, ( id, ))

#         # Load the single result into memory
#         data = db_cursor.fetchone()

#         # Create an mood instance from the current row
#         mood = mood(data['id'], data['concept'], data['mood'],
#                             data['mood_id'], data['date'])

#         return json.dumps(mood.__dict__)

def create_employee(new_mood):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, animal_id, location_id )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_mood['concept'], new_mood['mood'],
            new_mood['mood_id'], new_mood['date'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_mood['id'] = id



def delete_mood(id):
    # Initial -1 value for mood index, in case one isn't found
    mood_index = -1

    # Iterate the moods list, but use enumerate() so that you
    # can access the index value of each item
    for index, mood in enumerate(moods):
        if mood["id"] == id:
            # Found the mood. Store the current index.
            mood_index = index

    # If the mood was found, use pop(int) to remove it from list
    if mood_index >= 0:
        moods.pop(mood_index)

def get_moods_by_email(mood):

    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.concept,
            c.mood,
            c.mood,
            c.date
        from mood c
        WHERE c.mood = ?
        """, ( mood, ))

        moods = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            mood = Mood(row['id'], row['concept'], row['mood'], row['mood'] , row['date'])
            moods.append(mood.__dict__)

    return json.dumps(moods)
