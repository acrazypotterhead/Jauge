# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from components import Gauge, Segment  # Importation de la classe Gauge depuis gauge.py
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'multisamples', '2')  # Vous pouvez essayer avec 2, 4, 8, etc.

Builder.load_file('gauge.kv')

class GaugeApp(App):
    increasing = NumericProperty(1)
    begin = NumericProperty(0)
    step = NumericProperty(1)

    def build(self):
        box = BoxLayout(orientation='horizontal', padding=5)



        self.gauge = Gauge(value=0, size_gauge=600, size_text=25)   #initialisation de la jauge
        self.slider = Slider(orientation='horizontal', min=0.0 , max=100.0, step=0.1)  #initialisation du slider de données

        self.slider.size_hint = None, None
        self.slider.size = 200, 50
        self.slider.pos_hint = {'center_x': 0.5, 'center_y':0.5}



        box.add_widget(self.gauge)  # ajout de la jauge dans la box
        box.add_widget(self.slider)
        self.slider.bind(value = self.update_gauge)
        return box

    def update_gauge(self, instance, value):
        formatted_value = f"{value:.2f}"  # Formate la valeur pour afficher exactement deux chiffres après la virgule
        self.gauge.value = float(formatted_value)
        
        self.gauge.create_segments(value)

    #def gauge_increment(self):
    #    begin = self.begin    #
    #    begin += self.step * self.increasing
    #    if begin > 0 and begin < 100:
    #        self.gauge.value = self.slider.value = begin
    #    else:
    #        self.increasing *= -1
    #    self.begin = begin

class SegmentApp(App):

    def build(self):
        from kivy.clock import Clock
        from kivy.uix.gridlayout import GridLayout
        import random

        def refresh_task(self, *args):
            seg.value = random.choice('123456789')
  

        box = GridLayout(cols=8, padding=20)
        seg = Segment(scale=0.1, value="9")

        
        box.add_widget(seg)


        Clock.schedule_interval(refresh_task, 1)

        return box

if __name__ == '__main__':
    GaugeApp().run()