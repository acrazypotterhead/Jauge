# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from components import Gauge, Segment, Gauge_barre , Valeur_bouton, Main # Importation de la classe Gauge depuis gauge.py
from kivy.properties import NumericProperty
from kivy.lang import Builder




class GaugeApp(App):
    increasing = NumericProperty(1)
    begin = NumericProperty(0)
    step = NumericProperty(1)


    def build(self):
        box = BoxLayout(orientation='horizontal', padding=5)

        self.gauge = Gauge(value=0, size_gauge=800)   #initialisation de la jauge
        self.gauge.pos = 100, 100
        #self.slider1 = Slider(orientation='horizontal', min=self.gauge.min_slidder , max= self.gauge.max_slidder, step=0.01)  #initialisation du slider de données
#
        #self.slider1.size_hint = None, None
        #self.slider1.size = 200, 50
        #self.slider1.pos_hint = {'center_x': 0.5, 'center_y':0.5}
#
        #
        #self.slider1.bind(value = self.update_gauge)
        
        #self.gauge_barre=Gauge_barre()

        #self.slider2 = Slider(orientation='horizontal', min=self.gauge_barre.min_slidder , max= self.gauge_barre.max_slidder, step=1)
        #self.slider2.size_hint = None, None
        #self.slider2.size = 200, 50
        #self.slider2.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        
        
        box.add_widget(self.gauge) 
        #box.add_widget(self.slider1) 

        #box.add_widget(self.slider2)
        #box.add_widget(self.gauge_barre)

        #self.slider2.bind(value = self.update_gauge_barre)

  




        return box

    def update_gauge_barre(self, instance, value):
        self.gauge_barre.value = value

    def update_gauge(self, instance, value):
        formatted_value = f"{value:.2f}"  # Formate la valeur pour afficher exactement deux chiffres après la virgule
        self.gauge.value = float(formatted_value)
        
        #self.gauge.create_segments(formatted_value)

#class SegmentApp(App):
#
#    def build(self):
#        from kivy.clock import Clock
#        from kivy.uix.gridlayout import GridLayout
#        import random
#
#        def refresh_task(self, *args):
#            seg.value = random.choice('123456789')
#  
#
#        box = GridLayout(cols=8, padding=20)
#        seg = Segment(scale=0.1, value="9")
#
#        
#        box.add_widget(seg)
#
#
#        Clock.schedule_interval(refresh_task, 1)
#
#        return box

if __name__ == '__main__':
    GaugeApp().run()