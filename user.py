import sqlalchemy
import tkinter as tk
from tkinter import ttk
import re

class user:
    def __init__(self,db_url):
        self.engine = sqlalchemy.create_engine(db_url)
        self.meta= sqlalchemy.MetaData()
        self.meta.reflect(self.engine)
        self.connection = self.engine.connect()

    def login(self,userName,password):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_NAME']==userName,self.meta.tables['user'].c['PASSWORD']==password)
        result=self.connection.execute(query).fetchall()
        if (result):
            return True
            
        else:
            return False
               

    def register(self,username,fullname,password,role):
        if(self.checkuser(username,password)):
            query= self.meta.tables['user'].insert().values(USER_NAME=username,FULL_NAME=fullname,PASSWORD=password,ROLE=role)
            result=self.connection.execute(query)
            self.connection.commit()
            if(result):
                return True
            else:
                return False
        else:
            return False


    def checkuser(self,username,password):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_NAME']==username,self.meta.tables['user'].c['PASSWORD']==password)
        result=self.connection.execute(query).fetchall()
        if (not result):
            return True
        else:
            return False


    def checkuserId(self,id):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_ID']==id)
        result=self.connection.execute(query).fetchall()
        if (not result):
            return True
        else:
            return False
 
    
    def getAllUsers(self):
        query= self.meta.tables['user'].select()
        result=self.connection.execute(query).fetchall()
        return result
    
    
    def getUserInformation(self,id):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_ID']==id)
        result=self.connection.execute(query).fetchall()
        return result


    def getUserById(self,id):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_ID']==id)
        result=self.connection.execute(query).fetchall()
        return result
    
    
    def getUserId(self,username):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_NAME']==username)
        result=self.connection.execute(query).fetchall()
        return result[0][0]
    
    
    def getUserRole(self,username):
        query= self.meta.tables['user'].select().where(self.meta.tables['user'].c['USER_NAME']==username)
        result=self.connection.execute(query).fetchall()
        return result[0][4]


    def deleteUser(self,id):
        if(self.checkuserId(id)):
            False
        else:
            query= self.meta.tables['user'].delete().where(self.meta.tables['user'].c['USER_ID']==id)
            result=self.connection.execute(query)
            self.connection.commit()
            return True
    
    
    def editUser(self,oldData,newData,columnEdited):
        query= self.meta.tables['user'].update().values({f'{columnEdited}':newData}).where(self.meta.tables['user'].c[f'{columnEdited}']==oldData)
        result=self.connection.execute(query)
        self.connection.commit()
        if(result):
            return True
        else:
            return False  


    def getAllPosts(self,id):
        query=self.meta.tables['post'].select().where(self.meta.tables['post'].c['USERID']==id)
        result=self.connection.execute(query).fetchall()
        return result
