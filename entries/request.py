import sqlite3
import json
import datetime
from models import Entry, Mood, Tag


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label entry_mood
        from Entries e
        join Moods m
            on m.id = e.mood_id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            entry = Entry(
                row['id'], 
                row['concept'], 
                row['entry'], 
                row['mood_id'], 
                row['date'], 
            )

            mood = Mood(row['mood_id'], row['entry_mood'])

            db_cursor.execute("""
            select t.id, t.name
            from Entries e
            join Entrytag et on e.id = et.entry_id
            join Tags t on t.id = et.tag_id
            where e.id = ?
            """, (entry.id, ))

            tag_set = db_cursor.fetchall()
            for tag_data in tag_set:
                tag = Tag(tag_data['id'], tag_data['name'])
                entry.tags.append(tag.__dict__)

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


# Function with a single parameter
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label entry_mood
        from Entries e
        join Moods m
            on m.id = e.mood_id
        where e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

          # Create an entry instance from the current data
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['mood_id'], data['date'])

        db_cursor.execute("""
            select t.id, t.name
            from Entries e
            join Entrytag et on e.id = et.entry_id
            join Tags t on t.id = et.tag_id
            where e.id = ?
            """, ( id, ))


        tag_set = db_cursor.fetchall()
        for tag_data in tag_set:
            tag = Tag(tag_data['id'], tag_data['name'])
            entry.tags.append(tag.id)


        mood = Mood(data['mood_id'], data['entry_mood'])
      
        entry.mood = mood.__dict__
        return json.dumps(entry.__dict__)

def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        insert into Entries
            ( concept, entry, date, mood_id )
        values
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], datetime.datetime.now(), new_entry['moodId'] ))


        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id

        
        for tag in new_entry['tags']:
            db_cursor.execute("""
                insert into EntryTag
                (entry_id, tag_id)
                values (?, ?)
                """, (id, tag))

        return json.dumps(new_entry)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))


def get_entries_by_search_term(search_term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        from entries e
        WHERE e.concept like ?
        """, ( f'%{search_term}%', ))

        searched_entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'] , row['date'])
            searched_entries.append(entry.__dict__)

    return json.dumps(searched_entries)

def update_entry(id, updated_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        update Entries
            set
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        where id = ?
        """, (updated_entry['concept'], updated_entry['entry'],
              updated_entry['moodId'], updated_entry['date'], id ))

        
        for tag in updated_entry['tags']:
            db_cursor.execute("""
                insert into EntryTag
                (entry_id, tag_id)
                values (?, ?)
                """, (id, tag))
        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True