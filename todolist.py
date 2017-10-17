from tkinter import *
from tkinter import font

import sqlite3

conn = sqlite3.connect('tutorial.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE name='table_name'")
if not bool(c.fetchall()):
	c.execute("CREATE TABLE IF NOT EXISTS to_do(id INTEGER PRIMARY KEY AUTOINCREMENT,task TEXT,time TEXT)")

def data_entry(task,time):
    
    c.execute("INSERT INTO to_do (task,time) VALUES (?, ?)",
          (task,time))
    conn.commit()

def modify_task(task,id):
    c.execute('UPDATE to_do SET task=? where id=? ',(task,id))

def modify_time(time,id):
    c.execute('UPDATE to_do SET time=? where id=? ',(time,id))
    conn.commit()
    
def remove(id):
    id=str(id)
    print(id)
    c.execute('DELETE FROM to_do WHERE id=?',(id,))
    conn.commit()

sno={}
num=0
class todoList:
    def __init__(self):
        self.todo=[]
        self.done=[]

    def decode(self,task):
        tsk,time=str.split(task,'|')
        tsk=tsk.strip()
        time=time.strip()
        return tsk,time
		
    def addTask(self,task):
        global num
        num+=1
        tsk,time=self.decode(task)
        data_entry(tsk,time)
        self.todo.append(task)

    def completeTask(self,task):
        if self.todo.count(task)>0:
            self.todo.remove(task)
            print(task)
            self.done.append(task)

    def restoreList(self, file):
        c.execute('SELECT * FROM to_do')
        data = c.fetchall()
        global num
        global sno
        num=len(data)
        t=0
        for row in data:
            todotsk='%-50s | %-50s'%(row[1],row[2])
            self.todo.append(todotsk)
            sno[t]=row[0]
            t+=1
        return self.todo

    def save(self,name):
        c.execute('DELETE FROM to_do')
        conn.commit()

todo=todoList()


class App:
    def __init__(self,master):
        self.todo = todoList()
        self.master = master
        self.frame = Frame(master)
        self.frame.grid()

        self.addButton = Button(self.frame, text="Add", command=self.add)
        self.addButton.grid(row=1, column=5)
        self.saveButton = Button(self.frame, text="Remove All", command=self.save)
        self.saveButton.grid(row=0, column=2)
        self.restoreButton = Button(self.frame, text="Restore", command=self.restore)
        self.restoreButton.grid(row=0, column=1)
        self.button = Button(self.frame, text="Quit", command=self.quit)
        self.button.grid(row=0, column=4)
        self.doneButton = Button(self.frame, text="Done", command=self.done)
        self.doneButton.grid(row=0, column=3)

        label1 = Label(self.frame, text="Commands ")
        label1.grid(row=0, column=0)
		
		#for the input description
        label = Label(self.frame, text="New Task:")
        label.grid(row=1, column=0)
		#actual edit box for input
        self.entry1 = Entry(self.frame)
        self.entry1.grid(row=1, column=1, columnspan=2)
        self.entry2 = Entry(self.frame)
        self.entry2.grid(row=1, column=3, columnspan=2)
		
        frame1 = LabelFrame(self.frame, text="Tasks")
        frame1.grid(columnspan=7, sticky=E+W)
        frame1.columnconfigure(0, weight=1)
        self.tasks = Listbox(frame1)
        self.tasks.grid(sticky=E+W)

        frame2 = LabelFrame(self.frame, text="Completed")
        frame2.grid(columnspan=7, sticky=E+W)
        frame2.columnconfigure(0, weight=1)
        self.completed = Listbox(frame2)
        self.completed.grid(sticky=E+W)

    def save(self):
        self.todo.save("tasks.txt")
        self.tasks.delete(0,END)

    def restore(self):
        items=self.todo.restoreList("tasks.txt")
        for item in items:
            self.tasks.insert(END,item)
        """items = self.todo.getCompleted()
        self.completed.delete(0,END)
        for item in items:
            self.completed.insert(END,item)"""

    def add(self):
        task1 = self.entry1.get()
        task2=self.entry2.get()
        #print(task2)
        task2='%4d'%(int(task2+'0000'))
        task2=task2[:2]+':'+task2[2:4]+' hrs'
        task='%-50s | %-50s'%(task1,task2)
        self.todo.addTask(task)
        self.tasks.insert(END,task)

    def done(self):
        global sno
        selection = self.tasks.curselection()
        if len(selection) == 0:
            return
        task = self.tasks.get(selection[0])
        self.todo.completeTask(self.tasks)
        if bool(sno):
            remove(sno[selection[0]])
        else:
            tsk,time=self.todo.decode(task)
            c.execute('SELECT id FROM to_do WHERE task=? AND time=?',(tsk,time))
            val=c.fetchone()
            remove(val[0])
        self.tasks.delete(selection[0])
        self.completed.insert(END,task)
		
    def quit(self):
        self.frame.quit()
        self.master.destroy()


root = Tk()
app = App(root)
root.mainloop()