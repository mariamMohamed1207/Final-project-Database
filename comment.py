import sqlalchemy

class comment:
    def __init__(self,db_url):
        self.engine = sqlalchemy.create_engine(db_url)
        self.meta= sqlalchemy.MetaData()
        self.meta.reflect(self.engine)
        self.connection = self.engine.connect()


    def addComment(self,COMMENT_CONTENT,USERID):
        query= self.meta.tables['comment'].insert().values(COMMENT_CONTENT=COMMENT_CONTENT,USERID=USERID)
        result=self.connection.execute(query)
        self.connection.commit()
        if(result):
            return True
        else:
            return False
  
  
    def checkCommentId(self,id):
        query= self.meta.tables['comment'].select().where(self.meta.tables['comment'].c['COMMENT_ID']==id)
        result=self.connection.execute(query).fetchall()
        if (not result):
            return True
        else:
            return False
        
        
    def deleteComment(self,id):
        if(self.checkCommentId(id)):
            False
        else:
            query= self.meta.tables['comment'].delete().where(self.meta.tables['comment'].c['COMMENT_ID']==id)
            result=self.connection.execute(query)
            self.connection.commit()
            return True


    def editComment(self,oldData,newData):
        query= self.meta.tables['comment'].update().values({'COMMENT_CONTENT':newData}).where(self.meta.tables['comment'].c['COMMENT_CONTENT']==oldData)
        result=self.connection.execute(query)
        self.connection.commit()
        if(result):
            return True
        else:
            return False
     
    
    def getCommentContent(self,id):
        query= self.meta.tables['comment'].select().where(self.meta.tables['comment'].c['COMMENT_ID']==id)
        result=self.connection.execute(query).fetchall()
        return result[0][1]
    
    
    def search(self,data):
        query=self.meta.tables['comment'].select().where(self.meta.tables['comment'].c['COMMENT_CONTENT'].like(f"%{data}%"))
        result=self.connection.execute(query).fetchall()
        if(result):
            commentId=[]
            for e in range(len(result)):
                commentId.append(result[e][0])
            return commentId
        else:
            return False
    
    def getAllUserComments(self,id):
        query=self.meta.tables['comment'].select().where(self.meta.tables['comment'].c['USERID']==id)
        result=self.connection.execute(query).fetchall()
        if(result):
            return result
        else:
            return False
    
    
    def getAllComments(self):
        query=self.meta.tables['comment'].select()
        result=self.connection.execute(query).fetchall()
        if(result):
            return result
        else:
            return False
    

    def getCommentById(self,id=[]):
        comments=[]
        for comment in range(len(id)):
            query=self.meta.tables['comment'].select().where(self.meta.tables['comment'].c['COMMENT_ID']==id[comment])
            result=self.connection.execute(query).fetchall()
            comments.append(result)
        return comments
            