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
            pwd.text = ''
            app.text = ''
            self.dbManager.execute("INSERT INTO pwd VALUES (NULL, ?, ?)",(pwd.text, app.text))
            self.dbManager.commit()
            grid.add_widget(Label(
                    font_size = 15,
                    text = "{}, no app {}".format(pwd.text, app.text),size_hint_y = None, height = 30
                ))
            grid.height += 20
            grid.rows += 1
        else:
            pass

    def back(self, scManager):
        scManager.current = 'access_Screen'

    def populate(self, grid,scManager):
        self.cur.execute("SELECT pwd, app FROM pwd")
        listaAux = self.cur.fetchall()
        for i in range(len(listaAux)):            
            grid.add_widget(Label(
                font_size = 15,
                text = "{}, no app {}".format(listaAux[i][0], listaAux[i][1]),size_hint_y = None, height = 30
            ))
            grid.height = i*20
        
        return len(listaAux)      

    def search(self, searchTxt, grid, scManager):
        if searchTxt.text != "":
            print(grid.rows)
            self.cur.execute("SELECT pwd, app FROM pwd WHERE app like (?)", ("%" + searchTxt.text + "%",))
            listaAux = self.cur.fetchall() 
            grid.clear_widgets()
            for i in range(len(listaAux)):            
                grid.add_widget(Label(
                    font_size = 15,
                    text = "{}, no app {}".format(listaAux[i][0], listaAux[i][1]),size_hint_y = None, height = 30
                ))
                grid.height = i*20
        else:
            print(grid.rows)
            if grid.rows <= 0:
                self.populate(grid, scManager)
            else:
                pass
    


if __name__ == "__main__":
    PwdManager().run()