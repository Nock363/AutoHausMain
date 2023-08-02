import sqlalchemy as db

# Verbindung zur SQLite-Datenbank herstellen
engine = db.create_engine('sqlite:///Databases/sqlalchemyTest.db')

conn = engine.connect()
metadata = db.MetaData()

Student = db.Table('Student', metadata,
              db.Column('Id', db.Integer(),primary_key=True),
              db.Column('Name', db.String(255), nullable=False),
              db.Column('Major', db.String(255), default="Math"),
              db.Column('Pass', db.Boolean(), default=True)
              )

metadata.create_all(engine) 

# query = db.insert(Student).values(Id=2, Name='Matthew', Major="English2", Pass=True)
# Result = conn.execute(query)


# query = db.insert(Student)
# values_list = [{'Id':'12', 'Name':'Nisha', 'Major':"Science", 'Pass':False},
#               {'Id':'13', 'Name':'Natasha', 'Major':"Math", 'Pass':True},
#               {'Id':'14', 'Name':'Ben', 'Major':"English", 'Pass':False}]
# Result = conn.execute(query,values_list)

output = conn.execute(Student.select()).fetchall()
print(output)

