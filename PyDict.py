#--Author Rohit Kumar
from tkinter import*
from tkinter import ttk
import threading

import requests
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary
import enchant 

d = enchant.Dict("en_US") 
dictionary=PyDictionary()
root = Tk()
root.title("PyDict")
root.geometry("600x750+1000+100")
root.config(bg="white")
root.wm_iconbitmap('dict.ico')
#-----Frame---------------------------------
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Comic Sans MS','15'))

tab=ttk.Notebook(root)
##tab_parent.configure(background='#147852')
syno=Frame(tab, bg='white')
anto=Frame(tab, bg='white')
define=Frame(tab, bg='white')

tab.add(define,text="  Meaning  ")
tab.add(syno,text="  synonyms  ")
tab.add(anto,text="  anotnyms  ")
tab.place(x=0,y=250,width=600,height=400)
#--to style Button--------------------------

style = ttk.Style()
style.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )
style.configure('TButton', font = 
               ('calibri',23, 'bold'), 
                    borderwidth = '1')
#----------------------------------------
#----To style Entry Widget------------#rote it
Estyle = ttk.Style()
Estyle.configure('TEntry', foreground = 'green')
#-------------------------------------------

#---to Display Image "dict.png"-------------------
canvas=Canvas(root,width=53,height=58)
canvas.place(x=100,y=20)
profile=PhotoImage(file='dict.png')
canvas.create_image(0,0,anchor=NW,image=profile)
#-----------------------------------------------------
Label(text="PyDict",bg='white',font=('Comic Sans MS', 45),fg='#d76737').pack()

sm=Label(text="Search The Meaning Of The Word",bg='white',font=('Comic Sans MS',20),fg='#d76737')
sm.place(x=10,y=300)

word=''
#---this function is used to show hint below the Entry widget
def word_hint(word):
    label_no=1
    if word.isspace() or word=='':
        y1=100
        for i in range(4):
            eval('l'+str(label_no)).config(text='')
            eval('l'+str(label_no)).place(x=10,y=y1)
            y1+=20
            label_no+=1
    else:
        wd=[]
        d.check(word)
        arr=d.suggest(word) 
        for i in arr:
            if word==i[:len(word)]:
                wd.append(i)
        if len(wd)<5:
            for i in range(5-len(wd)):
                wd.append('')
        no=1
        y1=100
        for w in wd[:4]:
            eval('l'+str(no)).config(text=w)
            eval('l'+str(no)).place(x=10,y=y1)
            no=no+1
            y1+=33

l1=Label(bg='white',font=('Comic Sans MS', 18),fg='#d76737')
l1.place(x=10,y=130)

l2=Label(bg='white',font=('Comic Sans MS', 18),fg='#d76737')
l2.place(x=10,y=150)

l3=Label(bg='white',font=('Comic Sans MS', 18),fg='#d76737')
l3.place(x=10,y=170)

l4=Label(bg='white',font=('Comic Sans MS', 18),fg='#d76737')
l4.place(x=10,y=190)

means=Text(define,foreground='black',font=('Comic Sans MS', 12),width=45,height=2)
Syno=Text(syno,foreground='black',font=('Comic Sans MS', 12),width=45,height=2)
Anto=Text(anto,foreground='black',font=('Comic Sans MS', 12),width=45,height=2)
def click(key):
    global word,arr
    word=word+key.char
    return word_hint(word)
def back(key):
    global word,arr
    word=word[:-1]
    return word_hint(word)
value=''
def opposit():
    global value
    Anto.delete('1.0','end')
    Anto.config(foreground='#258528',font=('Comic Sans MS', 15))
    Anto.insert(END,'Searching....')
    Anto.place(x=10,y=5)

    antonyms=[]
    source=requests.get("https://www.thesaurus.com/browse/"+value).text
    soup=BeautifulSoup(source,'lxml')
    
    match=soup.find('main',class_="css-1ebf8b3 eavft172")
    match=soup.find_all('ul',class_="css-1ytlws2 et6tpn80")
    a=1
    for i in match:
       if a==1:
          a=a+1
          continue
       ul=i
    match=ul.find_all('span',class_="css-133coio etbu2a32")
    for i in match:
       antonyms.append(i.text)
    Anto.config(foreground='black')
    Anto.delete('1.0','end')
    a=1
    for i in antonyms:
          Anto.insert(END,'=> '+i+'\n')
    Anto.config(height=10)

def similar():
    Syno.delete('1.0','end')
    global value
    Syno.config(foreground='#258528',font=('Comic Sans MS', 15))
    Syno.insert(END,'Searching....')
    Syno.place(x=10,y=5)
    Synonym=[]
    source=requests.get("https://www.thesaurus.com/browse/"+value).text
    soup=BeautifulSoup(source,'lxml')
    match=soup.find('ul',class_="css-1ytlws2 et6tpn80")
    match=match.find_all('span',class_="css-133coio etbu2a32")
    for i in match:
       Synonym.append(i.text)
    Syno.config(foreground='black')
    Syno.delete('1.0','end')
    a=1
    for i in Synonym:
          Syno.insert(END,'=> '+i+'\n')          
    Syno.config(height=10)
       
       
#--This function Run when , user press enter by keyboard
def meaning1():
    global value
    Anto.delete('1.0','end')
    Syno.delete('1.0','end')
    means.delete('1.0','end')
    Syno.insert(END,'Searching....')
    Anto.insert(END,'Searching....')

    value=entry.get()
    sm.place_forget()
    means.config(foreground='#258528',font=('Comic Sans MS', 15))
    means.insert(END,'Searching....')
    means.place(x=10,y=5)
    mean=dictionary.meaning(value)
    means.config(foreground='black')
    means.delete('1.0','end')
    try:
        noun=list(mean.keys())[0]
        txt=value+' : '
        for i in mean[noun]:   
            txt=txt+i+'\n '
        means.insert(END,f'meaning of : {value}'+'\n')
        if len(txt)>152:
            lines=(len(txt)/76)-2
            max_down=2+lines*1.8
            if max_down>9:
                print(max_down)
                means.config(height=9)
                for i in mean[noun]:
                    means.insert(END,'=> '+i+'\n')
                means.place(x=10,y=5)
            else:
                print(max_down)
                means.config(height=max_down)
                for i in mean[noun]:
                    means.insert(END,'=> '+i+'\n')
                means.place(x=10,y=5)

        else:
            if len(txt)>100:
                means.config(height=3)
                means.insert(END,'=> '+txt)
                means.place(x=10,y=5)
            else:
                means.config(height=2.5)
                means.insert(END,'=> '+txt)
                means.place(x=10,y=5)

        length='1.'+str(16+len(value))
        means.tag_add("start", "1.13",length)
        means.tag_config("start", foreground="green")
        line=2
        lst=mean[noun]
        for i in range(len(lst)):
            st=str(line)+".3"
            ed=str(line)+f".{len(lst[i])+3}"
            means.tag_add(f"start{line}",st,ed)
            means.tag_config(f"start{line}", foreground="blue")
            line+=1

    except:
        means.delete('1.0','end')
        means.config(height=2,foreground='green')
        means.insert(END,f'meaning of word ')
        means.insert(END,f'{value}')
        means.insert(END,f' is not found')
        means.place(x=10,y=5)
        length='1.'+str(16+len(value))
        means.tag_add("start", "1.16",length)
        means.tag_config("start", foreground="red")
    threading.Thread(target=similar).start()
    threading.Thread(target=opposit).start()

#--This function Run when , user click Search button
def meaning2():
    global value
    Anto.delete('1.0','end')
    Syno.delete('1.0','end')
    means.delete('1.0','end')
    Syno.insert(END,'Searching....')
    Anto.insert(END,'Searching....')

    value=entry.get()
    sm.place_forget()
    means.config(foreground='#258528',font=('Comic Sans MS', 15))
    means.insert(END,'Searching....')
    means.place(x=10,y=5)
    mean=dictionary.meaning(value)
    means.config(foreground='black')
    means.delete('1.0','end')
    try:
        noun=list(mean.keys())[0]
        txt=value+' : '
        for i in mean[noun]:   
            txt=txt+i+'\n '
        means.insert(END,f'meaning of : {value}'+'\n')
        if len(txt)>152:
            lines=(len(txt)/76)-2
            max_down=2+lines*1.8
            if max_down>9:
                print(max_down)
                means.config(height=9)
                for i in mean[noun]:
                    means.insert(END,'=> '+i+'\n')
                means.place(x=10,y=5)
            else:
                print(max_down)
                means.config(height=max_down)
                for i in mean[noun]:
                    means.insert(END,'=> '+i+'\n')
                means.place(x=10,y=5)

        else:
            if len(txt)>100:
                means.config(height=3)
                means.insert(END,'=> '+txt)
                means.place(x=10,y=5)
            else:
                means.config(height=2.5)
                means.insert(END,'=> '+txt)
                means.place(x=10,y=5)

        length='1.'+str(16+len(value))
        means.tag_add("start", "1.13",length)
        means.tag_config("start", foreground="green")
        line=2
        lst=mean[noun]
        for i in range(len(lst)):
            st=str(line)+".3"
            ed=str(line)+f".{len(lst[i])+3}"
            means.tag_add(f"start{line}",st,ed)
            means.tag_config(f"start{line}", foreground="blue")
            line+=1

    except:
        means.delete('1.0','end')
        means.config(height=2,foreground='green')
        means.insert(END,f'meaning of word ')
        means.insert(END,f'{value}')
        means.insert(END,f' is not found')
        means.place(x=10,y=5)
        length='1.'+str(16+len(value))
        means.tag_add("start", "1.16",length)
        means.tag_config("start", foreground="red")
    threading.Thread(target=similar).start()
    threading.Thread(target=opposit).start()

#--To call meaning1 function using thread so that , window do not get frezz
def call(key):
    threading.Thread(target=meaning1).start()

entry=ttk.Entry(font = ('Comic Sans MS', 22, 'bold'),width=20)
entry.place(x=10,y=100)
entry.focus_set()

btn=ttk.Button(text="search",width=10,command=lambda:threading.Thread(target=meaning2).start(),style='C.TButton')
btn.place(x=376,y=100)


entry.bind("<BackSpace>", back)
entry.bind("<Key>", click)
entry.bind("<Return>",call)

root.mainloop()
#--Rohit Kumar
