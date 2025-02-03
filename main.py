# main.py

from kivy.app import App
from widgets import Jauge #, Vu_mètre, Gauge_barre , Valeur_bouton, Main 
from kivy.lang import Builder
from kivy.core.window import Window

# chargement des fichiers kv qui contiennent les widgets
Builder.load_file('jauge.kv')

# changement de la couleur de fond de l'application
Window.clearcolor = (255/255, 233/255, 204/255)

# appel de l'interface principale
class MyApp(App):
    def build(self):
        return Builder.load_file('interface.kv')
    
if __name__ == '__main__':
    MyApp().run()