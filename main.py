import tkinter as tk
import subprocess as sub
import summonAuto as sa

class Application(tk.Frame):
    def say_hi(self):
        output = "hi there, everyone!"
        self.text.insert("end", output) 


    def run(self):
        # p = sub.Popen('python D:\Code\python\summonAuto\run.py',stdout=sub.PIPE,stderr=sub.PIPE) 
        # output, errors = p.communicate() 
        sa.run_by_piont("dragon")
        self.text.insert("end", sa.log) 

    def createWidgets(self):

        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello",
        # self.hi_there["command"] = self.say_hi

        # self.hi_there.pack({"side": "left"})
        

        self.Run = tk.Button(self)
        self.Run["text"] = "Run",
        self.Run["command"] = self.run

        self.Run.pack({"side": "left"})

        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "X"
        # self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        

        self.text = tk.Text(root)
        self.text.pack()

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
# root.destroy()