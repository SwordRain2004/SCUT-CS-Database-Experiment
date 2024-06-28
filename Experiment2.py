import sys
import sqlite3
import datetime
import PyQt5
from PyQt5 import QtWidgets, QtCore
today = datetime.datetime.today()
userID, userChar, db = "", "", sqlite3.connect('Database.db')
specific_character = ['\\', '/', ':', '?', "\"", "\'", "<", ">", "|"]
def Initialize_Database():
    global db
    cursor = db.cursor()
    # ---------------------------------Create Tables---------------------------------
    # Create Students Table
    cursor.execute('''DROP TABLE IF EXISTS Students;''')
    cursor.execute('''
        
        CREATE TABLE IF NOT EXISTS Students (
            StudentID TEXT PRIMARY KEY CHECK(length(StudentID) = 10),
            StudentName TEXT NOT NULL,
            Sex TEXT CHECK(Sex IN ('male', 'female')),
            EntranceAge INTEGER CHECK(EntranceAge BETWEEN 10 AND 50),
            EntranceYear INTEGER NOT NULL,
            Class TEXT NOT NULL
        )
        ''')
    # Create Course Table
    cursor.execute('''DROP TABLE IF EXISTS Courses;''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            CourseID TEXT PRIMARY KEY CHECK(length(CourseID) = 7),
            CourseName TEXT NOT NULL,
            TeacherID TEXT NOT NULL CHECK(length(TeacherID) = 5),
            Credit REAL NOT NULL,
            Grade INTEGER NOT NULL,
            CanceledYear INTEGER,
            FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
        )
        ''')
    # Create Teacher Table
    cursor.execute('''DROP TABLE IF EXISTS Teachers;''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            TeacherID TEXT PRIMARY KEY CHECK(length(TeacherID) = 5),
            TeacherName TEXT NOT NULL
        )
        ''')
    # Create Course Choosing Table
    cursor.execute('''DROP TABLE IF EXISTS CourseChoosing;''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CourseChoosing (
            StudentID TEXT NOT NULL CHECK(length(StudentID) = 10),
            CourseID TEXT NOT NULL CHECK(length(CourseID) = 7),
            TeacherID TEXT NOT NULL CHECK(length(TeacherID) = 5),
            ChosenYear INTEGER NOT NULL,
            Score REAL,
            PRIMARY KEY (StudentID, CourseID, TeacherID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
            FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
        )
        ''')
    # Create Account and Password Table
    cursor.execute('''DROP TABLE IF EXISTS AccountPassword;''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AccountPassword (
            Account TEXT PRIMARY KEY,
            Occupation TEXT CHECK(Occupation IN ('student', 'teacher', 'admin')),
            Password TEXT NOT NULL,
            CHECK((Occupation = 'student' AND length(Account) = 10) OR 
                  (Occupation = 'teacher' AND length(Account) = 5) OR 
                  (Occupation = 'admin'))
        )
        ''')
    # ----------------------------------Insert Data----------------------------------
    # Insert Student Data
    students = [
        ('2022000001', 'Alice', 'female', 18, 2022, 'Class 1'),
        ('2022000002', 'Jack', 'male', 19, 2022, 'Class 1'),
        ('2022000003', 'Rose', 'female', 18, 2022, 'Class 1'),
        ('2021000001', 'Bob', 'male', 20, 2021, 'Class 2'),
        ('2020000001', 'Charlie', 'male', 22, 2020, 'Class 3')
    ]

    cursor.executemany('''
        INSERT INTO Students (StudentID, StudentName, Sex, EntranceAge, EntranceYear, Class)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', students)
    # Insert Course Data
    courses = [
        ('0000001', 'Mathematical analysis', '00001', 4, 1, None),
        ('0000002', 'Python Program', '00002', 3, 1, None),
        ('0000003', 'C++ Program', '00003', 2, 2, 2023)
    ]

    cursor.executemany('''
        INSERT INTO Courses (CourseID, CourseName, TeacherID, Credit, Grade, CanceledYear)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', courses)
    # Insert Teacher Data
    teachers = [
        ('00001', 'Smith'),
        ('00002', 'Johnson'),
        ('00003', 'Williams')
    ]

    cursor.executemany('''
        INSERT INTO Teachers (TeacherID, TeacherName)
        VALUES (?, ?)
        ''', teachers)
    # Insert Course Choosing Data
    course_choosing = [
        ('2020000001', '0000001', '00001', 2022, 78.0),
        ('2020000001', '0000002', '00002', 2021, 100.0),
        ('2020000001', '0000003', '00003', 2020, 60.0),
        ('2021000001', '0000002', '00002', 2022, 90.0),
        ('2021000001', '0000003', '00003', 2021, 99.0),
        ('2022000001', '0000003', '00003', 2022, 95.0),
        ('2022000002', '0000003', '00003', 2022, 88.5),
        ('2022000003', '0000003', '00003', 2022, 78.0)
    ]

    cursor.executemany('''
        INSERT INTO CourseChoosing (StudentID, CourseID, TeacherID, ChosenYear, Score)
        VALUES (?, ?, ?, ?, ?)
        ''', course_choosing)
    # Insert Account and Password Data
    account_passwords = [
        ('2020000001', 'student', '123456'),
        ('2021000001', 'student', '123456'),
        ('2022000001', 'student', '123456'),
        ('2022000002', 'student', '123456'),
        ('2022000003', 'student', '123456'),
        ('00001', 'teacher', '123456'),
        ('00002', 'teacher', '123456'),
        ('00003', 'teacher', '123456'),
        ('00000', 'admin', '123456')
    ]
    cursor.executemany('''
        INSERT INTO AccountPassword (Account, Occupation, Password)
        VALUES (?, ?, ?)
        ''', account_passwords)
    db.commit()
class Login_Ui(QtWidgets.QWidget):
    getID = "test"
    admin_window = PyQt5.QtCore.pyqtSignal()
    teacher_window = PyQt5.QtCore.pyqtSignal()
    student_window = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(500, 300)
        self.label_Welcome = QtWidgets.QLabel(Form)
        self.label_Welcome.setGeometry(PyQt5.QtCore.QRect(125, 30, 300, 51))
        self.label_Welcome.setLayoutDirection(PyQt5.QtCore.Qt.LeftToRight)
        self.label_Welcome.setWordWrap(True)
        self.label_Welcome.setObjectName("label_3")
        self.label_User_ID = QtWidgets.QLabel(Form)
        self.label_User_ID.setGeometry(PyQt5.QtCore.QRect(98, 93, 70, 40))
        self.label_User_ID.setObjectName("label")
        self.label_Password = QtWidgets.QLabel(Form)
        self.label_Password.setGeometry(PyQt5.QtCore.QRect(95, 130, 71, 20))
        self.label_Password.setObjectName("label_2")
        self.label_Invalid_Login_Error = QtWidgets.QLabel(Form)
        self.label_Invalid_Login_Error.setGeometry(PyQt5.QtCore.QRect(95, 195, 300, 51))
        self.label_Invalid_Login_Error.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Invalid_Login_Error.setVisible(False)
        self.label_Invalid_Login_Error.setWordWrap(True)
        self.label_Invalid_Login_Error.setObjectName("label_4")
        self.label_Invalid_Login_Error.setStyleSheet("color: rgb(250, 0, 0);")
        self.label_Author = QtWidgets.QLabel(Form)
        self.label_Author.setGeometry(PyQt5.QtCore.QRect(0, 240, 500, 50))
        self.label_Author.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Author.setObjectName("label_4")

        self.User_ID_Input = QtWidgets.QLineEdit(Form)
        self.User_ID_Input.setGeometry(PyQt5.QtCore.QRect(170, 100, 200, 20))
        self.User_ID_Input.setObjectName("lineEdit")
        self.Password_Input = QtWidgets.QLineEdit(Form)
        self.Password_Input.setGeometry(PyQt5.QtCore.QRect(170, 130, 200, 20))
        self.Password_Input.setObjectName("lineEdit_2")

        self.Button_login = QtWidgets.QPushButton(Form)
        self.Button_login.setGeometry(PyQt5.QtCore.QRect(200, 160, 75, 24))
        self.Button_login.setObjectName("pushButton")
        self.Button_login.clicked.connect(self.login_check)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def login_check(self):
        global db
        global userID
        global userChar
        getID = self.User_ID_Input.text()
        if not getID.isdigit():
            self.label_Invalid_Login_Error.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "User ID must be a decimal number\n   please try again"))
            self.label_Invalid_Login_Error.setVisible(True)
            return
        getPW = self.Password_Input.text()
        cursor = db.cursor()
        if getPW != "":
            for i in getPW:
                if i in specific_character:
                    self.label_Invalid_Login_Error.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Password should not contain \\, /, :, ?, \", \', <, >, |"))
                    self.label_Invalid_Login_Error.setVisible(True)
                    return
            sql = f"select * from AccountPassword where Account=\'{getID}\';"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) > 0 and str(results[0][2]) == getPW:
                userID = getID
                char = results[0][1]
                userChar = char
                if char == "admin":
                    self.admin_window.emit()
                elif char == "teacher":
                    self.teacher_window.emit()
                elif char == "student":
                    self.student_window.emit()
            else:
                self.label_Invalid_Login_Error.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "User ID or Password incorrect please try again"))
                self.label_Invalid_Login_Error.setVisible(True)
        else:
            self.label_Invalid_Login_Error.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Password should not be empty"))
            self.label_Invalid_Login_Error.setVisible(True)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login"))
        self.Button_login.setText(_translate("Form", "Login"))
        self.label_User_ID.setText(_translate("Form", "User ID"))
        self.label_Password.setText(_translate("Form", "Password"))
        self.label_Welcome.setText(_translate("Form", "Welcome to MIS for Computer\n  Science college of SCUT"))
        self.label_Invalid_Login_Error.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "User ID or Password incorrect please try again"))
        self.label_Author.setText(_translate("Form", "作者：计算机科学与技术(全英创新班) 某学生"))
class Student_Ui(QtWidgets.QWidget):
    logout = PyQt5.QtCore.pyqtSignal()
    query = PyQt5.QtCore.pyqtSignal()
    change = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(541, 365)
        self.Button_Query = QtWidgets.QPushButton(Form)
        self.Button_Query.setGeometry(PyQt5.QtCore.QRect(180, 90, 161, 61))
        self.Button_Query.setObjectName("pushButton")
        self.Button_Query.clicked.connect(lambda: self.query.emit())
        self.Button_Logout = QtWidgets.QPushButton(Form)
        self.Button_Logout.setGeometry(PyQt5.QtCore.QRect(180, 230, 161, 61))
        self.Button_Logout.setObjectName("pushButton_2")
        self.Button_Logout.clicked.connect(lambda: self.logout.emit())
        self.Button_Change_Password = QtWidgets.QPushButton(Form)
        self.Button_Change_Password.setGeometry(PyQt5.QtCore.QRect(180, 160, 161, 61))
        self.Button_Change_Password.setObjectName("pushButton_3")
        self.Button_Change_Password.clicked.connect(lambda: self.change.emit())

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Student"))
        self.Button_Query.setText(_translate("Form", "Query"))
        self.Button_Logout.setText(_translate("Form", "Logout"))
        self.Button_Change_Password.setText(_translate("Form", "Change Password"))
class Teacher_Ui(QtWidgets.QWidget):
    query = PyQt5.QtCore.pyqtSignal()
    sss = PyQt5.QtCore.pyqtSignal()
    cp = PyQt5.QtCore.pyqtSignal()
    lo = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(541, 365)
        self.Button_Logout = QtWidgets.QPushButton(Form)
        self.Button_Logout.setGeometry(PyQt5.QtCore.QRect(120, 260, 281, 61))
        self.Button_Logout.setObjectName("pushButton")
        self.Button_Logout.clicked.connect(lambda: self.lo.emit())
        self.Button_Query = QtWidgets.QPushButton(Form)
        self.Button_Query.setGeometry(PyQt5.QtCore.QRect(120, 50, 281, 61))
        self.Button_Query.setObjectName("pushButton_2")
        self.Button_Query.clicked.connect(lambda: self.query.emit())
        self.Button_SSS = QtWidgets.QPushButton(Form)
        self.Button_SSS.setGeometry(PyQt5.QtCore.QRect(120, 120, 281, 61))
        self.Button_SSS.setObjectName("pushButton_3")
        self.Button_SSS.clicked.connect(lambda: self.sss.emit())
        self.Button_CP = QtWidgets.QPushButton(Form)
        self.Button_CP.setGeometry(PyQt5.QtCore.QRect(120, 190, 281, 61))
        self.Button_CP.setObjectName("pushButton_4")
        self.Button_CP.clicked.connect(lambda: self.cp.emit())

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Teacher"))
        self.Button_Logout.setText(_translate("Form", "Logout"))
        self.Button_Query.setText(_translate("Form", "Query"))
        self.Button_SSS.setText(_translate("Form", "Set Student\'s Score"))
        self.Button_CP.setText(_translate("Form", "Change Password"))
class Admin_Ui(QtWidgets.QWidget):
    query = PyQt5.QtCore.pyqtSignal()
    mi = PyQt5.QtCore.pyqtSignal()
    cp = PyQt5.QtCore.pyqtSignal()
    logout = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(541, 380)
        self.Button_Query = QtWidgets.QPushButton(Form)
        self.Button_Query.setGeometry(PyQt5.QtCore.QRect(170, 20, 181, 60))
        self.Button_Query.setObjectName("pushButton_2")
        self.Button_Query.clicked.connect(lambda: self.query.emit())
        self.Button_MI = QtWidgets.QPushButton(Form)
        self.Button_MI.setGeometry(PyQt5.QtCore.QRect(170, 90, 181, 60))
        self.Button_MI.setObjectName("pushButton_5")
        self.Button_MI.clicked.connect(lambda: self.mi.emit())
        self.Button_Change_Password = QtWidgets.QPushButton(Form)
        self.Button_Change_Password.setGeometry(PyQt5.QtCore.QRect(170, 160, 181, 60))
        self.Button_Change_Password.setObjectName("pushButton_4")
        self.Button_Change_Password.clicked.connect(lambda: self.cp.emit())
        self.Button_Initialize_Database = QtWidgets.QPushButton(Form)
        self.Button_Initialize_Database.setGeometry(PyQt5.QtCore.QRect(170, 230, 181, 60))
        self.Button_Initialize_Database.setObjectName("pushButton_6")
        self.Button_Initialize_Database.clicked.connect(self.initialize_database)
        self.Button_Logout = QtWidgets.QPushButton(Form)
        self.Button_Logout.setGeometry(PyQt5.QtCore.QRect(170, 300, 181, 60))
        self.Button_Logout.setObjectName("pushButton")
        self.Button_Logout.clicked.connect(lambda: self.logout.emit())

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Admin"))
        self.Button_Logout.setText(_translate("Form", "Logout"))
        self.Button_Query.setText(_translate("Form", "Query"))
        self.Button_Change_Password.setText(_translate("Form", "Change Password"))
        self.Button_Initialize_Database.setText(_translate("Form", "Initialize\nDatabase"))
        self.Button_MI.setText(_translate("Form", "Modify Information"))

    def initialize_database(self):
        reply = QtWidgets.QMessageBox.question(None, 'Initialize Database',
                                     'Are you sure to initialize the database? This operation will initialize the database (as shown in the Program Manual)',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            Initialize_Database()
        else:
            pass
class Query_Ui(QtWidgets.QWidget):
    stu_info = PyQt5.QtCore.pyqtSignal()
    stu_score = PyQt5.QtCore.pyqtSignal()
    cou_info = PyQt5.QtCore.pyqtSignal()
    ave_score = PyQt5.QtCore.pyqtSignal()
    bs = PyQt5.QtCore.pyqtSignal()
    ti = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(451, 330)
        self.Button_Student_Info = QtWidgets.QPushButton(Form)
        self.Button_Student_Info.setGeometry(PyQt5.QtCore.QRect(100, 20, 231, 40))
        self.Button_Student_Info.setObjectName("pushButton_3")
        self.Button_Student_Info.clicked.connect(lambda: self.stu_info.emit())
        self.Button_Student_Score_Info = QtWidgets.QPushButton(Form)
        self.Button_Student_Score_Info.setGeometry(PyQt5.QtCore.QRect(100, 70, 231, 40))
        self.Button_Student_Score_Info.setObjectName("pushButton_5")
        self.Button_Student_Score_Info.clicked.connect(lambda: self.stu_score.emit())
        self.Button_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Course_Info.setGeometry(PyQt5.QtCore.QRect(100, 120, 231, 40))
        self.Button_Course_Info.setObjectName("pushButton")
        self.Button_Course_Info.clicked.connect(lambda: self.cou_info.emit())
        self.Button_Teacher_Info = QtWidgets.QPushButton(Form)
        self.Button_Teacher_Info.setGeometry(PyQt5.QtCore.QRect(100, 170, 231, 40))
        self.Button_Teacher_Info.setObjectName("pushButton1")
        self.Button_Teacher_Info.clicked.connect(lambda: self.ti.emit())
        self.Button_Average_Score_Info = QtWidgets.QPushButton(Form)
        self.Button_Average_Score_Info.setGeometry(PyQt5.QtCore.QRect(100, 220, 231, 40))
        self.Button_Average_Score_Info.setObjectName("pushButton_2")
        self.Button_Average_Score_Info.clicked.connect(lambda: self.ave_score.emit())
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(100, 270, 231, 40))
        self.Button_Back.setObjectName("pushButton_4")
        self.Button_Back.clicked.connect(lambda: self.bs.emit())

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Query"))
        self.Button_Course_Info.setText(_translate("Form", "Course (Choosing) Info"))
        self.Button_Average_Score_Info.setText(_translate("Form", "Average Score Info"))
        self.Button_Student_Info.setText(_translate("Form", "Student Info"))
        self.Button_Teacher_Info.setText(_translate("Form", "Teacher (Teaching) Info"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.Button_Student_Score_Info.setText(_translate("Form", "Student Score Info"))
class Student_Info_Query_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(700, 350)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(480, 110, 200, 30))
        self.Button_Back.setObjectName("pushButton_2")
        self.Button_Back.clicked.connect(lambda: self.back.emit())
        self.Button_Student_Info = QtWidgets.QPushButton(Form)
        self.Button_Student_Info.setGeometry(PyQt5.QtCore.QRect(480, 30, 200, 30))
        self.Button_Student_Info.setObjectName("pushButton_3")
        self.Button_Student_Info.clicked.connect(self.Student_Info_Query)
        self.Button_Chosen_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Chosen_Course_Info.setGeometry(PyQt5.QtCore.QRect(480, 70, 200, 30))
        self.Button_Chosen_Course_Info.setObjectName("pushButton_1")
        self.Button_Chosen_Course_Info.clicked.connect(self.Chosen_Course_Info_Query)
        self.label_Student_ID = QtWidgets.QLabel(Form)
        self.label_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 30, 120, 20))
        self.label_Student_ID.setObjectName("label")
        self.label_Student_Name = QtWidgets.QLabel(Form)
        self.label_Student_Name.setGeometry(PyQt5.QtCore.QRect(20, 90, 120, 20))
        self.label_Student_Name.setObjectName("label_2")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 150, 700, 20))
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setObjectName("label_5")
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.lineEdit_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_ID.setGeometry(PyQt5.QtCore.QRect(160, 30, 300, 20))
        self.lineEdit_Student_ID.setObjectName("lineEdit")
        self.lineEdit_Student_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_Name.setGeometry(PyQt5.QtCore.QRect(160, 90, 300, 20))
        self.lineEdit_Student_Name.setObjectName("lineEdit_2")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(20, 170, 660, 170))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def Student_Info_Query(self):
        global db
        Student_ID = self.lineEdit_Student_ID.text()
        Student_Name = self.lineEdit_Student_Name.text()
        cursor = db.cursor()
        if len(Student_Name) == 0 and len(Student_ID) != 0:
            if not Student_ID.isdigit() or len(Student_ID) != 10:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
                return
            sql = f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\' ORDER BY StudentID'
        elif len(Student_Name) != 0 and len(Student_ID) != 0:
            if not Student_ID.isdigit() or len(Student_ID) != 10:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a decimal number"))
                return
            if not Student_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student name must be English characters"))
                return
            sql = f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\' AND StudentName=\'{Student_Name}\' ORDER BY StudentID'
        elif len(Student_ID) == 0 and len(Student_Name) != 0:
            if not Student_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student name must be English characters"))
                return
            sql = f'SELECT * FROM Students WHERE StudentName=\'{Student_Name}\' ORDER BY StudentID'
        elif len(Student_ID) == 0 and len(Student_Name) == 0:
            sql = f'SELECT * FROM Students ORDER BY StudentID'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
    def Chosen_Course_Info_Query(self):
        global db
        Student_ID = self.lineEdit_Student_ID.text()
        Student_Name = self.lineEdit_Student_Name.text()
        cursor = db.cursor()
        if len(Student_Name) == 0 and len(Student_ID) != 0:
            if not Student_ID.isdigit() or len(Student_ID) != 10:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
                return
            sql = f'SELECT DISTINCT * FROM Courses WHERE CourseID IN (SELECT DISTINCT CourseID FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' ORDER BY CourseID)'
        elif len(Student_Name) != 0 and len(Student_ID) != 0:
            if not Student_ID.isdigit() or len(Student_ID) != 10:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
                return
            if not Student_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student name must be English characters"))
                return
            sql = f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\' AND StudentName=\'{Student_Name}\''
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                sql = f'SELECT DISTINCT * FROM Courses WHERE CourseID IN (SELECT DISTINCT CourseID FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' ORDER BY CourseID)'
        elif len(Student_ID) == 0 and len(Student_Name) != 0:
            if not Student_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student name must be English characters"))
                return
            sql = f'SELECT DISTINCT * FROM Courses WHERE CourseID IN (SELECT DISTINCT CourseID FROM CourseChoosing WHERE StudentID IN (SELECT DISTINCT StudentID FROM Students WHERE StudentName=\'{Student_Name}\')) ORDER BY CourseID'
        elif len(Student_ID) == 0 and len(Student_Name) == 0:
            sql = 'SELECT DISTINCT * FROM Courses WHERE CourseID IN (SELECT DISTINCT CourseID FROM CourseChoosing WHERE StudentID IN (SELECT DISTINCT StudentID FROM Students)) ORDER BY CourseID'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Student Info Query"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Student_Name.setText(_translate("Form", "Student Name"))
        self.label_Query_Result.setText(_translate("Form", "Query Result"))
        self.Button_Student_Info.setText(_translate("Form", "Student Info"))
        self.Button_Chosen_Course_Info.setText(_translate("Form", "Chosen Course Info"))
class Student_Score_Query_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(700, 350)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(480, 110, 200, 30))
        self.Button_Back.setObjectName("pushButton_2")
        self.Button_Back.clicked.connect(lambda: self.back.emit())
        self.Button_Student_Score_Info = QtWidgets.QPushButton(Form)
        self.Button_Student_Score_Info.setGeometry(PyQt5.QtCore.QRect(480, 30, 200, 30))
        self.Button_Student_Score_Info.setObjectName("pushButton_3")
        self.Button_Student_Score_Info.clicked.connect(self.Student_Score_Query)

        self.label_Student_ID = QtWidgets.QLabel(Form)
        self.label_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 30, 120, 20))
        self.label_Student_ID.setObjectName("label")
        self.label_Student_Name = QtWidgets.QLabel(Form)
        self.label_Student_Name.setGeometry(PyQt5.QtCore.QRect(20, 60, 120, 20))
        self.label_Student_Name.setObjectName("label_2")
        self.label_Course_ID = QtWidgets.QLabel(Form)
        self.label_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 90, 120, 20))
        self.label_Course_ID.setObjectName("label_3")
        self.label_Course_Name = QtWidgets.QLabel(Form)
        self.label_Course_Name.setGeometry(PyQt5.QtCore.QRect(20, 120, 120, 20))
        self.label_Course_Name.setObjectName("label_4")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(255, 150, 200, 20))
        self.label_Query_Result.setObjectName("label_5")
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.lineEdit_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_ID.setGeometry(PyQt5.QtCore.QRect(160, 30, 300, 20))
        self.lineEdit_Student_ID.setObjectName("lineEdit")
        self.lineEdit_Student_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_Name.setGeometry(PyQt5.QtCore.QRect(160, 60, 300, 20))
        self.lineEdit_Student_Name.setObjectName("lineEdit_2")
        self.lineEdit_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_ID.setGeometry(PyQt5.QtCore.QRect(160, 90, 300, 20))
        self.lineEdit_Course_ID.setObjectName("lineEdit_3")
        self.lineEdit_Course_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_Name.setGeometry(PyQt5.QtCore.QRect(160, 120, 300, 20))
        self.lineEdit_Course_Name.setObjectName("lineEdit_4")

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(20, 170, 660, 170))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Student Score Info Query"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Student_Name.setText(_translate("Form", "Student Name"))
        self.label_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Course_Name.setText(_translate("Form", "Course Name"))
        self.label_Query_Result.setText(_translate("Form", "Query Result"))
        self.Button_Student_Score_Info.setText(_translate("Form", "Student Score Info"))
    def Student_Score_Query(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Student_ID.text()
        if Student_ID != '':
            if len(Student_ID) != 10 or not Student_ID.isdigit():
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
                return
        Student_Name = self.lineEdit_Student_Name.text()
        for i in Student_Name:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student Name should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        Course_ID = self.lineEdit_Course_ID.text()
        if Course_ID != '':
            if len(Course_ID) != 7 or not Course_ID.isdigit():
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
                return
        Course_Name = self.lineEdit_Course_Name.text()
        for i in Course_Name:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form",
                                                            "Course Name should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        params = []
        if len(Student_ID) == 0 and len(Student_Name) == 0 and len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     ORDER BY Students.StudentID, Courses.CourseID;'''
        elif len(Student_ID) == 0 and len(Student_Name) == 0 and len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Course_Name)
        elif len(Student_ID) == 0 and len(Student_Name) == 0 and len(Course_ID) != 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Courses.CourseID=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Course_ID)
        elif len(Student_ID) == 0 and len(Student_Name) == 0 and len(Course_ID) != 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Courses.CourseID=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Course_ID)
            params.append(Course_Name)
        elif len(Student_ID) == 0 and len(Student_Name) != 0 and len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_Name)
        elif len(Student_ID) == 0 and len(Student_Name) != 0 and len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentName=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_Name)
            params.append(Course_Name)
        elif len(Student_ID) == 0 and len(Student_Name) != 0 and len(Course_ID) != 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentName=? AND Courses.CourseID=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_Name)
            params.append(Course_ID)
        elif len(Student_ID) == 0 and len(Student_Name) != 0 and len(Course_ID) != 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentName=? AND Courses.CourseID=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_Name)
            params.append(Course_ID)
            params.append(Course_Name)
        elif len(Student_ID) != 0 and len(Student_Name) == 0 and len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
        elif len(Student_ID) != 0 and len(Student_Name) == 0 and len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Course_Name)
        elif len(Student_ID) != 0 and len(Student_Name) == 0 and len(Course_ID) != 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Courses.CourseID=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Course_ID)
        elif len(Student_ID) != 0 and len(Student_Name) == 0 and len(Course_ID) != 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Courses.CourseID=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Course_ID)
            params.append(Course_Name)
        elif len(Student_ID) != 0 and len(Student_Name) != 0 and len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Students.StudentName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Student_Name)
        elif len(Student_ID) != 0 and len(Student_Name) != 0 and len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Students.StudentName=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Student_Name)
            params.append(Course_Name)
        elif len(Student_ID) != 0 and len(Student_Name) != 0 and len(Course_ID) != 0 and len(Course_Name) == 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Students.StudentName=? AND Courses.CourseID=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Student_Name)
            params.append(Course_ID)
        elif len(Student_ID) != 0 and len(Student_Name) != 0 and len(Course_ID) != 0 and len(Course_Name) != 0:
            sql = '''SELECT Students.StudentName, Students.StudentID, Courses.CourseName, Courses.CourseID, CourseChoosing.Score
                     FROM Students
                     JOIN CourseChoosing ON Students.StudentID=CourseChoosing.StudentID
                     JOIN Courses ON Courses.CourseID=CourseChoosing.CourseID
                     WHERE Students.StudentID=? AND Students.StudentName=? AND Courses.CourseID=? AND Courses.CourseName=?
                     ORDER BY Students.StudentID, Courses.CourseID;'''
            params.append(Student_ID)
            params.append(Student_Name)
            params.append(Course_ID)
            params.append(Course_Name)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
class Course_Info_Query_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(700, 350)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(480, 110, 200, 30))
        self.Button_Back.setObjectName("pushButton_2")
        self.Button_Back.clicked.connect(lambda: self.back.emit())
        self.Button_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Course_Info.setGeometry(PyQt5.QtCore.QRect(480, 30, 200, 30))
        self.Button_Course_Info.setObjectName("pushButton_3")
        self.Button_Course_Info.clicked.connect(self.Course_Info_Query)
        self.Button_Course_Choosing_Info = QtWidgets.QPushButton(Form)
        self.Button_Course_Choosing_Info.setGeometry(PyQt5.QtCore.QRect(480, 70, 200, 30))
        self.Button_Course_Choosing_Info.setObjectName("pushButton_1")
        self.Button_Course_Choosing_Info.clicked.connect(self.Course_Choosing_Info_Query)

        self.label_Course_ID = QtWidgets.QLabel(Form)
        self.label_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 30, 120, 20))
        self.label_Course_ID.setObjectName("label")
        self.label_Course_Name = QtWidgets.QLabel(Form)
        self.label_Course_Name.setGeometry(PyQt5.QtCore.QRect(20, 90, 120, 20))
        self.label_Course_Name.setObjectName("label_2")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 150, 700, 20))
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setObjectName("label_5")
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.lineEdit_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_ID.setGeometry(PyQt5.QtCore.QRect(160, 30, 300, 20))
        self.lineEdit_Course_ID.setObjectName("lineEdit")
        self.lineEdit_Course_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_Name.setGeometry(PyQt5.QtCore.QRect(160, 90, 300, 20))
        self.lineEdit_Course_Name.setObjectName("lineEdit_2")

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(20, 170, 660, 170))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Course and Course Choosing Info Query"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Course_Name.setText(_translate("Form", "Course Name"))
        self.label_Query_Result.setText(_translate("Form", "Query Result"))
        self.Button_Course_Info.setText(_translate("Form", "Course Info"))
        self.Button_Course_Choosing_Info.setText(_translate("Form", "Course Choosing Info"))
    def Course_Info_Query(self):
        global db
        cursor = db.cursor()
        Course_ID = self.lineEdit_Course_ID.text()
        Course_Name = self.lineEdit_Course_Name.text()
        for i in Course_Name:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Course Name should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        params = []
        if len(Course_Name) == 0 and len(Course_ID) != 0:
            if not Course_ID.isdigit():
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a decimal number"))
                return
            sql = """
            SELECT Courses.CourseID, Courses.CourseName, Courses.TeacherID, Teachers.TeacherName, Courses.Credit, Courses.Grade, Courses.CanceledYear
            FROM Courses
            JOIN Teachers ON Teachers.TeacherID = Courses.TeacherID
            WHERE Courses.CourseID = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_ID)
        elif len(Course_Name) != 0 and len(Course_ID) != 0:
            if not Course_ID.isdigit():
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a decimal number"))
                return
            sql = """
            SELECT Courses.CourseID, Courses.CourseName, Courses.TeacherID, Teachers.TeacherName, Courses.Credit, Courses.Grade, Courses.CanceledYear
            FROM Courses
            JOIN Teachers ON Teachers.TeacherID = Courses.TeacherID
            WHERE Courses.CourseID = ? AND Courses.CourseName = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_ID)
            params.append(Course_Name)
        elif len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = """
            SELECT Courses.CourseID, Courses.CourseName, Courses.TeacherID, Teachers.TeacherName, Courses.Credit, Courses.Grade, Courses.CanceledYear
            FROM Courses
            JOIN Teachers ON Teachers.TeacherID = Courses.TeacherID
            WHERE Courses.CourseName = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_Name)
        elif len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = """
            SELECT Courses.CourseID, Courses.CourseName, Courses.TeacherID, Teachers.TeacherName, Courses.Credit, Courses.Grade, Courses.CanceledYear
            FROM Courses
            JOIN Teachers ON Teachers.TeacherID = Courses.TeacherID
            ORDER BY Courses.CourseID;
            """
        cursor.execute(sql, params)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
    def Course_Choosing_Info_Query(self):
        global db
        cursor = db.cursor()
        Course_ID = self.lineEdit_Course_ID.text()
        Course_Name = self.lineEdit_Course_Name.text()
        for i in Course_Name:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Course Name should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        params = []
        if len(Course_Name) == 0 and len(Course_ID) != 0:
            sql = """
            SELECT CourseChoosing.CourseID, Courses.CourseName, CourseChoosing.StudentID, Students.StudentName, CourseChoosing.TeacherID, Teachers.TeacherName, CourseChoosing.ChosenYear, CourseChoosing.Score
            FROM CourseChoosing
            JOIN Teachers ON Teachers.TeacherID = CourseChoosing.TeacherID
            JOIN Students ON Students.StudentID = CourseChoosing.StudentID
            JOIN Courses ON Courses.CourseID = CourseChoosing.CourseID
            WHERE Courses.CourseID = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_ID)
        elif len(Course_Name) != 0 and len(Course_ID) != 0:
            sql = """
            SELECT CourseChoosing.CourseID, Courses.CourseName, CourseChoosing.StudentID, Students.StudentName, CourseChoosing.TeacherID, Teachers.TeacherName, CourseChoosing.ChosenYear, CourseChoosing.Score
            FROM CourseChoosing
            JOIN Teachers ON Teachers.TeacherID = CourseChoosing.TeacherID
            JOIN Students ON Students.StudentID = CourseChoosing.StudentID
            JOIN Courses ON Courses.CourseID = CourseChoosing.CourseID
            WHERE Courses.CourseID = ? AND Courses.CourseName = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_ID)
            params.append(Course_Name)
        elif len(Course_ID) == 0 and len(Course_Name) != 0:
            sql = """
            SELECT CourseChoosing.CourseID, Courses.CourseName, CourseChoosing.StudentID, Students.StudentName, CourseChoosing.TeacherID, Teachers.TeacherName, CourseChoosing.ChosenYear, CourseChoosing.Score
            FROM CourseChoosing
            JOIN Teachers ON Teachers.TeacherID = CourseChoosing.TeacherID
            JOIN Students ON Students.StudentID = CourseChoosing.StudentID
            JOIN Courses ON Courses.CourseID = CourseChoosing.CourseID
            WHERE Courses.CourseName = ?
            ORDER BY Courses.CourseID;
            """
            params.append(Course_Name)
        elif len(Course_ID) == 0 and len(Course_Name) == 0:
            sql = """
            SELECT CourseChoosing.CourseID, Courses.CourseName, CourseChoosing.StudentID, Students.StudentName, CourseChoosing.TeacherID, Teachers.TeacherName, CourseChoosing.ChosenYear, CourseChoosing.Score
            FROM CourseChoosing
            JOIN Teachers ON Teachers.TeacherID = CourseChoosing.TeacherID
            JOIN Students ON Students.StudentID = CourseChoosing.StudentID
            JOIN Courses ON Courses.CourseID = CourseChoosing.CourseID
            ORDER BY Courses.CourseID;
            """
        cursor.execute(sql, params)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
class Teaching_Info_Query_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(700, 350)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(480, 110, 200, 30))
        self.Button_Back.setObjectName("pushButton_2")
        self.Button_Back.clicked.connect(lambda: self.back.emit())
        self.Button_Teacher_Info = QtWidgets.QPushButton(Form)
        self.Button_Teacher_Info.setGeometry(PyQt5.QtCore.QRect(480, 30, 200, 30))
        self.Button_Teacher_Info.setObjectName("pushButton_3")
        self.Button_Teacher_Info.clicked.connect(self.Teacher_Info_Query)
        self.Button_Teaching_Info = QtWidgets.QPushButton(Form)
        self.Button_Teaching_Info.setGeometry(PyQt5.QtCore.QRect(480, 70, 200, 30))
        self.Button_Teaching_Info.setObjectName("pushButton_1")
        self.Button_Teaching_Info.clicked.connect(self.Teaching_Info_Query)
        self.label_Teacher_ID = QtWidgets.QLabel(Form)
        self.label_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(20, 30, 120, 20))
        self.label_Teacher_ID.setObjectName("label")
        self.label_Teacher_Name = QtWidgets.QLabel(Form)
        self.label_Teacher_Name.setGeometry(PyQt5.QtCore.QRect(20, 90, 120, 20))
        self.label_Teacher_Name.setObjectName("label_2")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 150, 700, 20))
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setObjectName("label_5")
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.lineEdit_Teacher_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(160, 30, 300, 20))
        self.lineEdit_Teacher_ID.setObjectName("lineEdit")
        self.lineEdit_Teacher_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Teacher_Name.setGeometry(PyQt5.QtCore.QRect(160, 90, 300, 20))
        self.lineEdit_Teacher_Name.setObjectName("lineEdit_2")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(20, 170, 660, 170))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def Teacher_Info_Query(self):
        global db
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        Teacher_Name = self.lineEdit_Teacher_Name.text()
        cursor = db.cursor()
        if len(Teacher_Name) == 0 and len(Teacher_ID) != 0:
            if not Teacher_ID.isdigit() or len(Teacher_ID) != 5:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 7 digit decimal number"))
                return
            sql = f'SELECT * FROM Teachers WHERE TeacherID=\'{Teacher_ID}\' ORDER BY TeacherID'
        elif len(Teacher_Name) != 0 and len(Teacher_ID) != 0:
            if not Teacher_ID.isdigit() or len(Teacher_ID) != 5:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a decimal number"))
                return
            if not Teacher_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher name must be English characters"))
                return
            sql = f'SELECT * FROM Teachers WHERE TeacherID=\'{Teacher_ID}\' AND TeacherName=\'{Teacher_Name}\' ORDER BY TeacherID'
        elif len(Teacher_ID) == 0 and len(Teacher_Name) != 0:
            if not Teacher_Name.isalpha():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher name must be English characters"))
                return
            sql = f'SELECT * FROM Teachers WHERE TeacherName=\'{Teacher_Name}\' ORDER BY TeacherID'
        elif len(Teacher_ID) == 0 and len(Teacher_Name) == 0:
            sql = f'SELECT * FROM Teachers ORDER BY TeacherID'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
    def Teaching_Info_Query(self):
        global db
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        Teacher_Name = self.lineEdit_Teacher_Name.text()
        cursor = db.cursor()
        if Teacher_ID == '' and Teacher_Name == '':
            sql = f"SELECT DISTINCT Teachers.TeacherName, Teachers.TeacherID, Courses.CourseName, Courses.CourseID, CourseChoosing.ChosenYear, Courses.Credit, Courses.Grade, Courses.CanceledYear FROM Teachers JOIN CourseChoosing ON Teachers.TeacherID=CourseChoosing.TeacherID JOIN Courses ON CourseChoosing.CourseID=Courses.CourseID ORDER BY Teachers.TeacherID, Courses.CourseID, CourseChoosing.ChosenYear;"
        elif Teacher_ID != '' and Teacher_Name == '':
            if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID should be a 5 digit decimal number"))
                return
            sql = f"SELECT DISTINCT Teachers.TeacherName, Teachers.TeacherID, Courses.CourseName, Courses.CourseID, CourseChoosing.ChosenYear, Courses.Credit, Courses.Grade, Courses.CanceledYear FROM Teachers JOIN CourseChoosing ON Teachers.TeacherID=CourseChoosing.TeacherID JOIN Courses ON CourseChoosing.CourseID=Courses.CourseID WHERE Teachers.TeacherID=\'{Teacher_ID}\' ORDER BY Courses.CourseID, CourseChoosing.ChosenYear;"
        elif Teacher_ID == '' and Teacher_Name != '':
            for i in Teacher_Name:
                if i in specific_character:
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Teacher Name should not contain \\, /, :, ?, \", \', <, >, |"))
                    return
            sql = f"SELECT DISTINCT Teachers.TeacherName, Teachers.TeacherID, Courses.CourseName, Courses.CourseID, CourseChoosing.ChosenYear, Courses.Credit, Courses.Grade, Courses.CanceledYear FROM Teachers JOIN CourseChoosing ON Teachers.TeacherID=CourseChoosing.TeacherID JOIN Courses ON CourseChoosing.CourseID=Courses.CourseID WHERE Teachers.TeacherName=\'{Teacher_Name}\' ORDER BY Courses.CourseID, CourseChoosing.ChosenYear;"
        elif Teacher_ID != '' and Teacher_Name != '':
            if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID should be a 5 digit decimal number"))
                return
            for i in Teacher_Name:
                if i in specific_character:
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Teacher Name should not contain \\, /, :, ?, \", \', <, >, |"))
                    return
            sql = f"SELECT DISTINCT Teachers.TeacherName, Teachers.TeacherID, Courses.CourseName, Courses.CourseID, CourseChoosing.ChosenYear, Courses.Credit, Courses.Grade, Courses.CanceledYear FROM Teachers JOIN CourseChoosing ON Teachers.TeacherID=CourseChoosing.TeacherID JOIN Courses ON CourseChoosing.CourseID=Courses.CourseID WHERE Teachers.TeacherID=\'{Teacher_ID}\' AND Teachers.TeacherName=\'{Teacher_Name}\' ORDER BY Courses.CourseID, CourseChoosing.ChosenYear;"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Teacher (Teaching) Info Query"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Teacher_ID.setText(_translate("Form", "Teacher ID"))
        self.label_Teacher_Name.setText(_translate("Form", "Teacher Name"))
        self.label_Query_Result.setText(_translate("Form", "Query Result"))
        self.Button_Teacher_Info.setText(_translate("Form", "Teacher Info"))
        self.Button_Teaching_Info.setText(_translate("Form", "Teaching Info"))
class Average_Score_Info_Query_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(500, 179)
        self.label_Student_ID = QtWidgets.QLabel(Form)
        self.label_Student_ID.setGeometry(PyQt5.QtCore.QRect(10, 30, 100, 16))
        self.label_Student_ID.setObjectName("label")
        self.label_Course_ID = QtWidgets.QLabel(Form)
        self.label_Course_ID.setGeometry(PyQt5.QtCore.QRect(10, 60, 100, 20))
        self.label_Course_ID.setObjectName("label_2")
        self.label_Class = QtWidgets.QLabel(Form)
        self.label_Class.setGeometry(PyQt5.QtCore.QRect(10, 90, 100, 20))
        self.label_Class.setObjectName("label_3")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 130, 500, 50))
        self.label_Query_Result.setObjectName("label_5")
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        self.lineEdit_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_ID.setGeometry(PyQt5.QtCore.QRect(110, 30, 180, 20))
        self.lineEdit_Student_ID.setObjectName("lineEdit")
        self.lineEdit_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_ID.setGeometry(PyQt5.QtCore.QRect(110, 60, 180, 20))
        self.lineEdit_Course_ID.setObjectName("lineEdit_2")
        self.lineEdit_Class = QtWidgets.QLineEdit(Form)
        self.lineEdit_Class.setGeometry(PyQt5.QtCore.QRect(110, 90, 180, 20))
        self.lineEdit_Class.setObjectName("lineEdit_3")

        self.Button_query = QtWidgets.QPushButton(Form)
        self.Button_query.setGeometry(PyQt5.QtCore.QRect(300, 30, 190, 24))
        self.Button_query.setObjectName("pushButton")
        self.Button_query.clicked.connect(self.Query_Average_Score)
        self.Button_back = QtWidgets.QPushButton(Form)
        self.Button_back.setGeometry(PyQt5.QtCore.QRect(300, 90, 190, 24))
        self.Button_back.setObjectName("pushButton")
        self.Button_back.clicked.connect(lambda: self.back.emit())

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(PyQt5.QtCore.QRect(300, 60, 190, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setEditable(True)

        line_edit = self.comboBox.lineEdit()
        line_edit.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Average Score Query"))
        self.label_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Class.setText(_translate("Form", "Class"))
        self.Button_query.setText(_translate("Form", "Query Average Score"))
        self.Button_back.setText(_translate("Form", "Back"))
        self.comboBox.setItemText(0, _translate("Form", "One Student"))
        self.comboBox.setItemText(1, _translate("Form", "All Students"))
        self.comboBox.setItemText(2, _translate("Form", "Course"))
        self.comboBox.setItemText(3, _translate("Form", "Class"))
        self.label_Query_Result.setText(_translate("Form", "Query Result"))
    def Query_Average_Score(self):
        global db
        Student_ID = self.lineEdit_Student_ID.text()
        Course_ID = self.lineEdit_Course_ID.text()
        Class = self.lineEdit_Class.text()
        flag = self.comboBox.currentText()
        cursor = db.cursor()
        if flag == 'One Student':
            if not Student_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a decimal number"))
                return
            cursor.execute(f'SELECT StudentName FROM Students WHERE StudentID=\'{Student_ID}\'')
            results = cursor.fetchall()
            if len(results) == 0:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"There is no StudentID matching {Student_ID}"))
            else:
                Student_Name = results[0][0]
                sql = f'SELECT AVG(Score) FROM CourseChoosing WHERE StudentID=\'{Student_ID}\''
                cursor.execute(sql)
                results = cursor.fetchall()
                Average_Score = results[0][0]
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"The Average Score of {Student_Name} is {Average_Score}."))
        elif flag == 'All Students':
            sql = 'SELECT AVG(Score) FROM CourseChoosing'
            cursor.execute(sql)
            results = cursor.fetchall()
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", f"The Average Score of all student is {results[0][0]}."))
        elif flag == 'Course':
            if not Course_ID.isdigit() or len(Course_ID) != 7:
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
                return
            cursor.execute(f'SELECT CourseName FROM Courses WHERE CourseID=\'{Course_ID}\'')
            results = cursor.fetchall()
            if len(results) == 0:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"There is no CourseID matching {Course_ID}"))
            else:
                Course_Name = results[0][0]
                if Class == '':
                    sql = f'SELECT AVG(Score) FROM CourseChoosing WHERE CourseID=\'{Course_ID}\''
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form", f"The Average Score of {Course_Name} is {results[0][0]}."))
                else:
                    for i in Class:
                        if i in specific_character:
                            self.label_Query_Result.setText(
                                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                        "Class should not contain \\, /, :, ?, \", \', <, >, |"))
                            return
                    cursor.execute(f'SELECT * FROM Students where Class=\'{Class}\'')
                    results = cursor.fetchall()
                    if len(results) == 0:
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                f"There is no such a class named \'{Class}\'")
                        return
                    # 从CourseChoosing选出StudentID, 然后在Students里找是否有匹配的class
                    cursor.execute(f'SELECT * FROM Students where Class=\'{Class}\' AND StudentID in(SELECT StudentID FROM CourseChoosing WHERE CourseID=\'{Course_ID}\')')
                    results = cursor.fetchall()
                    if len(results) == 0:
                        self.label_Query_Result.setText(
                            PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                    f"There is no student who chose\n{Course_Name} in {Class}"))
                        return
                    cursor.execute(f'SELECT AVG(Score) FROM CourseChoosing WHERE CourseID=\'{Course_ID}\' AND StudentID IN (SELECT StudentID FROM Students WHERE Class=\'{Class}\')')
                    results = cursor.fetchall()
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                f"The Average Score of {Class}\nin {Course_Name} is {results[0][0]}."))
        elif flag == 'Class':
            if Class == '':
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"Class should not be empty"))
                return
            cursor.execute(f'SELECT Class FROM Students WHERE Class=\'{Class}\'')
            results = cursor.fetchall()
            if len(results) == 0:
                self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", f"There is no class named {Class}"))
                return
            if Course_ID == '':
                sql = f'SELECT AVG(Score) FROM CourseChoosing WHERE StudentID IN (SELECT StudentID FROM Students WHERE Class=\'{Class}\')'
                cursor.execute(sql)
                results = cursor.fetchall()
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form",
                                                            f"The Average Score of {Class} is {results[0][0]}."))
                return
            for i in Course_ID:
                if i in specific_character:
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Course ID should not contain \\, /, :, ?, \", \', <, >, |"))
                    return
            cursor.execute(f"SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\'")
            results = cursor.fetchall()
            if len(results) == 0:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"There is no matched course"))
                return
            Course_Name = results[0][1]
            cursor.execute(f"SELECT * FROM CourseChoosing WHERE CourseID=\'{Course_ID}\' AND StudentID IN (SELECT StudentID FROM Students WHERE Class=\'{Class}\')")
            results = cursor.fetchall()
            if len(results) == 0:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", f"There is no student in {Class} who has chosen {Course_Name}"))
                return
            cursor.execute(
                f"SELECT AVG(Score) FROM CourseChoosing WHERE CourseID=\'{Course_ID}\' AND StudentID IN (SELECT StudentID FROM Students WHERE Class=\'{Class}\')")
            results = cursor.fetchall()
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                        f"The Average Score of {Class}\nin {Course_Name} is {results[0][0]}."))
        else:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                        f"Please choose one of the four items"))
class Modify_Info_Ui(QtWidgets.QWidget):
    stu_info = PyQt5.QtCore.pyqtSignal()
    cou_info = PyQt5.QtCore.pyqtSignal()
    coc_info = PyQt5.QtCore.pyqtSignal()
    bs = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(451, 313)
        self.Button_Student_Info = QtWidgets.QPushButton(Form)
        self.Button_Student_Info.setGeometry(PyQt5.QtCore.QRect(120, 60, 191, 41))
        self.Button_Student_Info.setObjectName("pushButton_3")
        self.Button_Student_Info.clicked.connect(lambda: self.stu_info.emit())
        self.Button_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Course_Info.setGeometry(PyQt5.QtCore.QRect(120, 110, 191, 41))
        self.Button_Course_Info.setObjectName("pushButton")
        self.Button_Course_Info.clicked.connect(lambda: self.cou_info.emit())
        self.Button_Course_Choosing_Info = QtWidgets.QPushButton(Form)
        self.Button_Course_Choosing_Info.setGeometry(PyQt5.QtCore.QRect(120, 160, 191, 41))
        self.Button_Course_Choosing_Info.setObjectName("pushButton_2")
        self.Button_Course_Choosing_Info.clicked.connect(lambda: self.coc_info.emit())
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(120, 210, 191, 41))
        self.Button_Back.setObjectName("pushButton_4")
        self.Button_Back.clicked.connect(lambda: self.bs.emit())

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Modify Information"))
        self.Button_Course_Info.setText(_translate("Form", "Course Info"))
        self.Button_Course_Choosing_Info.setText(_translate("Form", "Course Choosing Info"))
        self.Button_Student_Info.setText(_translate("Form", "Student Info"))
        self.Button_Back.setText(_translate("Form", "Back"))
class Student_Info_Modify_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(451, 465)
        self.label_Query_Line = QtWidgets.QLabel(Form)
        self.label_Query_Line.setGeometry(PyQt5.QtCore.QRect(10, 10, 431, 20))
        self.label_Query_Line.setObjectName("label_5")
        self.label_Query_Student_ID = QtWidgets.QLabel(Form)
        self.label_Query_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 47, 120, 16))
        self.label_Query_Student_ID.setObjectName("label")
        self.label_Modify_Line = QtWidgets.QLabel(Form)
        self.label_Modify_Line.setGeometry(PyQt5.QtCore.QRect(10, 80, 431, 20))
        self.label_Modify_Line.setObjectName("label_4")
        self.label_Modify_Student_ID = QtWidgets.QLabel(Form)
        self.label_Modify_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 100, 120, 16))
        self.label_Modify_Student_ID.setObjectName("label_7")
        self.label_Student_Name = QtWidgets.QLabel(Form)
        self.label_Student_Name.setGeometry(PyQt5.QtCore.QRect(20, 130, 120, 20))
        self.label_Student_Name.setObjectName("label_6")
        self.label_Sex = QtWidgets.QLabel(Form)
        self.label_Sex.setGeometry(PyQt5.QtCore.QRect(20, 160, 120, 20))
        self.label_Sex.setObjectName("label_3")
        self.label_Entrance_Age = QtWidgets.QLabel(Form)
        self.label_Entrance_Age.setGeometry(PyQt5.QtCore.QRect(20, 190, 120, 20))
        self.label_Entrance_Age.setObjectName("label_9")
        self.label_Entrance_Year = QtWidgets.QLabel(Form)
        self.label_Entrance_Year.setGeometry(PyQt5.QtCore.QRect(20, 220, 120, 20))
        self.label_Entrance_Year.setObjectName("label_8")
        self.label_Class = QtWidgets.QLabel(Form)
        self.label_Class.setGeometry(PyQt5.QtCore.QRect(20, 250, 120, 20))
        self.label_Class.setObjectName("label_10")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 280, 451, 20))
        self.label_Query_Result.setObjectName("label_11")
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.Button_Query_Student_Info = QtWidgets.QPushButton(Form)
        self.Button_Query_Student_Info.setGeometry(PyQt5.QtCore.QRect(300, 30, 141, 50))
        self.Button_Query_Student_Info.setObjectName("pushButton")
        self.Button_Query_Student_Info.clicked.connect(self.Query)
        self.Button_Insert = QtWidgets.QPushButton(Form)
        self.Button_Insert.setGeometry(PyQt5.QtCore.QRect(300, 100, 141, 51))
        self.Button_Insert.setObjectName("pushButton_2")
        self.Button_Insert.clicked.connect(self.Insert)
        self.Button_Update = QtWidgets.QPushButton(Form)
        self.Button_Update.setGeometry(PyQt5.QtCore.QRect(300, 160, 141, 51))
        self.Button_Update.setObjectName("pushButton_3")
        self.Button_Update.clicked.connect(self.Update)
        self.Button_Delete = QtWidgets.QPushButton(Form)
        self.Button_Delete.setGeometry(PyQt5.QtCore.QRect(300, 220, 141, 51))
        self.Button_Delete.setObjectName("pushButton_4")
        self.Button_Delete.clicked.connect(self.Delete)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(190, 435, 75, 24))
        self.Button_Back.setObjectName("pushButton_5")
        self.Button_Back.clicked.connect(lambda: self.back.emit())

        self.lineEdit_Query_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Query_Student_ID.setGeometry(PyQt5.QtCore.QRect(140, 47, 150, 20))
        self.lineEdit_Query_Student_ID.setObjectName("lineEdit")
        self.lineEdit_Modify_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Modify_Student_ID.setGeometry(PyQt5.QtCore.QRect(140, 100, 150, 20))
        self.lineEdit_Modify_Student_ID.setObjectName("lineEdit_5")
        self.lineEdit_Student_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_Name.setGeometry(PyQt5.QtCore.QRect(140, 130, 150, 20))
        self.lineEdit_Student_Name.setObjectName("lineEdit_4")
        self.lineEdit_Sex = QtWidgets.QLineEdit(Form)
        self.lineEdit_Sex.setGeometry(PyQt5.QtCore.QRect(140, 160, 150, 20))
        self.lineEdit_Sex.setObjectName("lineEdit_3")
        self.lineEdit_Entrance_Age = QtWidgets.QLineEdit(Form)
        self.lineEdit_Entrance_Age.setGeometry(PyQt5.QtCore.QRect(140, 190, 150, 20))
        self.lineEdit_Entrance_Age.setObjectName("lineEdit_7")
        self.lineEdit_Entrance_Year = QtWidgets.QLineEdit(Form)
        self.lineEdit_Entrance_Year.setGeometry(PyQt5.QtCore.QRect(140, 220, 150, 20))
        self.lineEdit_Entrance_Year.setObjectName("lineEdit_6")
        self.lineEdit_Class = QtWidgets.QLineEdit(Form)
        self.lineEdit_Class.setGeometry(PyQt5.QtCore.QRect(140, 250, 150, 20))
        self.lineEdit_Class.setObjectName("lineEdit_8")

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(10, 306, 431, 120))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Student Info Modify"))
        self.label_Query_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Sex.setText(_translate("Form", "Sex"))
        self.Button_Query_Student_Info.setText(_translate("Form", "Query Student\nInfo"))
        self.label_Modify_Line.setText(
            _translate("Form", "---------------------Modify---------------------"))
        self.Button_Insert.setText(_translate("Form", "Insert"))
        self.Button_Update.setText(_translate("Form", "Update"))
        self.Button_Delete.setText(_translate("Form", "Delete"))
        self.label_Query_Line.setText(
            _translate("Form", "----------------------Query---------------------"))
        self.label_Student_Name.setText(_translate("Form", "Student Name"))
        self.label_Modify_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Entrance_Year.setText(_translate("Form", "Entrance Year"))
        self.label_Entrance_Age.setText(_translate("Form", "Entrance Age"))
        self.label_Class.setText(_translate("Form", "Class"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Query_Result.setText(_translate("Form", "Operation Result"))
    def Query(self):
        global db
        Student_ID = self.lineEdit_Query_Student_ID.text()
        cursor = db.cursor()
        if Student_ID != '':
            if len(Student_ID) != 10 or not Student_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
                return
            sql = f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\' ORDER BY StudentID;'
        else:
            sql = 'SELECT * FROM Students ORDER BY StudentID;'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
    def Insert(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        if len(Student_ID) != 10 or not Student_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        Student_Name = self.lineEdit_Student_Name.text()
        if not Student_Name.isalpha():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student Name must be English characters"))
            return
        Sex = self.lineEdit_Sex.text()
        if Sex not in ['male', 'female']:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Sex must be \'male\' or \'female\'"))
            return
        Entrance_Age = self.lineEdit_Entrance_Age.text()
        if not Entrance_Age.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance Age must be a decimal number"))
            return
        Entrance_Age = int(Entrance_Age)
        if not 10 <= Entrance_Age <= 50:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance Age must in range [10,50]"))
            return
        Entrance_Year = self.lineEdit_Entrance_Year.text()
        if not Entrance_Year.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance Year must be a decimal number"))
            return
        Entrance_Year = int(Entrance_Year)
        Class = self.lineEdit_Class.text()
        if Class == '':
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Please input the class name"))
            return
        for i in Class:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Class should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        cursor.execute(f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\'')
        results = cursor.fetchall()
        if len(results) != 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "This student is already exist"))
        else:
            cursor.execute('''
                INSERT INTO Students (StudentID, StudentName, Sex, EntranceAge, EntranceYear, Class)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', [Student_ID, Student_Name, Sex, Entrance_Age, Entrance_Year, Class])
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Insert"))
            cursor.execute('''
                INSERT INTO AccountPassword (Account, Occupation, Password)
                VALUES (?, ?, ?)
                ''', [Student_ID, "student", "123456"])
        db.commit()
    def Update(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        if not Student_ID.isdigit() or len(Student_ID) != 10:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        cursor.execute(f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\'')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no this student"))
            return
        Student_Name = self.lineEdit_Student_Name.text()
        if len(Student_Name) != 0 and not Student_Name.isalpha():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student Name must be English characters"))
            return
        Sex = self.lineEdit_Sex.text()
        if Sex not in ['male', 'female', '']:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Sex must be \'male\' or \'female\'"))
            return
        Entrance_Age = self.lineEdit_Entrance_Age.text()
        if len(Entrance_Age) != 0 and not Entrance_Age.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance Age must in range [10,50]"))
            return
        if len(Entrance_Age) != 0 and not 10 <= int(Entrance_Age) <= 50:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance_Age must in range [10,50]"))
            return
        Entrance_Year = self.lineEdit_Entrance_Year.text()
        if len(Entrance_Year) != 0 and not Entrance_Year.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Entrance Year must a decimal number"))
            return
        Class = self.lineEdit_Class.text()
        if Class != '':
            for i in Class:
                if i in specific_character:
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Class should not contain \\, /, :, ?, \", \', <, >, |"))
                    return
        if Student_Name == '':
            Student_Name = results[0][1]
        if Sex == '':
            Sex = results[0][2]
        if Entrance_Age == '':
            Entrance_Age = results[0][3]
        Entrance_Age = int(Entrance_Age)
        if Entrance_Year == '':
            Entrance_Year = results[0][4]
        Entrance_Year = int(Entrance_Year)
        if Class == '':
            Class = results[0][5]
        cursor.execute('''
                    UPDATE Students 
                    SET StudentName=?, Sex=?, EntranceAge=?, EntranceYear=?, Class=?
                    WHERE StudentID=?
                    ''', [Student_Name, Sex, Entrance_Age, Entrance_Year, Class, Student_ID])
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Update"))
        db.commit()
    def Delete(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        if not Student_ID.isdigit() or len(Student_ID) != 10:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        cursor.execute(f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\';')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
            return
        cursor.execute(f'DELETE FROM Students WHERE StudentID=\'{Student_ID}\'')
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Delete"))
        cursor.execute(f'DELETE FROM AccountPassword WHERE Account=\'{Student_ID}\'')
        db.commit()
class Course_Info_Modify_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(451, 465)
        self.label_Query_Line = QtWidgets.QLabel(Form)
        self.label_Query_Line.setGeometry(PyQt5.QtCore.QRect(10, 10, 431, 20))
        self.label_Query_Line.setObjectName("label_5")
        self.label_Query_Course_ID = QtWidgets.QLabel(Form)
        self.label_Query_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 47, 120, 16))
        self.label_Query_Course_ID.setObjectName("label")
        self.label_Modify_Line = QtWidgets.QLabel(Form)
        self.label_Modify_Line.setGeometry(PyQt5.QtCore.QRect(10, 80, 431, 20))
        self.label_Modify_Line.setObjectName("label_4")
        self.label_Modify_Course_ID = QtWidgets.QLabel(Form)
        self.label_Modify_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 100, 120, 16))
        self.label_Modify_Course_ID.setObjectName("label_7")
        self.label_Course_Name = QtWidgets.QLabel(Form)
        self.label_Course_Name.setGeometry(PyQt5.QtCore.QRect(20, 130, 120, 20))
        self.label_Course_Name.setObjectName("label_6")
        self.label_Teacher_ID = QtWidgets.QLabel(Form)
        self.label_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(20, 160, 120, 20))
        self.label_Teacher_ID.setObjectName("label_3")
        self.label_Credit = QtWidgets.QLabel(Form)
        self.label_Credit.setGeometry(PyQt5.QtCore.QRect(20, 190, 120, 20))
        self.label_Credit.setObjectName("label_9")
        self.label_Grade = QtWidgets.QLabel(Form)
        self.label_Grade.setGeometry(PyQt5.QtCore.QRect(20, 220, 120, 20))
        self.label_Grade.setObjectName("label_8")
        self.label_Canceled_Year = QtWidgets.QLabel(Form)
        self.label_Canceled_Year.setGeometry(PyQt5.QtCore.QRect(20, 250, 120, 20))
        self.label_Canceled_Year.setObjectName("label_10")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 280, 451, 20))
        self.label_Query_Result.setObjectName("label_11")
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.Button_Query_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Query_Course_Info.setGeometry(PyQt5.QtCore.QRect(300, 30, 141, 50))
        self.Button_Query_Course_Info.setObjectName("pushButton")
        self.Button_Query_Course_Info.clicked.connect(self.Query)
        self.Button_Insert = QtWidgets.QPushButton(Form)
        self.Button_Insert.setGeometry(PyQt5.QtCore.QRect(300, 100, 141, 51))
        self.Button_Insert.setObjectName("pushButton_2")
        self.Button_Insert.clicked.connect(self.Insert)
        self.Button_Update = QtWidgets.QPushButton(Form)
        self.Button_Update.setGeometry(PyQt5.QtCore.QRect(300, 160, 141, 51))
        self.Button_Update.setObjectName("pushButton_3")
        self.Button_Update.clicked.connect(self.Update)
        self.Button_Delete = QtWidgets.QPushButton(Form)
        self.Button_Delete.setGeometry(PyQt5.QtCore.QRect(300, 220, 141, 51))
        self.Button_Delete.setObjectName("pushButton_4")
        self.Button_Delete.clicked.connect(self.Delete)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(190, 435, 75, 24))
        self.Button_Back.setObjectName("pushButton_5")
        self.Button_Back.clicked.connect(lambda: self.back.emit())

        self.lineEdit_Query_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Query_Course_ID.setGeometry(PyQt5.QtCore.QRect(140, 47, 150, 20))
        self.lineEdit_Query_Course_ID.setObjectName("lineEdit")
        self.lineEdit_Modify_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Modify_Course_ID.setGeometry(PyQt5.QtCore.QRect(140, 100, 150, 20))
        self.lineEdit_Modify_Course_ID.setObjectName("lineEdit_5")
        self.lineEdit_Course_Name = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_Name.setGeometry(PyQt5.QtCore.QRect(140, 130, 150, 20))
        self.lineEdit_Course_Name.setObjectName("lineEdit_4")
        self.lineEdit_Teacher_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(140, 160, 150, 20))
        self.lineEdit_Teacher_ID.setObjectName("lineEdit_3")
        self.lineEdit_Credit = QtWidgets.QLineEdit(Form)
        self.lineEdit_Credit.setGeometry(PyQt5.QtCore.QRect(140, 190, 150, 20))
        self.lineEdit_Credit.setObjectName("lineEdit_7")
        self.lineEdit_Grade = QtWidgets.QLineEdit(Form)
        self.lineEdit_Grade.setGeometry(PyQt5.QtCore.QRect(140, 220, 150, 20))
        self.lineEdit_Grade.setObjectName("lineEdit_6")
        self.lineEdit_Canceled_Year = QtWidgets.QLineEdit(Form)
        self.lineEdit_Canceled_Year.setGeometry(PyQt5.QtCore.QRect(140, 250, 150, 20))
        self.lineEdit_Canceled_Year.setObjectName("lineEdit_8")

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(10, 306, 431, 120))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Course Info Modify"))
        self.label_Query_Line.setText(_translate("Form", "----------------------Query---------------------"))
        self.label_Query_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Modify_Line.setText(_translate("Form", "---------------------Modify---------------------"))
        self.label_Modify_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Course_Name.setText(_translate("Form", "Course Name"))
        self.label_Teacher_ID.setText(_translate("Form", "Teacher ID"))
        self.label_Credit.setText(_translate("Form", "Credit"))
        self.label_Grade.setText(_translate("Form", "Grade"))
        self.label_Canceled_Year.setText(_translate("Form", "Canceled Year"))
        self.label_Query_Result.setText(_translate("Form", "Operation Result"))

        self.Button_Query_Course_Info.setText(_translate("Form", "Query Course\nInfo"))
        self.Button_Insert.setText(_translate("Form", "Insert"))
        self.Button_Update.setText(_translate("Form", "Update"))
        self.Button_Delete.setText(_translate("Form", "Delete"))
        self.Button_Back.setText(_translate("Form", "Back"))
    def Query(self):
        global db
        Course_ID = self.lineEdit_Query_Course_ID.text()
        cursor = db.cursor()
        if Course_ID != '':
            if not Course_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
                return
            sql = f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\' ORDER BY CourseID;'
        else:
            sql = 'SELECT * FROM Courses ORDER BY CourseID;'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
    def Insert(self):
        global db
        cursor = db.cursor()
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        Course_Name = self.lineEdit_Course_Name.text()
        for i in Course_Name:
            if i in specific_character:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Course Name should not contain \\, /, :, ?, \", \', <, >, |"))
                return
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 5 digit decimal number"))
            return
        cursor.execute(f"SELECT * FROM Teachers WHERE TeacherID=\'{Teacher_ID}\'")
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched Teacher"))
            return
        Credit = self.lineEdit_Credit.text()
        if not Credit.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Credit must be a float number"))
            return
        Credit = float(Credit)
        Grade = self.lineEdit_Grade.text()
        if not Grade.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Grade must be an integer number"))
            return
        Grade = int(Grade)
        if not 1 <= Grade <= 5:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Grade must in range [1,5]"))
            return
        Canceled_Year = self.lineEdit_Canceled_Year.text()
        if Canceled_Year != '':
            if not Canceled_Year.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Canceled Year must be an integer number or empty"))
                return
            Canceled_Year = int(Canceled_Year)
        cursor.execute(f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\'')
        results = cursor.fetchall()
        if len(results) != 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "This course is already exist"))
        else:
            if Canceled_Year == '':
                cursor.execute('''
                    INSERT INTO Courses (CourseID, CourseName, TeacherID, Credit, Grade)
                    VALUES (?, ?, ?, ?, ?)
                    ''', [Course_ID, Course_Name, Teacher_ID, Credit, Grade])
            else:
                cursor.execute('''
                    INSERT INTO Courses (CourseID, CourseName, TeacherID, Credit, Grade, CanceledYear)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', [Course_ID, Course_Name, Teacher_ID, Credit, Grade, Canceled_Year])
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Insert"))
        db.commit()
    def Update(self):
        global db
        cursor = db.cursor()
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        cursor.execute(f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\'')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched course"))
            return
        Course_Name = self.lineEdit_Course_Name.text()
        if Course_Name != '':
            for i in Course_Name:
                if i in specific_character:
                    self.label_Query_Result.setText(
                        PyQt5.QtCore.QCoreApplication.translate("Form",
                                                                "Course Name should not contain \\, /, :, ?, \", \', <, >, |"))
                    return
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        if Teacher_ID != '':
            if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 5 digit decimal number"))
                return
            cursor.execute(f'SELECT * FROM Teachers WHERE TeacherID=\'{Teacher_ID}\'')
            result = cursor.fetchall()
            if len(result) == 0:
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched Teacher"))
                return
        Credit = self.lineEdit_Credit.text()
        if Credit != '':
            if not Credit.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Credit must be a float number"))
                return
            Credit = float(Credit)
        Grade = self.lineEdit_Grade.text()
        if Grade != '':
            if not Grade.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Grade must be an integer number"))
                return
            Grade = int(Grade)
        Canceled_Year = self.lineEdit_Canceled_Year.text()
        if Canceled_Year != '':
            if not Canceled_Year.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Canceled_Year must be an integer number"))
                return
            Canceled_Year = int(Canceled_Year)
        if Course_Name == '':
            Course_Name = results[0][1]
        if Teacher_ID == '':
            Teacher_ID = results[0][2]
        if Credit == '':
            Credit = results[0][3]
        if Grade == '':
            Grade = results[0][4]
        if Canceled_Year == '':
            Canceled_Year = results[0][5]
        cursor.execute('''
                            UPDATE Courses 
                            SET CourseName=?, TeacherID=?, Credit=?, Grade=?, Canceled_Year=?
                            WHERE CourseID=?
                            ''', [Course_Name, Teacher_ID, Credit, Grade, Canceled_Year, Course_ID])
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Insert"))
        db.commit()
    def Delete(self):
        global db
        cursor = db.cursor()
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        cursor.execute(f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\';')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is matched course"))
            return
        cursor.execute(f'DELETE FROM Courses WHERE CourseID=\'{Course_ID}\'')
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Delete"))
        db.commit()
class Course_Choosing_Info_Modify_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(451, 404)
        self.label_Query_Line = QtWidgets.QLabel(Form)
        self.label_Query_Line.setGeometry(PyQt5.QtCore.QRect(10, 10, 431, 20))
        self.label_Query_Line.setObjectName("label_5")
        self.label_Query_Student_ID = QtWidgets.QLabel(Form)
        self.label_Query_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 33, 120, 20))
        self.label_Query_Student_ID.setObjectName("label_12")
        self.label_Query_Course_ID = QtWidgets.QLabel(Form)
        self.label_Query_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 57, 120, 20))
        self.label_Query_Course_ID.setObjectName("label")
        self.label_Modify_Line = QtWidgets.QLabel(Form)
        self.label_Modify_Line.setGeometry(PyQt5.QtCore.QRect(10, 80, 431, 20))
        self.label_Modify_Line.setObjectName("label_4")
        self.label_Modify_Student_ID = QtWidgets.QLabel(Form)
        self.label_Modify_Student_ID.setGeometry(PyQt5.QtCore.QRect(20, 100, 120, 20))
        self.label_Modify_Student_ID.setObjectName("label_7")
        self.label_Modify_Course_ID = QtWidgets.QLabel(Form)
        self.label_Modify_Course_ID.setGeometry(PyQt5.QtCore.QRect(20, 130, 120, 20))
        self.label_Modify_Course_ID.setObjectName("label_6")
        self.label_Teacher_ID = QtWidgets.QLabel(Form)
        self.label_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(20, 160, 120, 20))
        self.label_Teacher_ID.setObjectName("label_3")
        self.label_Chosen_Year = QtWidgets.QLabel(Form)
        self.label_Chosen_Year.setGeometry(PyQt5.QtCore.QRect(20, 190, 120, 20))
        self.label_Chosen_Year.setObjectName("label_9")
        self.label_Query_Result = QtWidgets.QLabel(Form)
        self.label_Query_Result.setGeometry(PyQt5.QtCore.QRect(0, 219, 451, 20))
        self.label_Query_Result.setObjectName("label_11")
        self.label_Query_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Query_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.Button_Query_Course_Info = QtWidgets.QPushButton(Form)
        self.Button_Query_Course_Info.setGeometry(PyQt5.QtCore.QRect(300, 30, 141, 50))
        self.Button_Query_Course_Info.setObjectName("pushButton")
        self.Button_Query_Course_Info.clicked.connect(self.Query)
        self.Button_Insert = QtWidgets.QPushButton(Form)
        self.Button_Insert.setGeometry(PyQt5.QtCore.QRect(300, 100, 141, 30))
        self.Button_Insert.setObjectName("pushButton_2")
        self.Button_Insert.clicked.connect(self.Insert)
        self.Button_Update = QtWidgets.QPushButton(Form)
        self.Button_Update.setGeometry(PyQt5.QtCore.QRect(300, 140, 141, 30))
        self.Button_Update.setObjectName("pushButton_3")
        self.Button_Update.clicked.connect(self.Update)
        self.Button_Delete = QtWidgets.QPushButton(Form)
        self.Button_Delete.setGeometry(PyQt5.QtCore.QRect(300, 180, 141, 30))
        self.Button_Delete.setObjectName("pushButton_4")
        self.Button_Delete.clicked.connect(self.Delete)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(190, 374, 75, 24))
        self.Button_Back.setObjectName("pushButton_5")
        self.Button_Back.clicked.connect(lambda: self.back.emit())

        self.lineEdit_Query_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Query_Student_ID.setGeometry(PyQt5.QtCore.QRect(140, 33, 150, 20))
        self.lineEdit_Query_Student_ID.setObjectName("lineEdit_8")
        self.lineEdit_Query_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Query_Course_ID.setGeometry(PyQt5.QtCore.QRect(140, 57, 150, 20))
        self.lineEdit_Query_Course_ID.setObjectName("lineEdit")
        self.lineEdit_Modify_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Modify_Student_ID.setGeometry(PyQt5.QtCore.QRect(140, 100, 150, 20))
        self.lineEdit_Modify_Student_ID.setObjectName("lineEdit_5")
        self.lineEdit_Modify_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Modify_Course_ID.setGeometry(PyQt5.QtCore.QRect(140, 130, 150, 20))
        self.lineEdit_Modify_Course_ID.setObjectName("lineEdit_4")
        self.lineEdit_Teacher_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Teacher_ID.setGeometry(PyQt5.QtCore.QRect(140, 160, 150, 20))
        self.lineEdit_Teacher_ID.setObjectName("lineEdit_3")
        self.lineEdit_Chosen_Year = QtWidgets.QLineEdit(Form)
        self.lineEdit_Chosen_Year.setGeometry(PyQt5.QtCore.QRect(140, 190, 150, 20))
        self.lineEdit_Chosen_Year.setObjectName("lineEdit_7")

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(PyQt5.QtCore.QRect(10, 245, 431, 120))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Course Choosing Info Modify"))
        self.label_Query_Line.setText(_translate("Form", "----------------------Query---------------------"))
        self.label_Query_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Query_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Modify_Line.setText(_translate("Form", "---------------------Modify---------------------"))
        self.label_Modify_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Modify_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Teacher_ID.setText(_translate("Form", "Teacher ID"))
        self.label_Chosen_Year.setText(_translate("Form", "Chosen Year"))
        self.label_Query_Result.setText(_translate("Form", "Operation Result"))

        self.Button_Query_Course_Info.setText(_translate("Form", "Query Course\nChoosing Info"))
        self.Button_Insert.setText(_translate("Form", "Insert"))
        self.Button_Update.setText(_translate("Form", "Update"))
        self.Button_Delete.setText(_translate("Form", "Delete"))
        self.Button_Back.setText(_translate("Form", "Back"))
    def Query(self):
        global db
        Student_ID = self.lineEdit_Query_Student_ID.text()
        Course_ID = self.lineEdit_Query_Course_ID.text()
        cursor = db.cursor()
        if Student_ID == '' and Course_ID == '':
            sql = f'SELECT * FROM CourseChoosing ORDER BY StudentID, CourseID;'
        elif Student_ID == '' and Course_ID != '':
            sql = f'SELECT * FROM CourseChoosing WHERE CourseID=\'{Course_ID}\' ORDER BY StudentID, CourseID;'
        elif Student_ID != '' and Course_ID == '':
            sql = f'SELECT * FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' ORDER BY StudentID, CourseID;'
        elif Student_ID != '' and Course_ID != '':
            sql = f'SELECT * FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' AND CourseID=\'{Course_ID}\' ORDER BY StudentID, CourseID;'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) > 0:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Query Result"))
            col_result = cursor.description
            self.row = len(results)  # 取得记录个数，用于设置表格的行数
            self.vol = len(results[0])  # 取得字段数，用于设置表格的列数
            col_result = list(col_result)
            a = 0
            self.tableWidget.setColumnCount(self.vol)
            self.tableWidget.setRowCount(self.row)
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(a, item)
                item = self.tableWidget.horizontalHeaderItem(a)
                item.setText(i[0])
                a = a + 1
            results = list(results)
            for i in range(len(results)):
                results[i] = list(results[i])
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(i, j, item)
                    item = self.tableWidget.item(i, j)
                    item.setText(str(results[i][j]))
        else:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is no data"))
    def Insert(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        Chosen_Year = self.lineEdit_Chosen_Year.text()
        if len(Student_ID) != 10 or not Student_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 5 digit decimal number"))
            return
        if not Chosen_Year.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Chosen Year must be a decimal number"))
            return
        Chosen_Year = int(Chosen_Year)
        cursor.execute(f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\'')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched student"))
            return
        if 1 <= today.month <= 6:
            Chosen_Grade = Chosen_Year - results[0][4]
        else:
            Chosen_Grade = Chosen_Year - results[0][4] + 1
        cursor.execute(f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\'')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched course"))
            return
        Grade = results[0][4]
        if Grade > Chosen_Grade:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                        f"The grade demand of this course is {Grade} while this student is in grade {Chosen_Grade}"))
            return
        if results[0][5] != None and Chosen_Year >= results[0][5]:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", f"Chosen Year must smaller than Canceled Year: {results[0][5]}"))
            return
        flag = False
        for info in results:
            if info[2] == Teacher_ID:
                flag = True
                break
        if not flag:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched teacher"))
            return
        cursor.execute(f'SELECT * FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' AND CourseID=\'{Course_ID}\' AND TeacherID=\'{Teacher_ID}\';')
        results = cursor.fetchall()
        if len(results) != 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "This Course Choosing is already exist"))
            return
        cursor.execute('''
            INSERT INTO CourseChoosing (StudentID, CourseID, TeacherID, ChosenYear)
            VALUES (?, ?, ?, ?)
            ''', [Student_ID, Course_ID, Teacher_ID, Chosen_Year])
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Insert"))
        db.commit()
    def Update(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        Chosen_Year = self.label_Chosen_Year.text()
        if len(Student_ID) != 10 or not Student_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 5 digit decimal number"))
            return
        if Chosen_Year != '':
            if not Chosen_Year.isdigit():
                self.label_Query_Result.setText(
                    PyQt5.QtCore.QCoreApplication.translate("Form", "Chosen Year must be an integer number"))
                return
            Chosen_Year = int(Chosen_Year)
        cursor.execute(f'SELECT * FROM CourseChoosing WHERE CourseID=\'{Course_ID}\' AND StudentID=\'{Student_ID}\' AND TeacherID=\'{Teacher_ID}\';')
        CourseChoosing_Results = cursor.fetchall()
        if len(CourseChoosing_Results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "There is no matched course choosing record"))
            return
        cursor.execute(f'SELECT * FROM Courses WHERE CourseID=\'{Course_ID}\'')
        Courses_results = cursor.fetchall()
        if Chosen_Year != '' and Courses_results[0][5] != None and Chosen_Year >= Courses_results[0][5]:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", f"Chosen Year must smaller than Canceled Year: {Courses_results[0][5]}"))
            return
        cursor.execute(f'SELECT * FROM Students WHERE StudentID=\'{Student_ID}\'')
        Student_results = cursor.fetchall()
        if len(Student_results) == 0:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                        f"There is no matched student"))
            return
        Grade = Courses_results[0][4]
        if 1 <= today.month <= 6:
            Chosen_Grade = Chosen_Year - Student_results[0][4]
        else:
            Chosen_Grade = Chosen_Year - Student_results[0][4] + 1
        if Grade > Chosen_Grade:
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form",
                                                        f"The grade demand of this course is {Grade} while this student is in grade {Chosen_Grade}"))
            return
        if Chosen_Year == '':
            Chosen_Year = CourseChoosing_Results[0][3]
        cursor.execute('''
                    UPDATE CourseChoosing 
                    SET ChosenYear=?
                    WHERE StudentID=? AND CourseID=? AND TeacherID=?
                    ''', [Chosen_Year, Student_ID, Course_ID, Teacher_ID])
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Update"))
        db.commit()
    def Delete(self):
        global db
        cursor = db.cursor()
        Student_ID = self.lineEdit_Modify_Student_ID.text()
        if len(Student_ID) != 10 or not Student_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a 10 digit decimal number"))
            return
        Course_ID = self.lineEdit_Modify_Course_ID.text()
        if len(Course_ID) != 7 or not Course_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a 7 digit decimal number"))
            return
        Teacher_ID = self.lineEdit_Teacher_ID.text()
        if len(Teacher_ID) != 5 or not Teacher_ID.isdigit():
            self.label_Query_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Teacher ID must be a 5 digit decimal number"))
            return
        cursor.execute(f'SELECT * FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' AND CourseID=\'{Course_ID}\' AND TeacherID=\'{Teacher_ID}\';')
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "There is matched Course Choosing"))
            return
        cursor.execute(f'DELETE FROM CourseChoosing WHERE StudentID=\'{Student_ID}\' AND CourseID=\'{Course_ID}\' AND TeacherID=\'{Teacher_ID}\';')
        self.label_Query_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully Delete"))
        db.commit()
class Set_Student_Score_Ui(QtWidgets.QWidget):
    back = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(371, 220)
        self.Button_Set_Score = QtWidgets.QPushButton(Form)
        self.Button_Set_Score.setGeometry(PyQt5.QtCore.QRect(90, 120, 90, 40))
        self.Button_Set_Score.setObjectName("pushButton_2")
        self.Button_Set_Score.clicked.connect(self.set_score)
        self.Button_Back = QtWidgets.QPushButton(Form)
        self.Button_Back.setGeometry(PyQt5.QtCore.QRect(190, 120, 90, 40))
        self.Button_Back.setObjectName("pushButton_1")
        self.Button_Back.clicked.connect(lambda: self.back.emit())
        self.label_Student_ID = QtWidgets.QLabel(Form)
        self.label_Student_ID.setGeometry(PyQt5.QtCore.QRect(30, 30, 100, 16))
        self.label_Student_ID.setObjectName("label")
        self.label_Course_ID = QtWidgets.QLabel(Form)
        self.label_Course_ID.setGeometry(PyQt5.QtCore.QRect(30, 60, 100, 16))
        self.label_Course_ID.setObjectName("label_2")
        self.label_Score = QtWidgets.QLabel(Form)
        self.label_Score.setGeometry(PyQt5.QtCore.QRect(30, 90, 100, 16))
        self.label_Score.setObjectName("label_3")
        self.lineEdit_Student_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Student_ID.setGeometry(PyQt5.QtCore.QRect(140, 30, 201, 20))
        self.lineEdit_Student_ID.setObjectName("lineEdit")
        self.lineEdit_Course_ID = QtWidgets.QLineEdit(Form)
        self.lineEdit_Course_ID.setGeometry(PyQt5.QtCore.QRect(140, 60, 201, 20))
        self.lineEdit_Course_ID.setObjectName("lineEdit_2")
        self.lineEdit_Score = QtWidgets.QLineEdit(Form)
        self.lineEdit_Score.setGeometry(PyQt5.QtCore.QRect(140, 90, 201, 20))
        self.lineEdit_Score.setObjectName("lineEdit_3")
        self.label_Operation_Result = QtWidgets.QLabel(Form)
        self.label_Operation_Result.setGeometry(PyQt5.QtCore.QRect(0, 170, 371, 40))
        self.label_Operation_Result.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Operation_Result.setObjectName("label_4")
        self.label_Operation_Result.setStyleSheet("color: rgb(250, 0, 0);")

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def set_score(self):
        global db
        global userID
        StudentID = self.lineEdit_Student_ID.text()
        if not StudentID.isdigit() or len(StudentID) != 10:
            self.label_Operation_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Student ID must be a\n10 digit decimal number"))
            return
        CourseID = self.lineEdit_Course_ID.text()
        if not CourseID.isdigit() or len(CourseID) != 7:
            self.label_Operation_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Course ID must be a\n7 digit decimal number"))
            return
        new_score = self.lineEdit_Score.text()
        if not new_score.isdigit() or not 0 <= float(new_score) <= 100:
            self.label_Operation_Result.setText(
                PyQt5.QtCore.QCoreApplication.translate("Form", "Score must be a real number\nin range [0,100]"))
            return
        cursor = db.cursor()
        sql = f'SELECT * FROM CourseChoosing WHERE TeacherID=\'{userID}\' AND CourseID=\'{CourseID}\' AND StudentID=\'{StudentID}\' ORDER BY ChosenYear DESC;'
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            self.label_Operation_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "You have no permission"))
            return
        Chosen_Year = results[0][3]
        sql = f'UPDATE CourseChoosing SET Score=\'{float(new_score)}\' WHERE CourseID=\'{CourseID}\' AND StudentID=\'{StudentID}\' AND ChosenYear=\'{Chosen_Year}\';'
        cursor.execute(sql)
        self.label_Operation_Result.setText(PyQt5.QtCore.QCoreApplication.translate("Form", "Successfully set score"))
        db.commit()
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Set Student's Score"))
        self.Button_Set_Score.setText(_translate("Form", "Set Score"))
        self.Button_Back.setText(_translate("Form", "Back"))
        self.label_Student_ID.setText(_translate("Form", "Student ID"))
        self.label_Course_ID.setText(_translate("Form", "Course ID"))
        self.label_Score.setText(_translate("Form", "Score"))
        self.label_Operation_Result.setText(_translate("Form", "Operation Result"))
class Change_Password_Ui(QtWidgets.QWidget):
    ret = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        Form = self
        Form.setObjectName("Form")
        Form.resize(400, 160)
        self.lineEdit_Original_Password = QtWidgets.QLineEdit(Form)
        self.lineEdit_Original_Password.setGeometry(PyQt5.QtCore.QRect(180, 20, 191, 20))
        self.lineEdit_Original_Password.setObjectName("lineEdit_2")
        self.lineEdit_New_Password = QtWidgets.QLineEdit(Form)
        self.lineEdit_New_Password.setGeometry(PyQt5.QtCore.QRect(180, 50, 191, 20))
        self.lineEdit_New_Password.setObjectName("lineEdit_3")
        self.label_Original_Password = QtWidgets.QLabel(Form)
        self.label_Original_Password.setGeometry(PyQt5.QtCore.QRect(10, 20, 160, 20))
        self.label_Original_Password.setObjectName("label")
        self.label_New_Password = QtWidgets.QLabel(Form)
        self.label_New_Password.setGeometry(PyQt5.QtCore.QRect(55, 50, 150, 20))
        self.label_New_Password.setObjectName("label_2")
        self.Button_Modify = QtWidgets.QPushButton(Form)
        self.Button_Modify.setGeometry(PyQt5.QtCore.QRect(120, 80, 75, 24))
        self.Button_Modify.setObjectName("pushButton")
        self.Button_Modify.clicked.connect(self.Modify_Password)
        self.Button_Return = QtWidgets.QPushButton(Form)
        self.Button_Return.setGeometry(PyQt5.QtCore.QRect(210, 80, 75, 24))
        self.Button_Return.setObjectName("pushButton_2")
        self.Button_Return.clicked.connect(self.send_ret_signal)
        self.label_Original_Password_Error = QtWidgets.QLabel(Form)
        self.label_Original_Password_Error.setGeometry(PyQt5.QtCore.QRect(0, 110, 400, 40))
        self.label_Original_Password_Error.setObjectName("label_3")
        self.label_Original_Password_Error.setVisible(False)
        self.label_Original_Password_Error.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label_Original_Password_Error.setStyleSheet("color: rgb(250, 0, 0);")

        self.retranslateUi(Form)
        PyQt5.QtCore.QMetaObject.connectSlotsByName(Form)
    def Modify_Password(self):
        global userID
        original_password = self.lineEdit_Original_Password.text()
        for i in original_password:
            if i in specific_character:
                self.label_Original_Password_Error.setText(
                    QtCore.QCoreApplication.translate("Form", "Original Password should not contain\n\\, /, :, ?, \", \', <, >, |"))
                self.label_Original_Password_Error.setVisible(True)
                return
        new_password = self.lineEdit_New_Password.text()
        for i in new_password:
            if i in specific_character:
                self.label_Original_Password_Error.setText(
                    QtCore.QCoreApplication.translate("Form", "New Password Should not contain\n\\, /, :, ?, \", \', <, >, |"))
                self.label_Original_Password_Error.setVisible(True)
                return
        cursor = db.cursor()
        sql = f"select * from AccountPassword where Account=\'{userID}\';"
        cursor.execute(sql)
        results = cursor.fetchall()
        if str(results[0][2]) != original_password:
            self.label_Original_Password_Error.setText(QtCore.QCoreApplication.translate("Form", "Original Password Error"))
            self.label_Original_Password_Error.setVisible(True)
            return
        if len(new_password) == 0:
            self.label_Original_Password_Error.setText(QtCore.QCoreApplication.translate("Form", "Password should not be empty"))
            self.label_Original_Password_Error.setVisible(True)
            return
        sql = f'UPDATE AccountPassword SET Password=\'{new_password}\' WHERE Account=\'{userID}\';'
        cursor.execute(sql)
        self.label_Original_Password_Error.setText(
            QtCore.QCoreApplication.translate("Form", "Successfully Modify"))
        self.label_Original_Password_Error.setVisible(True)
        db.commit()
    def send_ret_signal(self):
        self.ret.emit()
    def retranslateUi(self, Form):
        _translate = PyQt5.QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Change Password"))
        self.label_Original_Password.setText(_translate("Form", "Original Password"))
        self.Button_Modify.setText(_translate("Form", "Modify"))
        self.label_New_Password.setText(_translate("Form", "New Password"))
        self.label_Original_Password_Error.setText(_translate("Form", "Original Password Error"))
        self.Button_Return.setText(_translate("Form", "Return"))
class Controller:
    def show_login(self):
        self.login = Login_Ui()
        self.login.admin_window.connect(self.show_admin)
        self.login.teacher_window.connect(self.show_teacher)
        self.login.student_window.connect(self.show_student)
        self.login.show()
    def show_admin(self):
        self.admin = Admin_Ui()
        self.admin.cp.connect(self.show_change_password)
        self.admin.query.connect(self.show_query)
        self.admin.mi.connect(self.show_modify_info)
        self.admin.logout.connect(self.back_login)
        self.admin.show()
        self.login.close()
    def show_teacher(self):
        self.teacher = Teacher_Ui()
        self.teacher.lo.connect(self.back_login)
        self.teacher.query.connect(self.show_query)
        self.teacher.cp.connect(self.show_change_password)
        self.teacher.sss.connect(self.show_set_student_score)
        self.teacher.show()
        self.login.close()
    def show_student(self):
        self.student = Student_Ui()
        self.student.logout.connect(self.back_login)
        self.student.query.connect(self.show_query)
        self.student.change.connect(self.show_change_password)
        self.student.show()
        self.login.close()
    def show_query(self):
        if userChar == "admin":
            self.admin.close()
        elif userChar == "teacher":
            self.teacher.close()
        elif userChar == "student":
            self.student.close()
        self.query = Query_Ui()
        self.query.stu_info.connect(self.show_student_info_query)
        self.query.stu_score.connect(self.show_student_score_info_query)
        self.query.cou_info.connect(self.show_course_info_query)
        self.query.ti.connect(self.show_teacher_info_query)
        self.query.ave_score.connect(self.show_average_score_info_query)
        self.query.bs.connect(self.back_from_query)
        self.query.show()
    def back_from_query(self):
        self.query.close()
        if userChar == "admin":
            self.show_admin()
        elif userChar == "teacher":
            self.show_teacher()
        elif userChar == "student":
            self.show_student()
    def show_student_info_query(self):
        self.query.close()
        self.ssiq = Student_Info_Query_Ui()
        self.ssiq.back.connect(self.show_student_info_query_back_query)
        self.ssiq.show()
    def show_teacher_info_query(self):
        self.query.close()
        self.stiq = Teaching_Info_Query_Ui()
        self.stiq.back.connect(self.show_teacher_info_query_back_query)
        self.stiq.show()
    def show_teacher_info_query_back_query(self):
        self.stiq.close()
        self.query.show()
    def show_student_info_query_back_query(self):
        self.ssiq.close()
        self.query.show()
    def show_student_score_info_query(self):
        self.query.close()
        self.sssiq = Student_Score_Query_Ui()
        self.sssiq.back.connect(self.show_student_scor_info_query_back_query)
        self.sssiq.show()
    def show_student_scor_info_query_back_query(self):
        self.sssiq.close()
        self.query.show()
    def show_course_info_query(self):
        self.query.close()
        self.sciq = Course_Info_Query_Ui()
        self.sciq.back.connect(self.show_course_info_query_back_to_query)
        self.sciq.show()
    def show_course_info_query_back_to_query(self):
        self.sciq.close()
        self.query.show()
    def show_average_score_info_query(self):
        self.query.close()
        self.sasiq = Average_Score_Info_Query_Ui()
        self.sasiq.back.connect(self.show_average_score_info_query_back_to_query)
        self.sasiq.show()
    def show_average_score_info_query_back_to_query(self):
        self.sasiq.close()
        self.query.show()
    def show_set_student_score(self):
        self.teacher.close()
        self.ssss = Set_Student_Score_Ui()
        self.ssss.back.connect(self.set_score_to_teacher)
        self.ssss.show()
    def set_score_to_teacher(self):
        self.ssss.close()
        self.teacher.show()
    def show_modify_info(self):
        self.modify = Modify_Info_Ui()
        self.modify.show()
        self.modify.stu_info.connect(self.show_student_info_modify)
        self.modify.cou_info.connect(self.show_course_info_modify)
        self.modify.coc_info.connect(self.show_course_choosing_info_modify)
        self.modify.bs.connect(self.back_from_modify)
        self.modify.show()
        self.admin.close()
    def back_from_modify(self):
        self.modify.close()
        self.admin.show()
    def show_student_info_modify(self):
        self.modify.close()
        self.ssim = Student_Info_Modify_Ui()
        self.ssim.back.connect(self.back_to_modify_from_ssim)
        self.ssim.show()
    def back_to_modify_from_ssim(self):
        self.ssim.close()
        self.modify.show()
    def show_course_info_modify(self):
        self.modify.close()
        self.scim = Course_Info_Modify_Ui()
        self.scim.back.connect(self.back_to_modify_from_scim)
        self.scim.show()
    def back_to_modify_from_scim(self):
        self.scim.close()
        self.modify.show()
    def show_course_choosing_info_modify(self):
        self.modify.close()
        self.sccim = Course_Choosing_Info_Modify_Ui()
        self.sccim.back.connect(self.back_to_modify_from_sccim)
        self.sccim.show()
    def back_to_modify_from_sccim(self):
        self.sccim.close()
        self.modify.show()
    def back_login(self):
        if userChar == "admin":
            self.admin.close()
        elif userChar == "teacher":
            self.teacher.close()
        elif userChar == "student":
            self.student.close()
        self.show_login()
    def show_change_password(self):
        if userChar == "admin":
            self.admin.close()
        elif userChar == "teacher":
            self.teacher.close()
        elif userChar == "student":
            self.student.close()
        self.CP = Change_Password_Ui()
        self.CP.ret.connect(self.change_password_return)
        self.CP.show()
    def change_password_return(self):
        self.CP.close()
        if userChar == "admin":
            self.show_admin()
        elif userChar == "teacher":
            self.show_teacher()
        elif userChar == "student":
            self.show_student()
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
