import datetime
import sqlite3
import time
import datetime

conn = sqlite3.connect("homework2_db", check_same_thread=False)


# database-table-field-datatype

def create_table():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS database(sentence TEXT, sentiment TEXT, timestamp TEXT)')
    c.close()


def create_table_withfb():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS feedback_data(sentence TEXT, sentiment TEXT, timestamp TEXT, feedback BLOB)')
    c.close()


def add_data(line, res):
    b = [line, res]
    c = conn.cursor()
    unix = time.time()
    datestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d  %H:%M:%S'))
    b.append(datestamp)
    c.execute('INSERT INTO database(sentence,sentiment, timestamp) VALUES(?,?,?)', (line, res, datestamp))
    # c.execute('DELETE FROM database')
    conn.commit()
    return b


def add_feedbacks(a):
    c = conn.cursor()
    c.execute('INSERT INTO feedback_data(sentence,sentiment, timestamp,feedback) VALUES(?,?,?," ")', (a[0], a[1], a[2],))
    # c.execute('DELETE FROM feedback_data')
    conn.commit()
    c.close()


def add_feedback_data(fb, index):
    c = conn.cursor()
    c.execute('UPDATE feedback_data SET feedback=(?) WHERE rowid=(?)', (fb, index))
    conn.commit()
    c.close()


def read_data():
    c = conn.cursor()
    c.execute('SELECT * FROM database ORDER BY timestamp DESC')
    data = c.fetchall()
    return data


def read_fb_data():
    c = conn.cursor()
    c.execute('SELECT * FROM feedback_data ORDER BY timestamp DESC')
    data = c.fetchall()
    return data

