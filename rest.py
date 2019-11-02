#! /usr/bin/python3

import cgi
import cgitb
import os
import json
import MySQLdb
import passwords

def html_form():
        info = os.environ['PATH_INFO']
        print("Content-Type: text/html")
        print("Status: 200 OK")
        print()
        print('''<html>
                <title>test</title>
                <body>
                        {} Not found. Add to the roster using the form.<br>
                        <form action="/cgi-bin/rest.py/roster" method="POST">
                                Name: <input type="text" name="name" required><br>
                                Class: <input type="text" name="class" required><br>
                                Age: <input type="number" name="age"><br>
                                <input type="submit">
                        </form>
                </body>
        </html>'''.format(info))

def roster():
        conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db = "animus")
        cursor = conn.cursor()
        form = cgi.FieldStorage()
        if os.environ['REQUEST_METHOD'] == "POST":
                if "age" in form:
                        cursor.execute("INSERT INTO roster(name, class, age) VALUES (%s, %s, %s);", (form["name"].value, form["class"].value, form["age"].value))
                else:
                        cursor.execute("INSERT INTO roster(name, class) VALUES (%s, %s);", (form["name"].value, form["class"].value))
                new_id = cursor.lastrowid
                cursor.close()
                conn.commit()
                print("Status: 302 Redirect")
                print("Location: roster/" + str(new_id))
                print()
        else:
                if os.environ['PATH_INFO'] == "/roster":
                        cursor.execute("SELECT * FROM roster;")
                else:
                        cursor.execute("SELECT * FROM roster WHERE ID=%s;", (os.environ['PATH_INFO'][8:],))
                results = cursor.fetchall()
                cursor.close()
                output = []
                for unit in results:
                        info = {}
                        info["ID"] = unit[0]
                        info["Name"] = unit[1]
                        info["Class"] = unit[2]
                        info["Age"] = unit[3]
                        output.append(info)
                print("Content-Type: application/json")
                print("Status: 200 OK")
                print()
                print(json.dumps(output))

cgitb.enable()
if 'PATH_INFO' in os.environ:
        if os.environ['PATH_INFO'] == "/json":
                print("Content-Type: application/json")
                print("Status: 200 OK")
                print()
                print(json.dumps([1, 1, 2, 3, 5, {"Sequence": "Fibonacci"}, os.environ['REQUEST_METHOD']]))
        elif os.environ['PATH_INFO'][0:7] == "/roster":
                roster()
        else:
                html_form()
else:
        print("Status: 302 Redirect")
        print("Location: rest.py/json")
        print()


