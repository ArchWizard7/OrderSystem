from flask import Flask, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random

app = Flask(__name__)

# SET APP SECRET KEY
app.secret_key = "0123456789abcdef0123456789abcdef"
print(f"APP SECRET KEY: \u001b[31m{app.secret_key}\u001b[0m")

# DBはMySQLを使う
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:BTcfrLkK1FFU@localhost:3306/mconlinejudge"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = input("Input MYSQL Password: ")
app.config["MYSQL_PASSWORD"] = "BTcfrLkK1FFU"
app.config["MYSQL_DB"] = "order_system"

mysql = MySQL(app)


# カンマ区切りフィルタを定義
def comma_format(value):
    return "{:,}".format(value)


# テンプレートにフィルタを追加
app.jinja_env.filters['comma_format'] = comma_format


@app.route("/")
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM items;")
    items = cursor.fetchall()

    return render_template("index.html", items=items)


@app.route("/get-time")
def get_time():
    now = datetime.now()
    return str(now.strftime("%Y/%m/%d %H:%M:%S"))


@app.route("/confirm", methods=["POST"])
def confirm():
    data = []
    total = 0

    form = request.form

    print("request.form =", form)

    for key in form:
        if len(request.form[key]) > 0:
            count = int(request.form[key])

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM items WHERE name = '{key}';")
            item = cursor.fetchone()
            item["count"] = count

            data.append(item)

            total += item["price"] * count

    if total <= 0:
        return render_template("error.html", status=400, msg="個数が無効です")
    else:
        return render_template("confirm.html", data=data, total=total)


@app.route("/purchase", methods=["POST"])
def purchase():
    order_id = random.randint(1, 9999)
    now = datetime.now()
    str_datetime = str(now.strftime("%Y-%m-%d %H:%M:%S"))

    form = request.form

    print("form =", form)

    for key in form:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM items WHERE name = '{key}';")

        item = cursor.fetchone()
        name = item["name"]
        count = form[key]

        print(f"INSERT INTO orders (order_id, name, count, date, is_offered) VALUES ('{order_id}', '{name}', '{count}', '{str_datetime}', '{0}');")
        cursor.execute(f"INSERT INTO orders (order_id, name, count, date, is_offered) VALUES ('{order_id}', '{name}', '{count}', '{str_datetime}', '{0}');")

    mysql.connection.commit()

    return render_template("purchase.html", order_id=order_id)


@app.route("/staff-room")
def staff_room():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM orders WHERE is_offered = 0;")

    items = cursor.fetchall()

    return render_template("staff-room.html", items=items)


@app.route("/order-complete")
def order_complete():
    args = request.args
    unique_id = args.get("id")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"UPDATE orders SET is_offered = 1 WHERE id = {unique_id};")
    mysql.connection.commit()

    cursor.execute(f"SELECT * FROM orders WHERE is_offered = 0;")

    items = cursor.fetchall()

    return render_template("staff-room.html", items=items)


@app.route("/history")
def history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM orders;")

    items = cursor.fetchall()

    return render_template("history.html", items=items)


@app.route("/route")
def route():
    return render_template("route.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
