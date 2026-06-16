import sqlite3
import hashlib

DB_PATH = "database/zoo.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            species  TEXT NOT NULL,
            habitat  TEXT,
            diet     TEXT,
            status   TEXT DEFAULT 'Stabil',
            age      INTEGER DEFAULT 0,
            weight   REAL DEFAULT 0.0,
            origin   TEXT,
            notes    TEXT,
            image    BLOB
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    
    # Seed with sample data if empty
    c.execute("SELECT COUNT(*) FROM animals")
    if c.fetchone()[0] == 0:
        samples = [
            ("Singa Afrika", "Panthera leo", "Sabana", "Karnivora", "Baik", 5, 190.0, "Afrika", "Raja hutan yang gagah", None),
            ("Gajah Sumatera", "Elephas maximus sumatranus", "Hutan Tropis", "Herbivora", "Kritis", 12, 2700.0, "Sumatera", "Spesies terancam punah", None),
            ("Komodo", "Varanus komodoensis", "Pulau Kering", "Karnivora", "Rentan", 8, 70.0, "NTT", "Kadal terbesar di dunia", None),
            ("Harimau Benggala", "Panthera tigris tigris", "Hutan Hujan", "Karnivora", "Terancam", 6, 220.0, "India", "Kucing besar yang majestic", None),
            ("Jerapah", "Giraffa camelopardalis", "Sabana", "Herbivora", "Baik", 9, 800.0, "Afrika", "Hewan darat tertinggi", None),
            ("Orang Utan", "Pongo pygmaeus", "Hutan Hujan", "Omnivora", "Kritis", 15, 85.0, "Kalimantan", "Primata cerdas dari Borneo", None),
        ]
        c.executemany("""
            INSERT INTO animals (name,species,habitat,diet,status,age,weight,origin,notes,image)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, samples)
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,name,species,habitat,diet,status,age,weight,origin,notes,image FROM animals ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_one(animal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM animals WHERE id=?", (animal_id,))
    row = c.fetchone()
    conn.close()
    return row

def insert_animal(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO animals (name,species,habitat,diet,status,age,weight,origin,notes,image)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, data)
    conn.commit()
    conn.close()

def update_animal(animal_id, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE animals SET name=?,species=?,habitat=?,diet=?,status=?,age=?,weight=?,origin=?,notes=?,image=?
        WHERE id=?
    """, (*data, animal_id))
    conn.commit()
    conn.close()

def delete_animal(animal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM animals WHERE id=?", (animal_id,))
    conn.commit()
    conn.close()

def search_animals(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    like = f"%{query}%"
    c.execute("""
        SELECT id,name,species,habitat,diet,status,age,weight,origin,notes,image
        FROM animals
        WHERE name LIKE ? OR species LIKE ? OR habitat LIKE ? OR origin LIKE ?
        ORDER BY id DESC
    """, (like, like, like, like))
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_status_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM animals GROUP BY status")
    rows = c.fetchall()
    conn.close()
    return {status: count for status, count in rows}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # Username already exists
    conn.close()
    return success

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False
