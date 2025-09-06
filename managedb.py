from app import app, db
from sqlalchemy import text

if __name__ == '__main__':
    with app.app_context():
        db.session.execute(text("Drop TABLE user_data"))
        db.session.commit()

'''
deleting data from table
    with app.app_context():
        db.session.execute(text("Delete from calculation"))
        db.session.commit()
'''
'''
printing rows of data
    with app.app_context():
        rows = db.session.execute(text("select * from calculation")).fetchall()
        for row in rows:
            print(row)
'''