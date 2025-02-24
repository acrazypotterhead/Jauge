from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# Define what we want to graph
x = [1, 2, 3, 4, 5]
y1 = [5, 12, 6, 9, 15]
y2 = [2, 3, 4, 5, 6]
y3 = [7, 8, 9, 10, 11]

# Create a figure and three subplots

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 10))

ax1.plot(x, y1)
ax1.set_ylabel("Y1 Axis")
ax1.set_xlabel("X Axis")

ax2.plot(x, y2)
ax2.set_ylabel("Y2 Axis")
ax2.set_xlabel("X Axis")

ax3.plot(x, y3)
ax3.set_ylabel("Y3 Axis")
ax3.set_xlabel("X Axis")

class Matty(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(fig))



class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file('test.kv')
        return Matty()

if __name__ == '__main__':
    MainApp().run()