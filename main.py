from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
import sqlite3

Builder.load_file('App_.kv')

class App_(ScreenManager):
    pass

class PwdManager(App):
    dbManager = sqlite3.connect('pmStorage.db')
    def build(self):        
        self.dbManager.execute(
            "CREATE TABLE IF NOT EXISTS pwd(id integer PRIMARY KEY AUTOINCREMENT, pwd text, app text)"
            )

        self.cur = self.dbManager.cursor()


        return App_()        
    
    def connect(self,pwd, app, grid,scManager):
        if pwd.text != "" and app.text != "":            
            self.dbManager.execute("INSERT INTO pwd VALUES (NULL, ?, ?)",(pwd.text, app.text))
            self.dbManager.commit()
            lbl = Label(
                    font_size = 15,
                    text = "{}, no app {}".format(pwd.text, app.text),size_hint_y = None, height = 30
                )
            grid.add_widget(lbl)
            grid.height += 20
            grid.rows += 1        
            grid.ids[str(grid.rows-1)] = lbl
            self.button_maker(grid, scManager)         
            pwd.text = ''
            app.text = ''
        else:
            pass

    def back(self, scManager):
        scManager.current = 'access_Screen'

    def populate(self, grid,scManager):
        self.cur.execute("SELECT pwd, app FROM pwd")
        listaAux = self.cur.fetchall()  
        for i in range(len(listaAux)):     
            lbl = Label(
                font_size = 15,
                text = "{}, no app {}".format(listaAux[i][0], listaAux[i][1]),size_hint_y = None, height = 30
            )      
            grid.add_widget(lbl)
            grid.ids[str(i)] = lbl
            self.button_maker(grid,scManager,n=i)
            grid.height = i*20
        return len(listaAux)      

    def search(self, searchTxt, grid, scManager):
        if searchTxt.text != "":
            self.cur.execute("SELECT pwd, app FROM pwd WHERE app like (?)", ("%" + searchTxt.text + "%",))
            listaAux = self.cur.fetchall() 
            grid.clear_widgets()
            for i in range(len(listaAux)):     
                lbl = Label(
                    font_size = 15,
                    text = "{}, no app {}".format(listaAux[i][0], listaAux[i][1]),size_hint_y = None, height = 30
                )    
                grid.add_widget(lbl)
                grid.ids[str(i)] = lbl
                self.button_maker(grid, scManager)    
                grid.height = i*20
    
        else:
            print(grid.rows)
            if grid.rows <= 0:
                self.populate(grid, scManager)
            else:
                pass

    def decrypt(self,login,scManager):
        #temporary, just to get the login idea somewhat done
        if login.text == "y":
            scManager.current = "main_Screen"
        else:
            scManager.current = "error_Screen"

    def button_maker(self, grid, scManager, **kwargs):
        if len(kwargs) == 0:
            btn = Button(size_hint_x = None, width = 10,size_hint_y=None, height = 10, text = str((grid.rows-1)))            
            grid.add_widget(btn) 
            btn.bind(on_release=lambda x:self.editScreen(grid, btn, scManager))
        else:
            for key, values in kwargs.items():
                btn = Button(size_hint_x = None, width = 10,size_hint_y=None, height = 10, text = str(values))                
                grid.add_widget(btn)
                btn.bind(on_release=lambda x:self.editScreen(grid, btn, scManager))

    def editScreen(self, grid, btn, scManager):
        scManager.current = 'edit_Screen'
        #grid.ids[btn.text] acessa diretamente a label, portanto posso usar pra deletar no BD
        #por algum motivo, depois de criar o botão, o id dele é +1 do do que deveria ser (???)
        print((grid.ids[btn.text]).text)
        self.lblToEdit = (grid.ids[btn.text])
        self.btnToEdit = btn
    
    def edit(self,pwd,app, scManager):    
        if pwd.text != "" and app.text != "":    
            lblTextAux = self.lblToEdit.text.split(", no app ")        
            self.dbManager.execute("UPDATE pwd SET pwd = ?, app = ? WHERE pwd = ? and app = ?", (pwd.text, app.text, lblTextAux[0], lblTextAux[1]))
            self.dbManager.commit()
            self.lblToEdit.text = "{}, no app {}".format(pwd.text, app.text)
            self.lblToEdit = None
            scManager.current = 'main_Screen'
        else:
            scManager.current = 'main_Screen'

    def delete(self,grid, scManager):
        lblTextAux = self.lblToEdit.text.split(", no app ")    
        print(lblTextAux[0])
        print(lblTextAux[1])   
        grid.remove_widget(self.lblToEdit)
        grid.remove_widget(self.btnToEdit)        
        self.dbManager.execute("DELETE FROM pwd WHERE pwd = ? AND app = ?", (lblTextAux[0], lblTextAux[1]))
        self.dbManager.commit()
        self.btnToEdit = None
        self.lblToEdit = None
        scManager.current = 'main_Screen'

    


if __name__ == "__main__":
    PwdManager().run()