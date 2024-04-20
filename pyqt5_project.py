import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sqlite3

app = QApplication(sys.argv)
main_window = QWidget()
# con = QSqlDatabase.addDatabase("QSQLITE")
# con.setDatabaseName("notes.sqlite")

conn = sqlite3.connect('notes.db')
# cursor object
cursor = conn.cursor()
# drop query
cursor.execute("DROP TABLE IF EXISTS notes")
# create query
query = """
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            date_start TIMESTAMP,
            date_end TIMESTAMP,
            date_created TIMESTAMP,
            date_modified TIMESTAMP
        )
        """
cursor.execute(query)
# commit and close
conn.commit()
conn.close()

def submitData(title, description, date_start, date_end):
    conn = sqlite3.connect('notes.db')
    conn.execute("INSERT INTO notes (title, description, date_start, date_end) "
                 "VALUES (?, ?, ?, ?)", (title, description, date_start, date_end))
    # conn.execute("INSERT INTO NOTES (ID,NAME,ROLL,ADDRESS,CLASS) "
    #             "VALUES (1, 'John', '001', 'Bangalore', '10th')")
    # conn.execute("INSERT INTO STUDENT (ID,NAME,ROLL,ADDRESS,CLASS) "
    #             "VALUES (2, 'Naren', '002', 'Hyd', '12th')")
    conn.commit()
    conn.close()
    print("Judul notes",title)
    print("Description notes", description)
    print("Date start", date_start)
    print("Date end", date_end)
    print("Submit data executed")
    return (title, description, date_start, date_end)

def deleteData(self):
    print("Judul notes" + self.title)
    print("Description notes" + self.description)
    print("Delete data executed")

def checkConnectionDb():
    if conn.open():
        return True
    print("Database Error: %s" % conn.lastError().databaseText())
    return False
        
def createTable():
    createTableQuery = QSqlQuery()
    createTableQuery.exec(
        """
        CREATE TABLE NOTES (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            date_start TIMESTAMP,
            date_end TIMESTAMP,
            date_created TIMESTAMP,
            date_modified TIMESTAMP
        )
        """
    )
    cursor.execute(query)
    # commit and close
    conn.commit()
    conn.close()

def mainWindow():

    main_layout = QHBoxLayout()
    child_layout = QVBoxLayout()
    date_layout = QHBoxLayout()
    listView = QListWidget()
    login_layout = QHBoxLayout()

    et_title = QTextEdit()
    et_description = QPlainTextEdit()
    addButton = QPushButton("Submit")
    editButton = QPushButton("Edit")
    deleteButton = QPushButton("Delete")
    loginButton = QPushButton("Login")

    et_timeStart = QDateTimeEdit()
    et_timeEnd = QDateTimeEdit()

    et_username = QLineEdit()
    et_password = QLineEdit()

    child_layout.addLayout(login_layout)
    child_layout.addWidget(loginButton)
    child_layout.addWidget(et_title)
    et_title.setPlaceholderText("Masukkan judul") 
    child_layout.addLayout(date_layout)
    child_layout.addWidget(et_description)
    et_description.setPlaceholderText("Masukkan deskripsi") 
    date_layout.addWidget(et_timeStart)
    date_layout.addWidget(et_timeEnd)
    child_layout.addWidget(addButton)
    child_layout.addWidget(editButton)
    login_layout.addWidget(et_username)
    login_layout.addWidget(et_password)
    et_username.setPlaceholderText("Username")
    et_password.setPlaceholderText("Password")

    addButton.clicked.connect(lambda : addDataToList(et_title.toPlainText(), et_description.toPlainText()))
    
    child_layout.addWidget(deleteButton)
    main_layout.addWidget(listView)

    main_window.setLayout(main_layout)
    main_layout.addLayout(child_layout)
    child_layout.addLayout(date_layout)
    # main_layout.addWidget(addButton)
    # main_layout.addWidget(deleteButton)

    def addDataToList(title, description):
        start_time = et_timeStart.dateTime().toString("MM/dd/yyyy HH:mm")
        end_time = et_timeEnd.dateTime().toString("MM/dd/yyyy HH:mm")
        data = submitData(title, description, start_time, end_time)
        listView.addItem("Judul: " + data[0] + ", Deskripsi: " + data[1] + "\n(" + data[2] + " - " + data[3] + ")")

    def deleteData():
        selected = listView.currentItem()
        row = listView.row(selected)
        listView.takeItem(row)
    
    def editData(title, description):
        selected = listView.currentItem()
        row = listView.row(selected)
        start_time = et_timeStart.dateTime().toString("MM/dd/yyyy HH:mm")
        end_time = et_timeEnd.dateTime().toString("MM/dd/yyyy HH:mm")
        data = submitData(title, description, start_time, end_time)
        new_item = QListWidgetItem("Judul: " + data[0] + ", Deskripsi: " + data[1] + "\n(" + data[2] + " - " + data[3] + ")")
        listView.takeItem(row)
        listView.insertItem(row, new_item)

    editButton.clicked.connect(lambda: editData(et_title.toPlainText(), et_description.toPlainText()))
    deleteButton.clicked.connect(deleteData)

    main_window.show()


if __name__ == '__main__':
    # createTable()
    mainWindow()
    main_window.setGeometry(600,400,600,400)
    main_window.setWindowTitle("PyQt")

    sys.exit(app.exec_())
