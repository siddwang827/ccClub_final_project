from flask_sqlalchemy import SQLAlchemy
from workoutholly import db
from datetime import datetime



# users( 使用者 )定義
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    lineuserid = db.Column(db.String(50), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 預告users與routines有關聯
    db_users_routine = db.relationship('routines', backref='users', lazy=True)
    db_users_temp_routines = db.relationship('temp_routines', backref='users', lazy=True)

    def __init__(self, lineuserid):
        self.lineuserid = lineuserid


# positions( 部位 )定義
class positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 預告positions與exercise有關連
    db_positions_exercises = db.relationship('exercises', backref='positions', lazy=True)

    def __init__(self, name):
        self.name = name


# exercise( 動作 )定義
class exercises(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 設定foreign key 
    positions_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)

    # 預告exercises與routines有關連
    db_exercises_routines = db.relationship('routines', backref='exercises', lazy=True)
    db_exercises_temp_routines = db.relationship('temp_routines', backref='exercises', lazy=True)

    def __init__(self, name):
        self.name = name


# routine( 課表 )定義
class routines(db.Model):
    __tablename__ = 'routines'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

     # 設定foreign key 
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,  weight, sets, reps, rest, exercise_id, user_id):
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.rest = rest
        self.exercise_id = exercise_id
        self.user_id = user_id

# temp_routine( 暫存課表 )定義
class temp_routines(db.Model):
    __tablename__ = 'temp_routines'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

     # 設定foreign key 
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,  weight, sets, reps, rest, exercise_id, user_id):
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.rest = rest
        self.exercise_id = exercise_id
        self.user_id = user_id


if __name__ == "__main__":
    db.create_all()