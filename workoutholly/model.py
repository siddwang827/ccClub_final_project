import sys
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import dynamic
sys.path.append('.')
from workoutholly import db


positionSelect= ['chest', 'back', 'leg', 'shoulder', 'arm']
chest_exercises = [ '槓鈴臥推', '史密斯上胸', '啞鈴臥推', '斜板啞鈴上胸', '繩索夾胸', '機械下胸' ]
back_exercises = [ '引體向上', '槓鈴划船', '坐姿下拉', '坐姿划船', '直臂下拉', '啞鈴划船' ]
leg_exercises = [ '槓鈴深蹲', '保加利亞單腿蹲', '羅馬尼亞硬舉', '坐姿機械腿推', '股四頭前踢', '俯身勾腿' ]
shoulder_exercises = [ '槓鈴肩推', '啞鈴肩推', '啞鈴前平舉', '啞鈴惻平舉', '繩索臉拉', '機械反向飛鳥' ]
arm_exercises = [ '法式彎舉', '繩索三頭下壓', '啞鈴單臂後屈伸', 'W槓二頭彎舉', '啞鈴垂式彎舉', '啞鈴斜板彎舉' ]
exercises_list = [chest_exercises, back_exercises, leg_exercises, shoulder_exercises, arm_exercises]

# users( 使用者 )定義
class Users(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    lineuserid = db.Column(db.String(50), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 預告users與routines有關聯
    routine = db.relationship('Routines', backref='users', lazy=True)
    temp_routines = db.relationship('Temp_routines', backref='users', lazy='select')

    def __init__(self, lineuserid):
        self.lineuserid = lineuserid


# positions( 部位 )定義
class Positions(db.Model):

    __tablename__ = 'positions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 預告positions與exercise有關連
    exercises = db.relationship('Exercises', backref='positions', lazy='select')
    routines = db.relationship('Routines', backref='positions', lazy='select')
    temp_routines = db.relationship('Temp_routines', backref='positions', lazy='select')
    def __init__(self, name):
        self.name = name


# exercise( 動作 )定義
class Exercises(db.Model):

    __tablename__ = 'exercises'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

    # 設定foreign key (position_id)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)

    # 預告exercises與routines有關連
    routines = db.relationship('Routines', backref='exercises', lazy='select')
    temp_routines = db.relationship('Temp_routines', backref='exercises', lazy='select')

    def __init__(self, name, position_id):
        self.name = name
        self.position_id = position_id


# routine( 課表 )定義
class Routines(db.Model):

    __tablename__ = 'routines'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # 設定foreign key (user_id, positions_id, exercise_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    weight = db.Column(db.String(5), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    

    def __init__(self, user_id, position_id, exercise_id, weight, sets, reps, rest):
        self.user_id = user_id
        self.position_id = position_id
        self.exercise_id = exercise_id
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.rest = rest
        
        

# temp_routine( 暫存課表 )定義
class Temp_routines(db.Model):

    __tablename__ = 'temp_routines'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # 設定foreign key (user_id, positions_id, exercise_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    weight = db.Column(db.String(5), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)


    def __init__(self, user_id, position_id, exercise_id, weight, sets, reps, rest):
        self.user_id = user_id
        self.position_id = position_id
        self.exercise_id = exercise_id
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.rest = rest


# jinja2 web HTML參數定義
class Web_format():

    tabel_head = [ 'No.', '訓練動作', '訓練重量(Kg)', '訓練組數', '訓練次數', '組間休息時間(sec)' ]
    weight_select = [ n * 2.5 if n < 12 else (n-6) * 5 for n in range(1, 27) ]
    sets_select = [ n for n in range(1, 9) ]
    reps_select =  [n for n in range(1, 26) ]
    rest_select = [ 15, 30, 45, 60, 90, 120, 150, 180 ]

    def __init__(self, position):
        self.position = position
    
    def choose_exercises(self):

        if self.position == 'chest':
            exercises = chest_exercises
            
        elif self.position == 'back':
            exercises = back_exercises
           
        elif self.position =='leg':
            exercises = leg_exercises
            
        elif self.position == 'shoulder':
            exercises = shoulder_exercises
            
        elif self.position == 'arm':
            exercises = arm_exercises

        self.exercises = exercises    

        return self.exercises     
    
    def position_translate(self):
        
        if self.position == 'chest':
            self.position = '胸部'
        
        elif self.position == 'back':
            self.position = '背部'
            
        elif self.position == 'leg':
            self.position = '腿部'
            
        elif self.position == 'shoulder':
            self.position = '肩部'
            
        elif self.position == 'arm':
            self.position = '手臂'

        return self.position


class Add_fondation_element():

    def __init__(self) -> None:
        pass

    def add_positions(self, position_list):
        
        for pos in position_list:
            p = Positions(pos)
            db.session.add(p)
        db.session.commit()

    def add_exercises(self, position, exercise_list):

        if position == 'chest':
            for exe in exercise_list[0]:
                e = Exercises(exe, position_id=1)
                db.session.add(e)
        elif position == 'back':
            for exe in exercise_list[1]:
                e = Exercises(exe, position_id=2)
                db.session.add(e)
        elif position == 'leg':
            for exe in exercise_list[2]:
                e = Exercises(exe, position_id=3)
                db.session.add(e)
        elif position == 'shoulder':
            for exe in exercise_list[3]:
                e = Exercises(exe, position_id=4)
                db.session.add(e)
        elif position == 'arm':
            for exe in exercise_list[4]:
                e = Exercises(exe, position_id=5)
                db.session.add(e)
        
        db.session.commit()


class RoutineAction():

    def __init__(self) -> None:
        pass

    def Add_routines_to_db(self, check_exercises, check_exercises_dict, user_db, position_db):

        for num in range(len(check_exercises)):
            exercisedata = Exercises.query.filter_by(name=check_exercises[num]).first()
            routine = Routines(
                user_db.id,
                position_db.id, 
                exercisedata.id, 
                check_exercises_dict[check_exercises[num]][0], 
                check_exercises_dict[check_exercises[num]][1], 
                check_exercises_dict[check_exercises[num]][2], 
                check_exercises_dict[check_exercises[num]][3]
                )
            db.session.add(routine)
            db.session.commit()


    def get_routine(self, position_name, lineuserid):

        tableColumn = Web_format.tabel_head[1:] 
        
        # 從db獲取該user欲查詢該部位課表的所有exercise name
        routines_query = Routines.query.join(Positions, Users).filter((Positions.name == position_name) & (Users.lineuserid == lineuserid)).all()
        print(routines_query)

        if not routines_query:
            return pd.DataFrame()

        exercise = {tableColumn[0]:[i.exercises.name for i in routines_query]}

        # 從db獲取user欲查詢部位的課表並轉換為dataframe
        routines_statement = Routines.query.join(Positions, Users).filter((Positions.name == position_name) & (Users.lineuserid == lineuserid)).statement
        routine_df = pd.read_sql(routines_statement, db.engine)

        # 刪除多餘欄位
        del routine_df['id'], routine_df['user_id'], routine_df['position_id'], routine_df['create_time']
        
        # 修改dataframe的column名稱, 調整index, 並把exercise_id置換為name
        routine_df.columns = tableColumn
        routine_df.index += 1
        routine_df['訓練動作'] = exercise[tableColumn[0]]

        return routine_df


    def Create_temp_routines(self, position_name, lineuserid):

        query = Routines.query.join(Positions, Users).filter((Positions.name == position_name) & (Users.lineuserid == lineuserid)).first()

        if not query:

            return None

        try:
            user_db = Users.query.filter_by(lineuserid=lineuserid).first()
            position_db = Positions.query.filter_by(name=position_name).first()
            #清除user的暫存課表 
            Temp_routines.query.filter_by(position_id=position_db.id).filter_by(user_id= user_db.id).delete() 
            db.session.commit() 
                       
        except:
            pass

        finally:

            # 從user的課表複製一份到temp_routine
            sql = f'''

                INSERT INTO orm_test.temp_routines (`user_id`, `position_id`, `exercise_id`, `weight`, `sets`, `reps`, `rest`)
                SELECT `user_id`, `position_id`, `exercise_id`, `weight`, `sets`, `reps`, `rest` 
                FROM orm_test.routines
                WHERE user_id = {query.users.id} AND position_id = {query.positions.id};

            '''

            db.engine.execute(sql)
            db.session.commit()
            return 'OK'


    def get_routine_hint(self, position_name, lineuserid):

        user_db = Users.query.filter_by(lineuserid=lineuserid).first()
        position_db = Positions.query.filter_by(name=position_name).first()

        # 從db獲取該user欲查詢部位的暫時課表的第一個動作名稱
        temp_routines_query = Temp_routines.query.filter_by(position_id=position_db.id).filter_by(user_id= user_db.id).first()     



        # 從db獲取user暫時課表轉換為dataframe
        temp_routines_statement = Temp_routines.query.filter_by(position_id=position_db.id).filter_by(user_id= user_db.id).statement
        temp_routine_df = pd.read_sql(temp_routines_statement, db.engine)

        # 刪除多餘欄位
        del temp_routine_df['id'], temp_routine_df['user_id'], temp_routine_df['position_id'], temp_routine_df['create_time']
        
        # 修改dataframe的column名稱, 調整index, 並把exercise_id置換為name
        tableColumn = Web_format.tabel_head[1:]
        exercise = {tableColumn[0]: temp_routines_query.exercises.name }
        temp_routine_df.columns = tableColumn
        temp_routine_df.index += 1
        temp_routine_df = temp_routine_df[0:1]
        temp_routine_df['訓練動作'] = exercise[tableColumn[0]]

        return temp_routine_df

    def next_exercise_hint(self, lineuserid):

        user_db = Users.query.filter_by(lineuserid=lineuserid).first()


        
        try :
            # 從db獲取該user暫時課表的刪除上一個動作
            temp_routines_query = Temp_routines.query.filter_by(user_id= user_db.id).first()
            db.session.delete(temp_routines_query)
            db.session.commit()

            temp_routines_query = Temp_routines.query.filter_by(user_id= user_db.id).first()

            # 從db獲取user暫時課表轉換為dataframe
            temp_routines_statement = Temp_routines.query.filter_by(user_id= user_db.id).statement
            temp_routine_df = pd.read_sql(temp_routines_statement, db.engine)


            # 刪除多餘欄位
            del temp_routine_df['id'], temp_routine_df['user_id'], temp_routine_df['position_id'], temp_routine_df['create_time']

            
            # 修改dataframe的column名稱, 調整index, 並把exercise_id置換為name
            tableColumn = Web_format.tabel_head[1:]
            exercise = {tableColumn[0]: temp_routines_query.exercises.name }
            temp_routine_df.columns = tableColumn
            temp_routine_df.index += 1
            temp_routine_df = temp_routine_df[0:1]
            temp_routine_df['訓練動作'] = exercise[tableColumn[0]]

            position_name = temp_routines_query.positions.name
            

            return [temp_routine_df, position_name]
        
        except:
            
            #刪除報錯回傳none
            return None




# if __name__ == "__main__":
#     db.drop_all()
#     db.create_all()
    
#     foundation = Add_fondation_element()
#     foundation.add_positions(positionSelect)

#     for pos in positionSelect:
#         foundation.add_exercises(pos, exercises_list)
    
#     sql = '''
#         ALTER TABLE `orm_test`.`temp_routines` 
#         CHANGE COLUMN `create_time` `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ;
#     ''' 
#     db.engine.execute(sql)
    

   
# position_name = 'chest'
# lineuserid = 'U10aeabde734bf2b26f04844b5f930329'

# routines_query =Temp_routines.query.filter_by(position_id=position_db.id).filter_by(user_id= user_db.id).first()
        
# if not routines_query:
#     print('沒東西')

# # 從db獲取user欲查詢部位的課表並轉換為dataframe
# routines_statement = Temp_routines.query.join(Positions, Users).filter((Positions.name == position_name) & (Users.lineuserid == lineuserid)).statement
# routine_df = pd.read_sql(routines_statement, db.engine)

# print(routine_df)

# # 刪除多餘欄位
# del routine_df['id'], routine_df['user_id'], routine_df['position_id'], routine_df['create_time']

# # 修改dataframe的column名稱, 調整index, 並把exercise_id置換為name
# tableColumn = Web_format.tabel_head[1:]
# exercise = {tableColumn[0]: routines_query.exercises.name }
# routine_df.columns = tableColumn
# routine_df.index += 1
# routine_df['訓練動作'] = exercise[tableColumn[0]]
# routine_df = routine_df[0:1]
# print(routine_df)


