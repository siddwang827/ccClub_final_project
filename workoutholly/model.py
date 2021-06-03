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
    weight = db.Column(db.String(5), nullable=False)
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
    weight = db.Column(db.String(5), nullable=False)
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

# jinja2 web HTML參數定義
class web_table():

    tabel_head = [ 'No.', '訓練動作', '訓練重量', '訓練組數', '訓練次數', '組間休息時間' ]
    weight_select = [ n * 2.5 if n < 12 else (n-6) * 5 for n in range(1, 27) ]
    sets_select = [ n for n in range(1, 9) ]
    reps_select =  [n for n in range(1, 26) ]
    rest_select = [ 15, 30, 45, 60, 90, 120, 150, 180 ]

    def __init__(self, position):
        self.position = position
    
    def choose_exercises(self, position):
        chest_exercises = [ '槓鈴臥推', '史密斯上胸', '啞鈴臥推', '斜板啞鈴上胸'  , '繩索夾胸', '機械下胸' ]
        back_exercises = [ '引體向上', '槓鈴划船', '坐姿下拉', '坐姿划船', '直臂下拉', '啞鈴划船' ]
        leg_exercises = [ '槓鈴深蹲', '保加利亞單腿蹲', '羅馬尼亞硬舉', '坐姿機械腿推', '股四頭前踢', '俯身勾腿' ]
        shoulder_exercises = [ '槓鈴肩推', '啞鈴肩推', '啞鈴前平舉', '啞鈴惻平舉', '臉拉', '機械反向飛鳥' ]
        arm_exercises = [ '法式彎舉', '繩索三頭下壓', '啞鈴單臂後屈伸', 'W槓二頭彎舉', '啞鈴垂式彎舉', '啞鈴斜板彎舉' ]

        if position == 'chest':
            exercises = chest_exercises[:]
            
        elif position == 'back':
            exercises = back_exercises[:]
           
        elif position =='leg':
            exercises = leg_exercises[:]
            
        elif position == 'shoulder':
            exercises = shoulder_exercises[:]
            
        elif position == 'arm':
            exercises = arm_exercises[:]

        # exercises.insert(0,'請選擇動作')
        self.exercises = exercises    

        return self.exercises     



if __name__ == "__main__":
    db.create_all()