#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
kivy.require('1.6.0')

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BoundedNumericProperty, ListProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

class Gauge(Widget):
    unit = NumericProperty(1.8)  # 1.8 fait que l'aiguille fasse un arc de cercle de 180°
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    path = __file__
    file_gauge = StringProperty("images/cadran.png")
    file_needle = StringProperty("images/needle.png")
    file_square = StringProperty("images/carré.png")
    file_marker = StringProperty("images/marker.png")
    size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
    size_text = NumericProperty(10)
    marker_color = ListProperty([1, 1, 1, 1])
    marker_size = NumericProperty(0.10)
    marker_angle = NumericProperty(90)
    needle_angle = NumericProperty(0)
    marker_startangle = NumericProperty(-90)
    marker_ahead = NumericProperty(0)
    show_marker = BooleanProperty(True)
    _radius = NumericProperty(2)   

    
    _angle          = NumericProperty(-90)            # Internal angle calculated from value.
    _angle_step     = NumericProperty(0)            # Internal angle_step calculated from step.
    
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self.bind(value=self._turn)
        self.bind(show_marker=self._show_marker)

    def _show_marker(self, *args, flag):
        if flag:
            self.marker_color[3] = 1
        else:
            self.marker_color[3] = 0

    def _turn(self, *args):
        self.ids.needle.rotation = (50 * self.unit) - (self.value * self.unit) #50 fait que l'aiguille n'aille pas dans les negatifs 
        self.ids.label.text = f"[b]{self.value:.0f}[/b]"
        self.ids.progress.value = self.value
        self._angle = (self.value * self.unit)-90


class GaugeApp(App):
    increasing = NumericProperty(1)
    begin = NumericProperty(0)
    step = NumericProperty(1)

    def build(self):
        box = BoxLayout(orientation='horizontal', padding=5)
        self.gauge = Gauge(value=0, size_gauge=256, size_text=25)   #initialisation de la jauge
        self.slider = Slider(orientation='vertical', min=0, max=100)  #initialisation du slider de données

        stepper = Slider(min=1, max=25)  #initialisation du slider de pas de rotation
        stepper.bind(
            value=lambda instance, value: setattr(self, 'step', value) #valeur du pas de la rotation 
        )

        box.add_widget(self.gauge)  # ajout de la jauge dans la box
        box.add_widget(stepper)  # ajout du slider de pas de rotation dans la box
        box.add_widget(self.slider)
        #Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.30)
        self.slider.bind(value = self.update_gauge)
        return box

    def update_gauge(self, instance, value):
        self.gauge.value = value

    def gauge_increment(self):
        begin = self.begin    #
        begin += self.step * self.increasing
        if begin > 0 and begin < 100:
            self.gauge.value = self.slider.value = begin
        else:
            self.increasing *= -1
        self.begin = begin


if __name__ == '__main__':
    GaugeApp().run()
