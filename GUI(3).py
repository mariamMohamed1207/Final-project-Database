import tkinter as tk
from tkinter import ttk
import user as userfile
import post as postfile
import comment as commentfile
import connect

userClass=userfile.user(connect.db_url)
postClass = postfile.post(connect.db_url)
commentClass = commentfile.comment(connect.db_url)

#window
win=tk.Tk()
win.geometry("865x500")
win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)

#functions
def goToRegister():
    registerFrame.tkraise()

def goToLogin():
    loginFrame.tkraise()

def login(username,password):
    if(userClass.login(username.get(),password.get())):
        ttk.Label(loginSuccessfulFrame,text=f'welcom {username.get()}',font=('Helvetica bold',30)).grid(column=0,row=0,padx=200,pady=20)
        ttk.Label(loginSuccessfulFrame,text='******************************',font=('Helvetica bold',30)).grid(column=0,row=1)

        tk.Button(loginSuccessfulFrame,text='User page',command=user,background='#cde1f3').grid(column=0,row=2,pady=3)
        tk.Button(loginSuccessfulFrame,text='Post page',background='#e5bdbd',command=post).grid(column=0,row=3,pady=3)
        tk.Button(loginSuccessfulFrame,text='Comment page',command=comment,background='#efe1d3').grid(column=0,row=4,pady=3)
        
        loginSuccessfulFrame.tkraise()
    else:
        ttk.Label(loginFrame,text='wrong username or password',foreground='red').grid(column=1,row=20)

def register(username,fullname,password,role):
    if(userClass.register(username.get(),fullname.get(),password.get(),checkbox_var.get())):
       confirmDataFrame.tkraise()
    else:
        ttk.Label(registerFrame,text='user already exists go to log in').grid(column=1,row=20)

def user():
    userFrame.tkraise()
    
    #table
    table=ttk.Treeview(userFrame)
    table.place(x=100,y=100)
    
    def checkRole():
        if(userClass.getUserRole(username_var.get())==1):
            allUsers=userClass.getAllUsers()
            return allUsers
        elif(userClass.getUserRole(username_var.get())==2):
            allUsers=userClass.getUserInformation(userClass.getUserId(username_var.get())) 
            return allUsers

    userData=userClass.meta.tables["user"].c.keys()
    table["columns"]=userData
    table.column("#0", width=0, stretch=tk.NO)
    table.heading("#0", text="")
        
    for col in userData :
        table.column(col, width=150, stretch=tk.NO)
        table.heading(col, text=col)

    allUsers=checkRole()

    if(allUsers):
        for user in allUsers:
            table.insert(parent="", index="end",iid=user[0], values=list(user))
         
    def getData():
        result=table.focus()
        return result

      #BTN
    addUserBtn = tk.Button(userFrame,text="Add User",command=lambda:addUser(User_Name_var,User_fullname_var,User_password_var,checkbox_var,entries=[User_Name_entry,User_fullname_entry,User_password_entry]),background='#ffa79c').place(x=100,y=350)
    DeleteUserBtn = tk.Button(userFrame,text="Delete User",command=lambda:delete_user(getData()),background='#cde1f3').place(x=500,y=350)
    EditUserBtn = tk.Button(userFrame,text="Edit User",command=lambda:editUser(User_edit_var,User_edit_new_var,User_edit_old_var,entries=[User_edit_entry,User_edit_new_entry,User_edit_old_entry]),background='#e7cde4').place(x=320,y=350)
    backBtn = tk.Button(userFrame,text="Back",command=loginSuccessfulFrame.tkraise,background='#CCCCFF').place(x=680,y=350)
    
def addUser(username,fullname,password,role,entries=[]):   
    if(userClass.register(username.get(),fullname.get(),password.get(),checkbox_var.get())):
        for entry in entries:
            entry.delete(0)
        user()
    else:
        ttk.Label(userFrame,text='There was an error, please check your data and try again').pack()

def delete_user(id):
    if(userClass.deleteUser(id)):
        user()
    else:
        ttk.Label(userFrame,text="There was an error, please check your data and try again").pack()
        
def editUser(columnEdited,newData,oldData,entries=[]):
    if(userClass.editUser(oldData.get(),newData.get(),columnEdited.get())):
        for entry in entries:
            entry.delete(0)
        loginSuccessfulFrame.tkraise()
    else:
       ttk.Label(userFrame,text='There was an error, please check your data and try again').pack()


def comment():
    commentFrame.tkraise()
    
    #table
    table=ttk.Treeview(commentFrame)
    table.place(x=100,y=100)
    
    def checkRole():
        if(userClass.getUserRole(username_var.get())==1):
            allComments=commentClass.getAllComments()
            if(allComments):
                return allComments
        elif(userClass.getUserRole(username_var.get())==2):
            allComments=commentClass.getAllUserComments(userClass.getUserId(username_var.get()))
            if(allComments):
                return allComments

    commentData=commentClass.meta.tables["comment"].c.keys()
    table["columns"]=commentData
    table.column("#0", width=0, stretch=tk.NO)
    table.heading("#0", text="")
        
    for col in commentData :
        table.column(col, width=150, stretch=tk.NO)
        table.heading(col, text=col)

    allComments=checkRole()

    if(allComments):
        for comment in allComments:
            table.insert(parent="", index="end",iid=comment[0], values=list(comment))
    
        
    def getData():
        result=table.focus()
        return result
        
    #BTN
    addCommentBtn = tk.Button(commentFrame,text="Add Comment",command=lambda:addComment(commentContent_var,userClass.getUserId(username_var.get()),commentContentEntry),background='#ffa79c').place(x=100,y=350)
    DeleteCommentBtn = tk.Button(commentFrame,text="Delete Comment",command=lambda:deleteComment(getData(),commentContentEntry),background='#cde1f3').place(x=200,y=350)
    EditCommentBtn = tk.Button(commentFrame,text="Edit Comment",command=lambda:editComment(commentClass.getCommentContent(getData()),commentContent_var.get(),commentContentEntry),background='#e7cde4').place(x=320,y=350)
    SearchCommentBtn = tk.Button(commentFrame,text="Search Comment",command=lambda:searchComment(commentContent_var.get(),username_var,commentContentEntry),background='#c6d5b9').place(x=420,y=350)
    backBtn = tk.Button(commentFrame,text="Back",command=loginSuccessfulFrame.tkraise,background='#CCCCFF').place(x=540,y=350)

    
    #comment content entry
    ttk.Label(commentFrame,text='Comment Content:').place(x=100,y=400)
    commentContent_var=tk.StringVar()
    commentContentEntry=tk.Entry(commentFrame,textvariable=commentContent_var,bg='#efe1d3')
    commentContentEntry.place(x=100,y=430)   

def addComment(commentContent,userId,entry):   
    if(commentClass.addComment(commentContent.get(),userId)):
        comment()
        entry.delete(0)
    else:
        ttk.Label(commentFrame,text='There was an error, please check your data and try again').pack()

def deleteComment(id,entry):
    if(commentClass.deleteComment(id)):
        comment()
        entry.delete(0)
    else:
        ttk.Label(commentFrame,text="There was an error, please check your data and try again").pack()

def searchComment(data,username_var,entry):
    result=commentClass.search(data)
    if(result):
        tableResult=ttk.Treeview(commentFrame)
        tableResult.place(x=100,y=100)
        
        def checkRole():
            if(userClass.getUserRole(username_var.get())==1):
                allComments=commentClass.getCommentById(result)
                return allComments
            elif(userClass.getUserRole(username_var.get())==2):
                allComments=commentClass.getCommentById(commentClass.searchUser(data,userClass.getUserId(username_var.get())))
                return allComments

        commentData=commentClass.meta.tables["comment"].c.keys()
        tableResult["columns"]=commentData
        tableResult.column("#0", width=0, stretch=tk.NO)
        tableResult.heading("#0", text="")
            
        for col in commentData :
            tableResult.column(col, width=150, stretch=tk.NO)
            tableResult.heading(col, text=col)

        allComments=checkRole()

        for comment in allComments:
            tableResult.insert(parent="", index="end",iid=comment[0], values=list(comment[0])) 
        
        entry.delete(0)
    else:
        ttk.Label(commentFrame,text="No Result").pack()

def editComment(oldData,newData,entry):
    if(commentClass.editComment(oldData,newData)):
        comment()
        entry.delete(0)
    else:
       ttk.Label(commentFrame,text='There was an error, please check your data and try again').pack() 
       
def post():
    postFrame.tkraise()
    
    #table
    table=ttk.Treeview(postFrame)
    table.place(x=100,y=100)
    
    def checkRole():
        if(userClass.getUserRole(username_var.get())==1):
            allPosts=postClass.getAllPosts()
            if(allPosts):
                return allPosts
        elif(userClass.getUserRole(username_var.get())==2):
            allPosts=postClass.getAllUserPosts(userClass.getUserId(username_var.get()))
            if(allPosts):
                return allPosts

    postData=postClass.meta.tables["post"].c.keys()
    table["columns"]=postData
    table.column("#0", width=0, stretch=tk.NO)
    table.heading("#0", text="")
        
    for col in postData :
        table.column(col, width=150, stretch=tk.NO)
        table.heading(col, text=col)

    allPosts=checkRole()

    if(allPosts):
        for post in allPosts:
            table.insert(parent="", index="end",iid=post[0], values=list(post))
    
        
    def getData():
        result=table.focus()
        return result
        
    #BTN
    addPostBtn = tk.Button(postFrame,text="Add Post",command=lambda:addPost(postContentVar,postNameVar,userClass.getUserId(username_var.get()),entries=[postContentEntry,postNameEntry]),background='#ffa79c').place(x=100,y=350)
    DeletePostBtn = tk.Button(postFrame,text="Delete Post",command=lambda:deletePost(getData()),background='#cde1f3').place(x=500,y=350)
    EditPostBtn = tk.Button(postFrame,text="Edit Post",command=lambda:editPost(postColunmVar,postNewTextVar,postOldTextVar,entries=[postColunmEntry,postOldTextEntry,postNewTextEntry]),background='#e7cde4').place(x=320,y=350)
    backBtn = tk.Button(postFrame,text="Back",command=loginSuccessfulFrame.tkraise,background='#CCCCFF').place(x=600,y=350)

    
    #post content entry
    ttk.Label(postFrame,text='Post Content:').place(x=100,y=400)
    postContentVar=tk.StringVar()
    postContentEntry=tk.Entry(postFrame,textvariable=postContentVar,bg='#efe1d3')
    postContentEntry.place(x=100,y=420)   
    
    #post name entry
    ttk.Label(postFrame,text='Post name:').place(x=100,y=450)
    postNameVar=tk.StringVar()
    postNameEntry=tk.Entry(postFrame,textvariable=postNameVar,bg='#efe1d3')
    postNameEntry.place(x=100,y=470)
    
    #post colunm entry
    ttk.Label(postFrame,text='Which column to edit:').place(x=320,y=400)
    postColunmVar=tk.StringVar()
    postColunmEntry=tk.Entry(postFrame,textvariable=postColunmVar,bg='#efe1d3')
    postColunmEntry.place(x=320,y=420) 
    
    #post old text entry
    ttk.Label(postFrame,text='Current data:').place(x=320,y=450)
    postOldTextVar=tk.StringVar()
    postOldTextEntry=tk.Entry(postFrame,textvariable=postOldTextVar,bg='#efe1d3')
    postOldTextEntry.place(x=320,y=470)  
        
    #post new text entry
    ttk.Label(postFrame,text='New data:').place(x=320,y=500)
    postNewTextVar=tk.StringVar()
    postNewTextEntry=tk.Entry(postFrame,textvariable=postNewTextVar,bg='#efe1d3')
    postNewTextEntry.place(x=320,y=520) 
    
def addPost(postContent,postName,userId,entries=[]):   
    if(postClass.addPost(postName.get(),postContent.get(),userId)):
        post()
        for entry in entries:
            entry.delete(0)
    else:
        ttk.Label(postFrame,text='There was an error, please check your data and try again').pack()

def deletePost(id):
    if(postClass.deletePost(id)):
        post()
    else:
        ttk.Label(postFrame,text="There was an error, please check your data and try again").pack()

def editPost(columnEdited,newData,oldData,entries=[]):
    if(postClass.editPost(oldData.get(),newData.get(),columnEdited.get())):
        for entry in entries:
            entry.delete(0)
        loginSuccessfulFrame.tkraise()
    else:
       ttk.Label(postFrame,text='There was an error, please check your data and try again').pack()


#frames

#login frame
loginFrame=ttk.Frame(win)
loginFrame.grid(column=0,row=0,sticky=tk.NSEW)
title=ttk.Label(loginFrame,text='Login',font=('Helvetica bold',20)).grid(column=1,row=1)

#login successful frame
loginSuccessfulFrame=ttk.Frame(win)
loginSuccessfulFrame.grid(column=0,row=0,sticky=tk.NSEW)

#register frame
registerFrame=ttk.Frame(win)
registerFrame.grid(column=0,row=0,sticky=tk.NSEW)

#comment frame
commentFrame=ttk.Frame(win)
commentFrame.grid(column=0,row=0,sticky=tk.NSEW)

#user frame
userFrame=ttk.Frame(win)
userFrame.grid(column=0,row=0,sticky=tk.NSEW)

#confirm data frame
confirmDataFrame=ttk.Frame(win)
confirmDataFrame.grid(column=0,row=0,sticky=tk.NSEW)

#post frame
postFrame=ttk.Frame(win)
postFrame.grid(column=0,row=0,sticky=tk.NSEW)


#user Frame

#username entry
ttk.Label(userFrame,text='Username:').place(x=100,y=400)
User_Name_var=tk.StringVar()
User_Name_entry=tk.Entry(userFrame,textvariable=User_Name_var,bg='#efe1d3')
User_Name_entry.place(x=100,y=420)

#user fullname entry
ttk.Label(userFrame,text='Full Name:').place(x=100,y=450)
User_fullname_var=tk.StringVar()
User_fullname_entry=tk.Entry(userFrame,textvariable=User_fullname_var,bg='#efe1d3')
User_fullname_entry.place(x=100,y=470)

#user password entry
ttk.Label(userFrame,text='Password:').place(x=100,y=500)
User_password_var=tk.StringVar()
User_password_entry=tk.Entry(userFrame,textvariable=User_password_var,bg='#efe1d3')
User_password_entry.place(x=100,y=520)
     
#user edit entry
ttk.Label(userFrame,text='Which column to edit:').place(x=320,y=400)
User_edit_var=tk.StringVar()
User_edit_entry=tk.Entry(userFrame,textvariable=User_edit_var,bg='#efe1d3')
User_edit_entry.place(x=320,y=420)
        
#user edit old entry
ttk.Label(userFrame,text='Current data:').place(x=320,y=450)
User_edit_old_var=tk.StringVar()
User_edit_old_entry=tk.Entry(userFrame,textvariable=User_edit_old_var,bg='#efe1d3')
User_edit_old_entry.place(x=320,y=470)

#user edit new entry
ttk.Label(userFrame,text='New data:').place(x=320,y=500)
User_edit_new_var=tk.StringVar()
User_edit_new_entry=tk.Entry(userFrame,textvariable=User_edit_new_var,bg='#efe1d3')
User_edit_new_entry.place(x=320,y=520)
            
#role
checkbox_var= tk.IntVar()
ttk.Checkbutton(userFrame, text="Admin", variable=checkbox_var, onvalue=1).place(x=100,y=550)
ttk.Checkbutton(userFrame, text="User", variable=checkbox_var, onvalue=2).place(x=180,y=550)
#login frame

#username
ttk.Label(loginFrame,text='Username:',font=('Helvetica bold',15)).grid(column=0,row=5)
username_var=tk.StringVar()
usernameEntry=tk.Entry(loginFrame,textvariable=username_var,bg='#efe1d3').grid(column=1,row=5)

#password
ttk.Label(loginFrame,text='Password:',font=('Helvetica bold',15)).grid(column=0,row=6)
password_var=tk.StringVar()
passwordEntry=tk.Entry(loginFrame,textvariable=password_var,bg='#efe1d3',show='*').grid(column=1,row=6)

#login btn
tk.Button(loginFrame,text='Login',command=lambda:login(username_var,password_var),background='#e5bdbd',font=('Helvetica bold',10)).grid(column=0,row=7)

#register btn
tk.Button(loginFrame,text='Register',command=goToRegister,background='#cde1f3',font=('Helvetica bold',10)).grid(column=1,row=7)


#confirm data frame 

#username
ttk.Label(confirmDataFrame,text='Username:',font=('Helvetica bold',15)).grid(column=0,row=5)
confirmUsername_var=tk.StringVar()
confirmUsernameEntry=tk.Entry(confirmDataFrame,textvariable=username_var,bg='#efe1d3').grid(column=1,row=5)

#password
ttk.Label(confirmDataFrame,text='Password:',font=('Helvetica bold',15)).grid(column=0,row=6)
confirmPassword_var=tk.StringVar()
confimPasswordEntry=tk.Entry(confirmDataFrame,textvariable=password_var,bg='#efe1d3',show='*').grid(column=1,row=6)

#confirmation btn
tk.Button(confirmDataFrame,text='Confirm',command=lambda:login(username_var,password_var),background='#e5bdbd',font=('Helvetica bold',10)).grid(column=0,row=7)

#back to register btn
tk.Button(confirmDataFrame,text='Back',command=goToRegister,background='#cde1f3',font=('Helvetica bold',10)).grid(column=1,row=7)

#register frame
title=ttk.Label(registerFrame,text='Register',font=('Helvetica bold',20),anchor='center').grid(column=1,row=1)

# username - register
ttk.Label(registerFrame,text='Username:',font=('Helvetica bold',15)).grid(column=0,row=2)
register_username_var=tk.StringVar()
registerusernameEntry=tk.Entry(registerFrame,textvariable=register_username_var,bg='#efe1d3').grid(column=1,row=2)

#fullname
ttk.Label(registerFrame,text='Fullname:',font=('Helvetica bold',15),anchor='center').grid(column=0,row=3)
register_fullname_var=tk.StringVar()
fullname_RegisterEntry=tk.Entry(registerFrame,textvariable=register_fullname_var,bg='#efe1d3').grid(column=1,row=3)

#password
ttk.Label(registerFrame,text='Password:',font=('Helvetica bold',15),anchor='center').grid(column=0,row=7)
register_password_var=tk.StringVar()
password_RegisterEntry=tk.Entry(registerFrame,textvariable=register_password_var,bg='#efe1d3',show='*').grid(column=1,row=7)

#role
checkbox_var= tk.IntVar()

#checking btns
ttk.Checkbutton(registerFrame, text="Admin", variable=checkbox_var, onvalue=1).grid(column=0,row=8)
ttk.Checkbutton(registerFrame, text="User", variable=checkbox_var, onvalue=2).grid(column=1,row=8)

# btns in register
tk.Button(registerFrame,text='Login',command=goToLogin,background='#e5bdbd',font=('Helvetica bold',10)).grid(column=0,row=12)
tk.Button(registerFrame,text='Register',background='#cde1f3',command=lambda:register(register_username_var,register_fullname_var,register_password_var,checkbox_var),font=('Helvetica bold',10)).grid(column=1,row=12)


loginFrame.tkraise()
win.mainloop()
