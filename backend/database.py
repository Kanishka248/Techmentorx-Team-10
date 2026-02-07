import sqlite3

# Connect to the database
def get_connection():
    conn = sqlite3.connect("social_mentor.db")
    return conn

# Create all tables
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =======================
    # USERS TABLE
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        location TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('Donor', 'Volunteer', 'Admin')),
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        points INTEGER DEFAULT 0
    )
    """)

    # =======================
    # DONATIONS TABLE
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('Food', 'Clothes', 'Toys', 'Essentials')),
        quantity INTEGER NOT NULL,
        location TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL CHECK(status IN ('Available', 'Picked up', 'Delivered', 'Received')) DEFAULT 'Available',
        volunteer_id INTEGER,
        FOREIGN KEY(donor_id) REFERENCES users(id),
        FOREIGN KEY(volunteer_id) REFERENCES users(id)
    )
    """)

    # =======================
    # VOLUNTEER TASKS TABLE
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteer_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volunteer_id INTEGER NOT NULL,
        donation_id INTEGER NOT NULL,
        task_status TEXT NOT NULL CHECK(task_status IN ('Assigned', 'Picked up', 'Delivered')) DEFAULT 'Assigned',
        assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        picked_up_at DATETIME,
        delivered_at DATETIME,
        FOREIGN KEY(volunteer_id) REFERENCES users(id),
        FOREIGN KEY(donation_id) REFERENCES donations(id)
    )
    """)

    # =======================
    # POINTS / REWARDS TABLE
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volunteer_id INTEGER NOT NULL,
        donation_id INTEGER,
        points_awarded INTEGER NOT NULL,
        awarded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(volunteer_id) REFERENCES users(id),
        FOREIGN KEY(donation_id) REFERENCES donations(id)
    )
    """)

    # =======================
    # ACTIVITY LOG TABLE
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        performed_by INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(donation_id) REFERENCES donations(id),
        FOREIGN KEY(performed_by) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
    print("All tables created successfully!")

if __name__ == "__main__":
    create_tables()
