import mysql.connector

DB_CONFIG = {
    'user': '',
    'password': '',
    'database': 'cs122a'
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def print_bool(success):
    print("Success" if success else "Fail")

def print_table(rows):
    for row in rows:
        print(','.join('' if v is None else str(v) for v in row))


DDL_DROPS = [
    "DROP TABLE IF EXISTS Approval",
    "DROP TABLE IF EXISTS Host",
    "DROP TABLE IF EXISTS Slot",
    "DROP TABLE IF EXISTS Event",
    "DROP TABLE IF EXISTS OnCampus",
    "DROP TABLE IF EXISTS OffCampus",
    "DROP TABLE IF EXISTS Venue",
    "DROP TABLE IF EXISTS Organizer",
    "DROP TABLE IF EXISTS Participant",
    "DROP TABLE IF EXISTS Administrator",
    "DROP TABLE IF EXISTS User",
]

DDL_CREATES = [
    """CREATE TABLE User (
        uid INTEGER NOT NULL,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        joined DATE NOT NULL,
        PRIMARY KEY (uid)
    )""",
    """CREATE TABLE Organizer (
        uid INTEGER NOT NULL,
        department VARCHAR(100) NOT NULL,
        experience INTEGER NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )""",
    """CREATE TABLE Participant (
        uid INTEGER NOT NULL,
        type VARCHAR(255) NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )""",
    """CREATE TABLE Administrator (
        uid INTEGER NOT NULL,
        firstname VARCHAR(50) NOT NULL,
        lastname VARCHAR(50) NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )""",
    """CREATE TABLE Venue (
        vid INTEGER NOT NULL,
        street VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL,
        state CHAR(2) NOT NULL,
        zip CHAR(10) NOT NULL,
        PRIMARY KEY (vid)
    )""",
    """CREATE TABLE OnCampus (
        vid INTEGER NOT NULL,
        code VARCHAR(20) NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )""",
    """CREATE TABLE OffCampus (
        vid INTEGER NOT NULL,
        distance DECIMAL(6,2) NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )""",
    """CREATE TABLE Event (
        eid INTEGER NOT NULL,
        title VARCHAR(200) NOT NULL,
        type VARCHAR(50) NOT NULL,
        date DATETIME NOT NULL,
        uid INTEGER NOT NULL,
        PRIMARY KEY (eid),
        FOREIGN KEY (uid) REFERENCES Organizer(uid) ON DELETE CASCADE
    )""",
    """CREATE TABLE Slot (
        eid INTEGER NOT NULL,
        snum INTEGER NOT NULL,
        is_reserved INTEGER NOT NULL,
        uid INTEGER,
        PRIMARY KEY (eid, snum),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (uid) REFERENCES Participant(uid)
    )""",
    """CREATE TABLE Host (
        eid INTEGER NOT NULL,
        vid INTEGER NOT NULL,
        is_primary INTEGER NOT NULL,
        PRIMARY KEY (eid, vid),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES Venue(vid)
    )""",
    """CREATE TABLE Approval (
        uid INTEGER NOT NULL,
        vid INTEGER NOT NULL,
        valid_from DATE NOT NULL,
        valid_until DATE NOT NULL,
        PRIMARY KEY (uid, vid),
        FOREIGN KEY (uid) REFERENCES Administrator(uid),
        FOREIGN KEY (vid) REFERENCES OffCampus(vid)
    )""",
]

CSV_TABLES = [
    ('User', 'User'),
    ('Organizer', 'Organizer'),
    ('Participant', 'Participant'),
    ('Administrator', 'Administrator'),
    ('Venue', 'Venue'),
    ('OnCampus', 'OnCampus'),
    ('OffCampus', 'OffCampus'),
    ('Event', 'Event'),
    ('Slot', 'Slot'),
    ('Host', 'Host'),
    ('Approval', 'Approval'),
]
