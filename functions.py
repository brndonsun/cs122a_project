import os
import csv
from db import get_conn, print_bool, print_table, DDL_DROPS, DDL_CREATES, CSV_TABLES


def cmd_import(folder):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        for stmt in DDL_DROPS:
            cursor.execute(stmt)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        for stmt in DDL_CREATES:
            cursor.execute(stmt)
        conn.commit()

        for filename, table in CSV_TABLES:
            filepath = os.path.join(folder, filename + '.csv')
            with open(filepath, 'r', newline='') as f:
                rows = list(csv.reader(f))
            if not rows:
                continue
            placeholders = ','.join(['%s'] * len(rows[0]))
            sql = f"INSERT INTO {table} VALUES ({placeholders})"
            for row in rows:
                cursor.execute(sql, [None if v == 'NULL' else v for v in row])
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_insert_admin(uid, email, username, joined, firstname, lastname):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO User (uid, username, email, joined) VALUES (%s,%s,%s,%s)",
            (uid, username, email, joined)
        )
        cursor.execute(
            "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s,%s,%s)",
            (uid, firstname, lastname)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_add_venue(eid, vid, is_primary):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        ip = 1 if is_primary else 0
        if ip == 1:
            cursor.execute(
                "SELECT COUNT(*) FROM Host WHERE eid=%s AND is_primary=1", (eid,)
            )
            if cursor.fetchone()[0] > 0:
                cursor.close()
                conn.close()
                print_bool(False)
                return
        cursor.execute(
            "INSERT INTO Host (eid, vid, is_primary) VALUES (%s,%s,%s)",
            (eid, vid, ip)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_reserve_slot(eid, snum, uid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_reserved FROM Slot WHERE eid=%s AND snum=%s", (eid, snum)
        )
        row = cursor.fetchone()
        if row is None or row[0] != 0:
            cursor.close()
            conn.close()
            print_bool(False)
            return
        cursor.execute(
            "UPDATE Slot SET is_reserved=1, uid=%s WHERE eid=%s AND snum=%s",
            (uid, eid, snum)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_cancel_reservation(eid, snum, uid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_reserved, uid FROM Slot WHERE eid=%s AND snum=%s", (eid, snum)
        )
        row = cursor.fetchone()
        if row is None or row[0] != 1 or str(row[1]) != str(uid):
            cursor.close()
            conn.close()
            print_bool(False)
            return
        cursor.execute(
            "UPDATE Slot SET is_reserved=0, uid=NULL WHERE eid=%s AND snum=%s",
            (eid, snum)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_update_event(eid, title, datetime_str):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Event SET title=%s, date=%s WHERE eid=%s",
            (title, datetime_str, eid)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            print_bool(False)
            return
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_delete_organizer(uid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM Organizer WHERE uid=%s", (uid,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            print_bool(False)
            return
        cursor.execute("DELETE FROM Organizer WHERE uid=%s", (uid,))
        conn.commit()
        cursor.close()
        conn.close()
        print_bool(True)
    except Exception:
        print_bool(False)


def cmd_available_events(date):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.date, COUNT(*) AS availableSlots
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = 0 AND e.date > %s
            GROUP BY e.eid, e.title, e.type, e.date
            ORDER BY e.date ASC, e.eid ASC
        """, (date,))
        print_table(cursor.fetchall())
        cursor.close()
        conn.close()
    except Exception:
        pass


def cmd_popular_event_types(n):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.type, COUNT(*) AS reservedCount
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = 1
            GROUP BY e.type
            HAVING COUNT(*) >= %s
            ORDER BY reservedCount DESC, e.type ASC
        """, (n,))
        print_table(cursor.fetchall())
        cursor.close()
        conn.close()
    except Exception:
        pass


def cmd_participant_schedule(uid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.date, s.snum,
                   h.vid, v.street, v.city, v.state, v.zip
            FROM Event e
            JOIN Slot s ON e.eid = s.eid AND s.uid = %s
            LEFT JOIN Host h ON e.eid = h.eid AND h.is_primary = 1
            LEFT JOIN Venue v ON h.vid = v.vid
            ORDER BY e.date ASC
        """, (uid,))
        print_table(cursor.fetchall())
        cursor.close()
        conn.close()
    except Exception:
        pass


def cmd_organizer_stats(n):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.uid, u.username, o.department, COUNT(e.eid) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            JOIN Event e ON o.uid = e.uid
            GROUP BY o.uid, u.username, o.department
            HAVING COUNT(e.eid) >= %s
            ORDER BY eventCount DESC, o.uid ASC
        """, (n,))
        print_table(cursor.fetchall())
        cursor.close()
        conn.close()
    except Exception:
        pass


def cmd_venue_events(vid):
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.date, h.is_primary
            FROM Host h
            JOIN Event e ON h.eid = e.eid
            WHERE h.vid = %s
            ORDER BY e.date ASC, e.eid ASC
        """, (vid,))
        print_table(cursor.fetchall())
        cursor.close()
        conn.close()
    except Exception:
        pass
