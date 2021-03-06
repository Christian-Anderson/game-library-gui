#!/usr/bin/python3
# Christian Anderson
# 2/4/2020

'''A database to store video games with various tags, but this time with a GUI'''

#===[ Import(s) ]===
import pickle
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
#===[ Constant(s) ]===
TITLE_FONT = ("Times New Roman", 24)
BUTTON_FONT = ("Arial", 15)

#===[ Class(es) ]===
class Screen(tk.Frame):
    
    current = 0
    
    def __init__(self):
        tk.Frame.__init__(self)
        
    def switch_frame():
        screens[Screen.current].tkraise()
        
        
class MainMenu(Screen):
    
    def __init__(self):
        Screen.__init__(self)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.lbl_title = tk.Label(self,text="Game Library", font=TITLE_FONT)
        self.lbl_title.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.btn_add = tk.Button(self,text="Add",font=BUTTON_FONT,command=self.go_add)
        self.btn_add.grid(row=1,column=1)
        
        self.btn_edit = tk.Button(self,text="Edit",font=BUTTON_FONT,command=self.go_edit)
        self.btn_edit.grid(row=2,column=1) 
        
        self.btn_search = tk.Button(self,text="Search",font=BUTTON_FONT,command=self.go_search)
        self.btn_search.grid(row=3,column=1)
        
        self.btn_remove = tk.Button(self,text="Remove",font=BUTTON_FONT,command=self.go_remove_choose)
        self.btn_remove.grid(row=4,column=1)
        
        self.btn_save = tk.Button(self,text="Save",font=BUTTON_FONT,command=self.save)    #,command=self.go_save
        self.btn_save.grid(row=5,column=1)  
    
    def go_add(self):
        self.going_add = True
        Screen.current=2
        Screen.switch_frame()
        
    def go_edit(self):
        self.going_add = False
        pop_up = tk.Tk()
        pop_up.title("Edit")
        
        frm_edit_list=ChooseEdit(pop_up)
        frm_edit_list.grid(row=0,column=0)

    def go_search(self):
        Screen.current=1
        Screen.switch_frame()
        
    def go_remove_choose(self):
        pop_up = tk.Tk()
        pop_up.title("Remove")
        
        frm_remove_list=ChooseRemove(pop_up)
        frm_remove_list.grid(row=0,column=0)
        
        #Screen.current=5
        #Screen.switch_frame()
        
    def save(self):
        datafile = open("game_library.pickle", "wb")
        pickle.dump(games, datafile)
        datafile.close()
        messagebox.showinfo(message="Data Saved!")
        
        
    '''def go_save(self):
        Screen.current=2
        Screen.switch_frame()'''
          

class SearchMenu(Screen):
    
    def __init__(self):
        Screen.__init__(self)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.lbl_title = tk.Label(self,text="Search", font=TITLE_FONT)
        self.lbl_title.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.lbl_search_by = tk.Label(self,text="Search by:")
        self.lbl_search_by.grid(row=1,column=0,sticky="sw")
        
        self.options = ["All", "Genre", "Title", "Developer", "Publisher", "Console", "Release Year", "Rating", "# of Players", "Price", "Beaten?", "Purchase Date", "Notes"]
        self.tkvar = tk.StringVar(self)
        self.tkvar.set(self.options[0])
        self.menu = tk.OptionMenu(self, self.tkvar, *self.options)
        self.menu.grid(row=2,column=0,sticky="nw")           
        
        self.lbl_search_for = tk.Label(self,text="Search for:")
        self.lbl_search_for.grid(row=3,column=0,sticky="sw")
        
        self.ent_search_for = tk.Entry(self)
        self.ent_search_for.grid(row=4,column=0,sticky="nw")        
        
        self.lbl_print_filters = tk.Label(self,text="Print Filters:")
        self.lbl_print_filters.grid(row=1,column=1,columnspan=2,sticky="news")
        
        self.frm_filters = PrintFilters(self)
        self.frm_filters.grid(row=2,column=1,rowspan=3,columnspan=2,sticky="news")      
        
        self.scr_search_results = ScrolledText(self,width=40,height=8)
        self.scr_search_results.grid(row=5,column=0,columnspan=3,sticky="news")
        
        self.grid_rowconfigure(5,weight=1)
        
        self.btn_back = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.go_main)
        self.btn_back.grid(row=6,column=0,sticky="news")
        
        self.btn_reset = tk.Button(self,text="Reset",font=BUTTON_FONT,command=self.clear)
        self.btn_reset.grid(row=6,column=1,sticky="news")
        
        self.btn_submit = tk.Button(self,text="Submit",font=BUTTON_FONT,command=self.submit_search)
        self.btn_submit.grid(row=6,column=2,sticky="news")
        
        for key in games.keys():
            entry = games[key]
            self.filter_print(entry)
        
    def go_main(self):
        Screen.current=0
        Screen.switch_frame() 
        
    def filter_print(self, entry):
        if self.frm_filters.genre_var.get() == True:
            msg = entry[1]+"\n"
            self.scr_search_results.insert("insert", msg)
        if self.frm_filters.title_var.get() == True:
            msg = entry[0]+"\n"
            self.scr_search_results.insert("insert", msg)
        if self.frm_filters.company_var.get() == True:
            msg = entry[2]+"\n"
            self.scr_search_results.insert("insert", msg)            
        if self.frm_filters.publisher_var.get() == True:
            msg = entry[3]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.release_var.get() == True:
            msg = entry[5]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.console_var.get() == True:
            msg = entry[4]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.rating_var.get() == True:
            msg = entry[6]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.player_var.get() == True:
            msg = entry[7]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.price_var.get() == True:
            msg = entry[8]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.beaten_var.get() == True:
            msg = entry[9]+"\n"
            self.scr_search_results.insert("insert", msg)  
        if self.frm_filters.purchase_var.get() == True:
            msg = entry[10]+"\n"
            self.scr_search_results.insert("insert", msg) 
        if self.frm_filters.notes_var.get() == True:
            msg = entry[11]+"\n"
            self.scr_search_results.insert("insert", msg)          
        msg = "------------------------------------------------------------\n"
        self.scr_search_results.insert("insert", msg)
        
    def clear(self):
        self.frm_filters.genre_var.set(False)
        self.frm_filters.title_var.set(False)
        self.frm_filters.company_var.set(False)
        self.frm_filters.publisher_var.set(False)
        self.frm_filters.release_var.set(False)
        self.frm_filters.console_var.set(False)
        self.frm_filters.rating_var.set(False)
        self.frm_filters.player_var.set(False)
        self.frm_filters.price_var.set(False)
        self.frm_filters.beaten_var.set(False)
        self.frm_filters.purchase_var.set(False)
        self.frm_filters.notes_var.set(False)
        self.scr_search_results.delete(0.0, "end")
        
    def submit_search(self):
        self.scr_search_results.delete(0.0, "end")
        self.print_search()
            
    def print_search(self):
        self.scr_search_results.delete(0.0, "end")
        keyword = self.ent_search_for.get()
        for key in games.keys():
            entry=games[key]
            if self.tkvar.get() == self.options[0]:
                self.filter_print(entry)
            if self.tkvar.get() == self.options[1]:
                if keyword in entry[0]:
                    self.filter_print(entry)
            if self.tkvar.get() == self.options[2]:
                if keyword in entry[1]:
                    self.filter_print(entry) 
            if self.tkvar.get() == self.options[3]:
                if keyword in entry[2]:
                    self.filter_print(entry) 
            if self.tkvar.get() == self.options[4]:
                if keyword in entry[3]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[5]:
                if keyword in entry[4]:
                    self.filter_print(entry)   
            if self.tkvar.get() == self.options[6]:
                if keyword in entry[5]:
                    self.filter_print(entry)
            if self.tkvar.get() == self.options[7]:
                if keyword in entry[6]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[8]:
                if keyword in entry[7]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[9]:
                if keyword in entry[8]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[10]:
                if keyword in entry[9]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[11]:
                if keyword in entry[10]:
                    self.filter_print(entry)                    
            if self.tkvar.get() == self.options[12]:
                if keyword in entry[11]:
                    self.filter_print(entry) 
                    

class PrintFilters(tk.Frame):
    
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        
        self.genre_var = tk.BooleanVar(self, True)
        self.title_var = tk.BooleanVar(self, True)
        self.company_var = tk.BooleanVar(self, True)
        self.publisher_var = tk.BooleanVar(self, True)
        self.release_var = tk.BooleanVar(self, True)
        self.console_var = tk.BooleanVar(self, True)
        self.rating_var = tk.BooleanVar(self, True)
        self.player_var = tk.BooleanVar(self, True)
        self.price_var = tk.BooleanVar(self, True)
        self.beaten_var = tk.BooleanVar(self, True)
        self.purchase_var = tk.BooleanVar(self, True)
        self.notes_var = tk.BooleanVar(self, True)
        
        self.chk_title = tk.Checkbutton(self,text="Title",variable=self.genre_var)
        self.chk_title.grid(row=0,column=0,sticky="nsw")
        
        self.chk_genre = tk.Checkbutton(self,text="Genre",variable=self.title_var)
        self.chk_genre.grid(row=0,column=1,sticky="nsw")  
        
        self.chk_company = tk.Checkbutton(self,text="Company",variable=self.company_var)
        self.chk_company.grid(row=0,column=2,sticky="nsw")        
        
        self.chk_publisher = tk.Checkbutton(self,text="Publisher",variable=self.publisher_var)
        self.chk_publisher.grid(row=1,column=0,sticky="nsw")        
        
        self.chk_release_year = tk.Checkbutton(self,text="Release Year",variable=self.release_var)
        self.chk_release_year.grid(row=1,column=1,sticky="nsw")        
        
        self.chk_console = tk.Checkbutton(self,text="Console",variable=self.console_var)
        self.chk_console.grid(row=1,column=2,sticky="nsw")        
        
        self.chk_rating = tk.Checkbutton(self,text="Rating",variable=self.rating_var)
        self.chk_rating.grid(row=2,column=0,sticky="nsw")
        
        self.chk_single_multi = tk.Checkbutton(self,text="Single/Multi Player",variable=self.player_var)
        self.chk_single_multi.grid(row=2,column=1,sticky="nsw")         
        
        self.chk_price = tk.Checkbutton(self,text="Price",variable=self.price_var)
        self.chk_price.grid(row=2,column=2,sticky="nsw")
        
        self.chk_beaten = tk.Checkbutton(self,text="Beaten?",variable=self.beaten_var)
        self.chk_beaten.grid(row=3,column=0,sticky="nsw")         
        
        self.chk_purchase_date = tk.Checkbutton(self,text="Date Purchase",variable=self.purchase_var)
        self.chk_purchase_date.grid(row=3,column=1,sticky="nsw")
        
        self.chk_notes = tk.Checkbutton(self,text="Notes",variable=self.notes_var)
        self.chk_notes.grid(row=3,column=2,sticky="nsw")           
        

'''class FileSaved(Screen):
    
    def __init__(self):
        Screen.__init__(self)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.lbl_saved = tk.Label(self,text="File Saved.", font=TITLE_FONT)
        self.lbl_saved.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.btn_edit_confirm = tk.Button(self,text="OK",font=BUTTON_FONT,command=self.go_main)
        self.btn_edit_confirm.grid(row=1,column=1)
        
    def go_main(self):
        Screen.current=0
        Screen.switch_frame()'''     
        
        
class ChooseEdit(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        self.parent = parent
        
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        
        self.lbl_edit_ask = tk.Label(self,text="Which Title to Edit?", font=TITLE_FONT)
        self.lbl_edit_ask.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.options = ["Select a title."]
        for key in games.keys():
            self.options.append(games[key][1])
        self.tkvar = tk.StringVar(self)
        self.tkvar.set(self.options[0])
        self.menu = tk.OptionMenu(self, self.tkvar, *self.options)
        self.menu.grid(row = 1, column = 0, columnspan=3)        
        
        self.btn_cancel = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.cancel)
        self.btn_cancel.grid(row=2,column=0,sticky="news")        
        
        self.btn_edit_choose = tk.Button(self,text="Confirm",font=BUTTON_FONT,command=self.go_add_edit)
        self.btn_edit_choose.grid(row=2,column=2,sticky="news") 
        
    def cancel(self):
        self.parent.destroy()
        
    def go_add_edit(self):
        if self.tkvar.get() == self.options[0]:
            pop_up = tk.Tk()
            pop_up.title("Error")
            msg="ERROR, choose a title"
            frm_error=ErrorMessage(pop_up, msg)
            frm_error.grid(row=0,column=0)            
        else:
            for i in range(len(self.options)):
                if self.tkvar.get() == self.options[i]:
                    screens[2].edit_key = i            
                    break
                
            Screen.current=2
            screens[Screen.current].update()
            Screen.switch_frame()
            self.parent.destroy()
        
        
class AddEdit(Screen):
    
    def __init__(self):
        Screen.__init__(self)
        self.edit_key = 0
        self.button_checked = 0
        self.check_var = tk.BooleanVar(self, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        #self.lbl_title = tk.Label(self,text="Search", font=TITLE_FONT)
        #self.lbl_title.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.lbl_edit_genre = tk.Label(self,text="Genre:")
        self.lbl_edit_genre.grid(row=0,column=0,sticky="sw")
        
        self.ent_edit_genre = tk.Entry(self)
        self.ent_edit_genre.grid(row=0,column=1,sticky="nw")
        
        self.lbl_edit_title = tk.Label(self,text="Title:")
        self.lbl_edit_title.grid(row=0,column=2,sticky="sw")
        
        self.ent_edit_title = tk.Entry(self)
        self.ent_edit_title.grid(row=0,column=3,sticky="nw")
        
        self.lbl_edit_developer = tk.Label(self,text="Developer:")
        self.lbl_edit_developer.grid(row=1,column=0,sticky="sw")
        
        self.ent_edit_developer = tk.Entry(self)
        self.ent_edit_developer.grid(row=1,column=1,sticky="nw") 
        
        self.lbl_edit_publisher = tk.Label(self,text="Publisher:")
        self.lbl_edit_publisher.grid(row=1,column=2,sticky="sw")
        
        self.ent_edit_publisher = tk.Entry(self)
        self.ent_edit_publisher.grid(row=1,column=3,sticky="nw")   
        
        self.lbl_edit_system = tk.Label(self,text="System:")
        self.lbl_edit_system.grid(row=2,column=0,sticky="sw")
        
        self.ent_edit_system = tk.Entry(self)
        self.ent_edit_system.grid(row=2,column=1,sticky="nw") 
        
        self.lbl_edit_release = tk.Label(self,text="Release Date:")
        self.lbl_edit_release.grid(row=2,column=2,sticky="sw")
        
        self.ent_edit_release = tk.Entry(self)
        self.ent_edit_release.grid(row=2,column=3,sticky="nw")        
        
        self.lbl_edit_rating = tk.Label(self,text="Rating:")
        self.lbl_edit_rating.grid(row=3,column=0,sticky="sw")
        
        self.ent_edit_rating = tk.Entry(self)
        self.ent_edit_rating.grid(row=3,column=1,sticky="nw")
        
        self.lbl_edit_price = tk.Label(self,text="Price:")
        self.lbl_edit_price.grid(row=3,column=2,sticky="sw")
        
        self.ent_edit_price = tk.Entry(self)
        self.ent_edit_price.grid(row=3,column=3,sticky="nw")  
        
        self.lbl_edit_purchase = tk.Label(self,text="Purchase Date:")
        self.lbl_edit_purchase.grid(row=4,column=0,sticky="sw")
        
        self.ent_edit_purchase = tk.Entry(self)
        self.ent_edit_purchase.grid(row=4,column=1,sticky="nw")        
        
        self.chk_beaten = tk.Checkbutton(self,text="Beaten?",variable=self.check_var)
        self.chk_beaten.grid(row=4,column=2,sticky="nsw")  
        
        self.lbl_edit_mode = tk.Label(self,text="# of Players:")
        self.lbl_edit_mode.grid(row=5,column=0,sticky="sw")
        
        self.options = ["1", "2", "3", "4"]
        self.tkvar = tk.StringVar(self)
        self.tkvar.set(self.options[0])
        self.menu = tk.OptionMenu(self, self.tkvar, *self.options)
        self.menu.grid(row = 5, column = 1)          
        
        self.lbl_edit_notes = tk.Label(self,text="Notes:")
        self.lbl_edit_notes.grid(row=6,column=0,sticky="sw") 
        
        self.scr_add_edit = ScrolledText(self,width=40,height=8)
        self.scr_add_edit.grid(row=7,column=0,columnspan=3,sticky="news") 
        
        self.btn_back = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.go_main)
        self.btn_back.grid(row=8,column=0,sticky="news")
        
        self.btn_reset = tk.Button(self,text="Reset",font=BUTTON_FONT,command=self.reset)
        self.btn_reset.grid(row=8,column=1,sticky="news")
        
        self.btn_submit = tk.Button(self,text="Submit",font=BUTTON_FONT,command=self.submit)
        self.btn_submit.grid(row=8,column=2,sticky="news")
        
    def update(self):
        entry = games[self.edit_key]
        #self.ent_genre.set(entry[0])
        self.ent_edit_genre.delete(0, "end")
        self.ent_edit_genre.insert(0, entry[0])
        
        self.ent_edit_title.delete(0, "end")
        self.ent_edit_title.insert(0, entry[1])
        
        self.ent_edit_developer.delete(0, "end")
        self.ent_edit_developer.insert(0, entry[2])
        
        self.ent_edit_publisher.delete(0, "end")
        self.ent_edit_publisher.insert(0, entry[3])
        
        self.ent_edit_system.delete(0, "end")
        self.ent_edit_system.insert(0, entry[4])
        
        self.ent_edit_release.delete(0, "end")
        self.ent_edit_release.insert(0, entry[5])
        
        self.ent_edit_rating.delete(0, "end")
        self.ent_edit_rating.insert(0, entry[6])
        
        self.ent_edit_price.delete(0, "end")
        self.ent_edit_price.insert(0, entry[8])  
        
        self.ent_edit_purchase.delete(0, "end")
        self.ent_edit_purchase.insert(0, entry[10])
        
        self.tkvar.set(self.options[int(entry[7])-1])
        
        if entry[9] == "Yes":
            self.button_checked = 1
            self.chk_beaten.toggle()
                
        self.scr_add_edit.delete(0.0, "end")
        self.scr_add_edit.insert(0.0, entry[11])        

        
    def go_main(self):
        self.reset()
        
        Screen.current=0
        Screen.switch_frame() 
        
    def reset(self):
        self.ent_edit_genre.delete(0, "end")
        self.ent_edit_title.delete(0, "end")
        self.ent_edit_developer.delete(0, "end")
        self.ent_edit_publisher.delete(0, "end")
        self.ent_edit_system.delete(0, "end")
        self.ent_edit_release.delete(0, "end")
        self.ent_edit_rating.delete(0, "end")
        self.ent_edit_price.delete(0, "end")
        self.ent_edit_purchase.delete(0, "end")
        self.tkvar.set(self.options[0])
        if self.check_var == True:
            self.chk_beaten.toggle()
        self.scr_add_edit.delete(0.0, "end")          
        
    def submit(self):
        entry = []
        entry.append(self.ent_edit_genre.get())
        entry.append(self.ent_edit_title.get())
        entry.append(self.ent_edit_developer.get())
        entry.append(self.ent_edit_publisher.get())
        entry.append(self.ent_edit_system.get())
        entry.append(self.ent_edit_release.get())
        entry.append(self.ent_edit_rating.get())
        entry.append(self.tkvar.get())                 #self.options.get())
        entry.append(self.ent_edit_price.get())
        #entry.append("Not Determined")
        if self.check_var.get() == True:
            entry.append("Yes")
        else:
            entry.append("No")
        entry.append(self.ent_edit_purchase.get())
        entry.append(self.scr_add_edit.get(0.0,"end"))
        if screens[0].going_add == False:
            games[self.edit_key] = entry
            messagebox.showinfo(message="Entry has been edited.")
        else:
            games[len(games)+1] = entry
            messagebox.showinfo(message="Entry has been added.")
        
        self.reset()
        self.go_main()
        
 
class ChooseRemove(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        self.parent = parent
        self.delete_key = 0
        
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        
        self.lbl_edit_ask = tk.Label(self,text="Which Title to Delete?", font=TITLE_FONT)
        self.lbl_edit_ask.grid(row=0,column=0,columnspan=3,sticky="news")
        
        self.options = ["Select a title."]
        for key in games.keys():
            self.options.append(games[key][1])
        self.tkvar = tk.StringVar(self)
        self.tkvar.set(self.options[0])
        self.menu = tk.OptionMenu(self, self.tkvar, *self.options)
        self.menu.grid(row = 1, column = 0, columnspan=3)        
        
        self.btn_cancel = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.cancel)
        self.btn_cancel.grid(row=2,column=0,sticky="news")        
        
        self.btn_edit_choose = tk.Button(self,text="Confirm",font=BUTTON_FONT,command=self.go_remove)
        self.btn_edit_choose.grid(row=2,column=2,sticky="news")       
        
    def cancel(self):
        self.parent.destroy()
        
    def go_remove(self):
        if self.tkvar.get() == self.options[0]:
            pop_up = tk.Tk()
            pop_up.title("Error")
            msg="ERROR, choose a title"
            frm_error=ErrorMessage(pop_up, msg)
            frm_error.grid(row=0,column=0)    
        else:
            for i in range(len(self.options)):
                if self.tkvar.get() == self.options[i]:
                    screens[3].delete_key = i            
                    break
                
            Screen.current=3
            screens[Screen.current].update()
            Screen.switch_frame()
            self.parent.destroy()
    
    
'''class ChooseRemove(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, master=parent)
        self.parent = parent
        
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        
        self.lbl_remove_ask = tk.Label(self,text="Which Title to Remove?", font=TITLE_FONT)
        self.lbl_remove_ask.grid(row=0,column=0,columnspan=3,sticky="news")
        
        options = ["one", "two"]
        self.tkvar = tk.StringVar(self)
        self.tkvar.set(options[0])
        self.menu = tk.OptionMenu(self, self.tkvar, *options)
        self.menu.grid(row = 1, column = 1)        
        
        self.btn_cancel = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.cancel)
        self.btn_cancel.grid(row=2,column=0,sticky="news")        
        
        self.btn_remove_choose = tk.Button(self,text="Confirm",font=BUTTON_FONT)     #,command=self.go_remove
        self.btn_remove_choose.grid(row=2,column=2,sticky="news") 
    
    def cancel(self):
        self.parent.destroy()
        
    def go_remove(self):
        Screen.current=6
        Screen.switch_frame()    
        
'''              
class ConfirmRemove(Screen):
    
    def __init__(self):
        Screen.__init__(self)
        self.delete_key = 0
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        self.lbl_removal = tk.Label(self,text="These games are", font=TITLE_FONT)
        self.lbl_removal.grid(row=0,column=0,columnspan=3,sticky="news")      
        
        self.lbl_removal = tk.Label(self,text="marked for Removal", font=TITLE_FONT)
        self.lbl_removal.grid(row=1,column=0,columnspan=3,sticky="news")  
        
        self.scr_delete = ScrolledText(self,width=40,height=8)
        self.scr_delete.grid(row=2,column=0,columnspan=3,sticky="news")
        
        self.btn_cancel = tk.Button(self,text="Back",font=BUTTON_FONT,command=self.cancel)
        self.btn_cancel.grid(row=3,column=0,sticky="news")        
        
        self.btn_remove_confirm = tk.Button(self,text="Confirm",font=BUTTON_FONT,command=self.confirm)
        self.btn_remove_confirm.grid(row=3,column=2,sticky="news")
        
    def update(self):
        entry = games[self.delete_key]
        self.scr_delete.delete(0.0, "end")
        to_print = "Title:        " + entry[0] + "\nGenre:        " + entry[1] + "\nDeveloper:    " + entry[2] + "\nPublisher:    " + entry[3] +"\nSystem:       " + entry[4] + "\nRelease Date: " + entry[5] + "\nRating:       " + entry[6] + "\n# of Players: " + entry[7] +"\nPrice:        " + entry[8] + "\nBeaten?:      " + entry[9] + "\nPurchase Date:" + entry[10] + "\nNotes:        " + entry[11]
        self.scr_delete.insert(0.0, to_print)     
        
    def confirm(self):      
        for keys in range(1, len(games)+1):
            if keys >= self.delete_key and keys != len(games):
                games[keys] = games[keys+1]
            if keys == len(games):
                games.pop(keys)  
                
        messagebox.showinfo(message="Entry has been deleted.")
        Screen.current=0
        Screen.switch_frame()
        
    def cancel(self):
        Screen.current=0
        Screen.switch_frame()  
        
class ErrorMessage(tk.Frame):
    
    def __init__(self,parent,msg="Generic"):
        tk.Frame.__init__(self,master=parent)
        self.parent = parent
        self.lbl_continue = tk.Label(self,text=msg)
        self.lbl_continue.grid(row=0,column=0)
        self.btn_ok=tk.Button(self,text="OK",command=self.parent.destroy)
        self.btn_ok.grid(row=0,column=1)
                  
#===[ Global Function(s) ]===

#===[ Main ]===
if __name__ == "__main__":
    datafile = open("game_library.pickle","rb")
    games = pickle.load(datafile)
    datafile.close()
    
    root = tk.Tk()
    root.title("Media Library")
    root.geometry("500x500")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    screens = [MainMenu(), SearchMenu(), AddEdit(), ConfirmRemove()]   #FileSaved(2), ChooseEdit(3), ChooseRemove(5),
    screens[0].grid(row=0,column=0,sticky="news")
    screens[1].grid(row=0,column=0,sticky="news")
    #screens[2].grid(row=0,column=0,sticky="news")
    #screens[3].grid(row=0,column=0,sticky="news")
    screens[2].grid(row=0,column=0,sticky="news")     #was 4
    #screens[5].grid(row=0,column=0,sticky="news")
    screens[3].grid(row=0,column=0,sticky="news")     #was 6
    
    
    screens[0].tkraise()
    root.mainloop()