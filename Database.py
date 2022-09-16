from datetime import datetime
import sqlite3
class Database:
    def __init__(self,user):
        self.data="data.db"
        self.day=int(datetime.now().strftime('%j'))
        self.conn = None
        self.user=user

        
        try:
            self.conn = sqlite3.connect(self.data)
            
        except Error as e:
            print(e)

    def authenticate(self,password):
        query="select * from users where userid='"+self.user+"'"
        
        try :
            self.conn = sqlite3.connect(self.data)
            c = self.conn.cursor()
            c.execute(query)
            ans=c.fetchall()
           # print(ans)
            if ans:
                query="select * from users where userid='"+self.user+"' AND + password='"+password+"'"
                c.execute(query)
                self.conn.commit()
                if c.fetchall():
                    return 1
                return "Incorrect Password"
            else:
                return "Username doesn't exist"
        except:
            return "Something went Wrong,Please try again after sometime"
        
    def add_users(self,password):
        query="select * from users where userid='"+self.user+"'"
        try :
            c = self.conn.cursor()
            c.execute(query)
            ans=c.fetchall()
            
            if not ans:
                query="Insert into users values('"+self.user+"','"+password+"')"
                c.execute(query)
                self.conn.commit()
                return "Account created Successfully, Click on Log in below to navigate through login page"
            else:
                return "Username already taken ,Please try something else"
        except:
            return "Something went Wrong,Please try again after sometime"
            
    def create_challenge(self, c_name,desc,count):
        insert="Insert into alltables values('"+c_name+"',"+str(count)+",'"+desc+"')"
        tb=""" CREATE TABLE IF NOT EXISTS """+c_name+""" (
                                        uid char(10),
                                        start_d int,
                                        pre_d int
                                    ); """
        
        try:
            self.conn = sqlite3.connect(self.data)
            c = self.conn.cursor()
           # print('insert')
            c.execute(insert)
           # print('itb')
            c.execute(tb)
            self.conn.commit()
            return True
        except Error as e:
          #  print(e)
            return False
    def check(self,table):
        self.conn = sqlite3.connect(self.data)
        cursorObj = self.conn.cursor()
        query='SELECT pre_d-start_d,pre_d from '+table+' where uid="'+self.user+'"'
        query2='SELECT count from alltables where name="'+table+'"'
       # print(query2)
        cursorObj.execute(query)
        a=cursorObj.fetchall()
        cursorObj = self.conn.cursor()
       # print(query2)
        cursorObj.execute(query2)
        b=cursorObj.fetchall()
        #print("n",b)
        #print(a,b,table)
        if a and a[0][0]==b[0][0]:
            return ["CHALLENGE COMPLETE",a[0][0]]
        elif a and self.day-a[0][1]<2:
            return ["SEE YOU TOMMORROW" if a[0][1]==self.day else "TODAY STREAK MISSING",a[0][0]]
        elif a:
            query='Delete from '+table+' where uid="'+self.user+'"'
            cursorObj.execute(query)
            self.conn.commit()
        return ["START CHALLENGE",0]
        
    
    def fetch(self):
        self.conn = sqlite3.connect(self.data)
        cursorObj = self.conn.cursor()
        cursorObj.execute('SELECT * from alltables ')
        arr=[]
        for table in cursorObj.fetchall():
            a,b=self.check(table[0])
            arr.append([table[0],a,b,table[2]])
        return arr

    def update(self,table):
        self.conn = sqlite3.connect(self.data)
        cursorObj = self.conn.cursor()
        query='SELECT pre_d from '+table+' where uid="'+self.user+'"'
        #print(query)
        cursorObj.execute(query)
        tmp=cursorObj.fetchall()
        if tmp:
            query='UPDATE '+table+ ' set pre_d='+str(self.day) +' where uid="'+self.user+'";'
            
        else:
            query='Insert into '+table+ ' values("'+self.user+'",'+ str(self.day-1)+','+str(self.day)+')'
        #print(query)
        cursorObj.execute(query)
        self.conn.commit()
        return 0
               
            
            
