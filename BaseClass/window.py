from tkinter import *
 
def main():   
    tk = Tk()
    label = Label(tk,text ='Welcome to Python Tkinter')
    button = Button(tk,text = "Click Me")
    label.pack()
    button.pack()
    tk.mainloop()
    
if __name__ == '__main__':
    main()