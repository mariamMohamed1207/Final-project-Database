import sqlalchemy

class post:
    def __init__(self,db_url):
        self.engine = sqlalchemy.create_engine(db_url)
        self.meta= sqlalchemy.MetaData()
        self.meta.reflect(self.engine)
        self.connection = self.engine.connect()


    def addPost(self,POST_NAME,POST_CONTENT,USERID):
        query= self.meta.tables['post'].insert().values(POST_NAME=POST_NAME,POST_CONTENT=POST_CONTENT,USERID=USERID)
        result=self.connection.execute(query)
        self.connection.commit()
        if(result):
            return True
        else:
            return False


    def deletePost(self,id):
        if(self.checkPostId(id)):
            False
        else:
            query= self.meta.tables['post'].delete().where(self.meta.tables['post'].c['POST_ID']==id)
            result=self.connection.execute(query)
            self.connection.commit()
            return True
        
            
    def checkPostId(self,id):
        query= self.meta.tables['post'].select().where(self.meta.tables['post'].c['POST_ID']==id)
        result=self.connection.execute(query).fetchall()
        if (not result):
            return True
        else:
            return False


    def editPost(self,oldData,newData,columnEdited):
        query= self.meta.tables['post'].update().values({f'{columnEdited}':newData}).where(self.meta.tables['post'].c[f'{columnEdited}']==oldData)
        result=self.connection.execute(query)
        self.connection.commit()
        if(result):
            return True
        else:
            return False  
      
        
    def getAllUserPosts(self,id):
        query=self.meta.tables['post'].select().where(self.meta.tables['post'].c['USERID']==id)
        result=self.connection.execute(query).fetchall()
        if(result):
            return result
        else:
            return False
    
    
    def getAllPosts(self):
        query=self.meta.tables['post'].select()
        result=self.connection.execute(query).fetchall()
        if(result):
            return result
        else:
            return False                            
       
 
    def getPostContent(self,id):
        query= self.meta.tables['post'].select().where(self.meta.tables['post'].c['POST_ID']==id)
        result=self.connection.execute(query).fetchall()
        return result[0][1]
    

    def getPostById(self,id=[]):
        posts=[]
        for post in range(len(id)):
            query=self.meta.tables['post'].select().where(self.meta.tables['post'].c['POST_ID']==id[post])
            result=self.connection.execute(query).fetchall()
            posts.append(result)
        return posts