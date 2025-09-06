from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
db = SQLAlchemy(app)
id_count = 0


def updateID_Count():
    global id_count
    id_count += 1


class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(100))
    result = db.Column(db.String(100))


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


@app.route('/clear', methods=['POST'])
def clear_data():
    db.session.execute(text("DELETE FROM calculation"))
    db.session.commit()
    return jsonify({'status': 'cleared'})


@app.route('/add_column', methods=["POST"])
def add_column():
    data = request.get_json()
    column_name = data.get("column")
    datatype = data['type']
    if datatype == 'String':
        datatype = 'VARCHAR(255)'
    elif datatype == 'Integer':
        datatype = 'INT'
    elif datatype == 'Float':
        datatype = 'FLOAT'
    elif datatype == 'Boolean':
        datatype = 'BOOLEAN'
    try:
        db.session.execute(text(f'ALTER TABLE user_data ADD COLUMN "{column_name}" {datatype}'))
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_rows', methods=['POST'])
def get_rows():
    try:
        data = request.get_json()
        column_name = data.get("column")
        result = db.session.execute(text(f'SELECT "{column_name}" FROM user_data '))
        values = []
        for row in result:
            values.append(row[0])
        return jsonify(values)
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_row')
def get_row():
    try:
        result = db.session.execute(text(f'SELECT * FROM user_data'))
        values = []
        for row in result:
            values.append(list(row))
        return jsonify(values)
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/get_columns')
def get_columns():
    try:
        inspector = inspect(db.engine)
        columns = inspector.get_columns('user_data')
        column_names = []
        for col in columns:
            column_names.append(col['name'])

        return jsonify(column_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_row', methods=["POST"])
def update_row():
    data = request.get_json()
    column_name = data.get("column")
    row_name = data.get('row')
    new_val = data.get('value')

    if row_name is None:
        query = text(f'UPDATE user_data SET "{column_name}" = :new_value WHERE "{column_name}" IS NULL')
        db.session.execute(query, {"new_value": new_val})
    else:
        query = text(f'UPDATE user_data SET "{column_name}" = :new_value WHERE "{column_name}" = :row_name')
        db.session.execute(query, {"new_value": new_val, "row_name": row_name})
    db.session.commit()
    return jsonify({"status": "success"})


@app.route('/insert_data', methods=["POST"])
def insert_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    try:
        columns = [col for col in data.keys() if col.lower() != "id"]
        values = [data[col] for col in columns]
        placeholders = [f":val{i}" for i in range(len(columns))]
        value_dict = {f"val{i}": val for i, val in enumerate(values)}
        columns_sql = ", ".join(f'"{col}"' for col in columns)
        placeholders_sql = ", ".join(placeholders)

        db.session.execute(
            text(f'INSERT INTO user_data ({columns_sql}) VALUES ({placeholders_sql})'),
            value_dict
        )
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/remove_column', methods=["POST"])
def remove_column():
    data = request.get_json()
    column_name = data.get("column")
    inspector = inspect(db.engine)
    columns = inspector.get_columns('user_data')
    column_names = [col['name'] for col in columns]
    if column_name == "id":
        return jsonify({"status": "error", "message": "cannot remove id column"})
    if column_name not in column_names:
        return jsonify({"status": "error", "message": "Column does not exist"})
    try:
        new_columns = []
        for col in columns:
            if col['name'] != column_name:
                name = col['name']
                col_type = str(col['type']).upper()
                if name == "id":
                    new_columns.append((name, "INTEGER PRIMARY KEY AUTOINCREMENT"))
                else:
                    new_columns.append((name, col_type))

        column_defs = []
        for col in new_columns:
            column_def = f'"{col[0]}" {col[1]}'
            column_defs.append(column_def)

        columns_sql = ", ".join(column_defs)
        column_list = []
        for col in new_columns:
            column_list.append(f'"{col[0]}"')

        copy_columns = ""
        for i in range(len(column_list)):
            copy_columns += column_list[i]
            if i < len(column_list) - 1:
                copy_columns += ", "

        db.session.execute(text(f"""Create TABLE user_data_temp ({columns_sql})"""))
        db.session.execute(text(f"""INSERT INTO user_data_temp ({copy_columns}) Select {copy_columns} 
        FROM user_data """))

        db.session.execute(text("DROP TABLE user_data"))
        db.session.execute(text("ALTER TABLE user_data_temp RENAME TO user_data"))
        db.session.commit()
        return jsonify({"status": "success"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/cleardb', methods=['POST'])
def cleardb():
    db.session.execute(text(f'DELETE FROM user_data'))
    db.session.execute(text("DELETE FROM sqlite_sequence WHERE name='user_data'"))
    db.session.commit()
    return jsonify({"status": "success"})


@app.route('/checktype', methods=['POST'])
def checktype():
    data = request.get_json()
    column_name = data.get('column')
    try:
        query = text("PRAGMA table_info(user_data)")
        result = db.session.execute(query)
        rows = result.fetchall()

        for row in rows:
            if row[1] == column_name:
                print(str(row[2]))
                return jsonify(str(row[2]))

    except Exception as e:
        db.session.rollback()
        print("DEBUG ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/history')
def get_history():
    results = (Calculation.query.order_by(Calculation.id.desc()).limit(10).all())
    return jsonify([
        {"expression": c.expression, "result": c.result}
        for c in results
    ])


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    expr = data.get('expression')
    result = data.get('result')

    calc = Calculation(expression=expr, result=str(result))
    db.session.add(calc)
    db.session.commit()

    return jsonify({'status': 'saved', 'expression': expr, 'result': result})


@app.route('/menu')
def menu():
    return render_template('Menu.html')


'''
Menu
URL: http://localhost:5000/menu
loads: templates/Menu.html
'''


@app.route('/calculator')
def calculator():
    return render_template('Calculator.html')


'''
Calculator
URL: http://localhost:5000/calculator
loads: templates/Calculator.html
'''


@app.route('/database')
def database():
    return render_template('DataBase.html')


'''
DataBase
URL: http://localhost:5000/database
loads: templates/DataBase/DataBase.html
'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    webbrowser.open_new("http://localhost:5000/menu")
    app.run(debug=True, use_reloader=False)
