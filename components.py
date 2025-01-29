from kivy.uix.effectwidget import Rectangle
# gauge.py
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BoundedNumericProperty, ListProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Ellipse, Mesh, Scale
from kivy.utils import get_color_from_hex
import math
from kivy.uix.boxlayout import BoxLayout
from plyer import accelerometer
from kivy.clock import Clock

class Gauge(Widget):

    #Valeur max de la jauge
    min_slidder = NumericProperty(200)
    max_slidder = NumericProperty(500)
    variable = NumericProperty()
    unit = NumericProperty(3) 

    
    _angle          = NumericProperty(-180)  

    marker_startangle = NumericProperty()
    needle_start_angle = NumericProperty()

 
    size_center = NumericProperty(194)
    
    value = BoundedNumericProperty(0, min=0, max=500, errorvalue=0)
    path = __file__

    # Importation images
    file_gauge = StringProperty("images/cadran3.jpg")
    file_needle = StringProperty("images/aiguille violette.png")
    file_marker = StringProperty("images/marker.png")
    file_background_color = StringProperty("images/couleur1.jpg")
    file_value_marker = StringProperty("images/trait_rouge.png")

    size_gauge = NumericProperty()
    size_text = NumericProperty()
    
    marker_color = ListProperty([1, 1, 1, 1])

    
    max_value_encountered = NumericProperty(0)
    show_marker = BooleanProperty(True)
    
    segment_color = StringProperty('2fc827')
    
    number_digits = NumericProperty()
    segment_scale = NumericProperty(0.3)
    
    

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self.bind(value=self._turn)
        self.marker_startangle = -self.unit * 100 / 2  
        self.needle_start_angle = self.unit * 100 / 2

        self.sensorEnabled = False

        

    def _turn(self, *args):
        self.ids.needle.rotation = (50 * self.unit) - ((self.value - self.min_slidder)*(100/(self.max_slidder-self.min_slidder)) * self.unit) #50 fait que l'aiguille n'aille pas dans les negatifs 
        self._angle = ((self.value - self.min_slidder)*(100/(self.max_slidder-self.min_slidder)) * self.unit)-50 * self.unit

        
        if self.value > self.max_value_encountered:
            self.max_value_encountered = self.value

        # Mettre à jour la rotation du value_marker
        self.ids.value_marker.rotation = (50 * self.unit) - ((self.max_value_encountered - self.min_slidder) * (100 / (self.max_slidder - self.min_slidder)) * self.unit)


    def reset_max_value(self):
        self.max_value_encountered = 0
        self.ids.value_marker.rotation = self.needle_start_angle

    def is_max(self, value):
        max = self.value
        if value > max:
            return True
        

    def contains_value(self, string, value):
        return value in string

    def split_number_integer(self, number):
        return [int(digit) for digit in str(number)]
    
    def split_number_decimal(self, number):
        integer_part, decimal_part = str(number).split('.')
        integer_digits = [int(digit) for digit in integer_part]
        decimal_digits = [int(digit) for digit in decimal_part]
        return integer_digits, decimal_digits

    def create_segments(self, number):
        if self.contains_value(str(number), '.'):
            integer_digits, decimal_digits = self.split_number_decimal(number)
            self.ids.segments_box.clear_widgets()

            for digit in integer_digits:
                segment = Segment(scale=self.segment_scale, value=str(digit), color=self.segment_color)
                self.ids.segments_box.add_widget(segment)
               
            segment = Segment(scale=self.segment_scale, value='.', color=self.segment_color)

            self.ids.segments_box.add_widget(segment)

            for digit in decimal_digits:
                segment = Segment(scale=self.segment_scale, value=str(digit), color=self.segment_color)
                self.ids.segments_box.add_widget(segment)
                
        else:

            digits = self.split_number_integer(number)
            self.ids.segments_box.clear_widgets()

            for digit in digits:
                segment = Segment(scale=self.segment_scale, value=str(digit), color='2fc827')
                self.ids.segments_box.add_widget(segment)



    def do_toggle(self):
        if not self.sensorEnabled:
            try:
                accelerometer.enable()
                print(accelerometer.acceleration)
                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            except:
                print("Accelerometer is not implemented for your platform")
    
            if self.sensorEnabled:
                Clock.schedule_interval(self.get_acceleration, 1 / 20)
            else:
                accelerometer.disable()
                status = "Accelerometer is not implemented for your platform"
                self.ids.toggle_button.text = status
        else:
            # Stop de la capture
            accelerometer.disable()
            Clock.unschedule(self.get_acceleration)
    
            # Retour à l'état arrété
            self.sensorEnabled = False
            self.ids.toggle_button.text = "Start Accelerometer"
    
    def get_acceleration(self, dt):
        if self.sensorEnabled:
            val = accelerometer.acceleration[:3]
    
            if not val == (None, None, None):
                self.ids.x_label.text = "X: " + str(val[0])
                self.ids.y_label.text = "Y: " + str(val[1])
                self.ids.z_label.text = "Z: " + str(val[2])
                self.value = val[0]


class Segment(RelativeLayout):
    '''
    Segment class

    The class`Segment` widget is a widget for displaying segment.

    The value property of segment must be a string.
    The scale property of segment must be a float.
    The color property of segment must be a string.

    Ex::

    seg = Segment(scale=0.3, value="A.")

    Are permitted : 0 1 2 3 4 5 6 7 8 9 and 0. 1. 2. 3. 4. 5. 6. 7. 8. 9.

    and

    A b C d E F and A. b. C. d. E. F.

    '''

    # Object properties configuration
    scale = BoundedNumericProperty(0.1, min=0.1, max=1, errorvalue=0.2)
    color = StringProperty('2fc827')
    value = StringProperty('A.')

    def __init__(self, **kwargs):     
        super(Segment, self).__init__(**kwargs)

        # Drawing meshes configuration, indices range meshes and mode
        self.indice = range(0, 6)
        self.xmode = 'triangle_fan'
        
        # Segment matrix configuration
        #
        #     _ 1 _
        #   |       |          
        #   2       3
        #   |       |
        #     _ 4 _
        #   |       |
        #   5       6
        #   |       |
        #     _ 7 _

        seg_1 = [
            8, 222, 0, 0,
            7, 224, 0, 0,
            10, 225, 0, 0,
            120, 225, 0, 0,
            123, 224, 0, 0,
            122, 222, 0, 0,
            100, 200,0 ,0,
            30, 200, 0, 0,
            
            ]
        seg_2 = [
            0, 220, 0, 0,
            1, 223, 0, 0,
            3, 222, 0, 0,
            30, 195, 0, 0,
            30, 132, 0, 0,
            3, 119, 0, 0,
            1, 117, 0, 0,
            0, 120, 0, 0,
            ]
        seg_3 = [
            100, 195, 0, 0,
            127, 222, 0, 0,
            129, 223, 0, 0,
            130, 222, 0, 0,
            130, 105, 0, 0,
            129, 102, 0, 0,
            127, 103, 0, 0,
            100, 130, 0, 0,
            ]
        seg_4 = [
            33, 130, 0, 0,
            97, 130, 0, 0,
            97, 100, 0, 0,
            33, 100, 0, 0,
            4, 115, 0, 0,
     
            ]
        seg_5 = [
            0, 110, 0, 0,         #7 coordonnées
            1, 113, 0, 0,
            3, 112, 0, 0,
            30, 97, 0, 0,
            30, 48, 0, 0,
            0, 48, 0, 0,

            ]
        seg_6 = [
            130, 95, 0, 0,
            130, 10, 0, 0,
            129, 9, 0, 0,
            128, 8, 0, 0,
            127, 7, 0, 0,
            100, 35, 0, 0,
            100, 120, 0, 0,
            101, 123, 0, 0,
   
            ]
        seg_7 = [
            
            10, 5, 0, 0,
            9, 6, 0, 0,
            7, 5, 0, 0,
            5, 6, 0, 0,
            4, 8, 0, 0,
            3, 9, 0, 0,
            2, 10, 0, 0,
            1, 12, 0, 0,
            0, 15, 0, 0,
            0, 45, 0, 0,        #10 coordonnées
            30, 45, 0, 0,
            30, 35, 0, 0,
            95, 35, 0, 0,
            125, 5, 0, 0,
            ]

        seg_point = [	
                9, 35, 0, 0,
                26, 35, 0, 0,
                35, 27, 0, 0,
                35, 13, 0, 0,
                26, 5, 0, 0,
                9, 5, 0, 0,
                0, 13, 0, 0,
                0, 27, 0, 0,
                ]        


        # Drawing association
        type_0 = [seg_1, seg_2, seg_3, seg_5, seg_6, seg_7]
        type_1 = [seg_3, seg_6]
        type_2 = [seg_1, seg_3, seg_4, seg_5, seg_7]
        type_3 = [seg_1, seg_3, seg_4, seg_6, seg_7]
        type_4 = [seg_2, seg_3, seg_4, seg_6]
        type_5 = [seg_1, seg_2, seg_4, seg_6, seg_7]
        type_6 = [seg_1, seg_2, seg_4, seg_5, seg_6, seg_7]
        type_7 = [seg_1, seg_3, seg_6]
        type_8 = [seg_1, seg_2, seg_3, seg_4, seg_5, seg_6, seg_7]
        type_9 = [seg_1, seg_2, seg_3, seg_4, seg_6, seg_7]
        type_point = [seg_point]
       
        # Routing association
        self.type_dic = {
                "0" : type_0,
                "1" : type_1,
                "2" : type_2,
                "3" : type_3,
                "4" : type_4,
                "5" : type_5,
                "6" : type_6,
                "7" : type_7,
                "8" : type_8,
                "9" : type_9,
                "." : type_point,
                }

        # Binding refresh drawing method
        self.bind(
            pos=self._update_canvas, 
            size=self._update_canvas,
            value=self._update_canvas,
            scale=self._update_canvas,
            )

    def _update_canvas(self, *args):

        with self.canvas:

            # Refresh
            self.canvas.clear()

            # Configure
            Color(
                get_color_from_hex(self.color)[0], 
                get_color_from_hex(self.color)[1], 
                get_color_from_hex(self.color)[2], 100)

            # Scale
            Scale(self.scale, self.scale, 1)


            self.make_mesh()
            # Draw meshes
    def make_mesh(self, *args):
        ''' Drawing meshes
        '''
        for key, val in self.type_dic.items():
            if self.value == key:
                for segment in val:
                    self.indice = range(0, len(segment)//4)
                    Mesh(
                        vertices=segment, 
                        indices=self.indice, 
                        mode=self.xmode
                        )
             
             
class Main(BoxLayout):
    pass

class Valeur_bouton(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Valeur_bouton instancié :", self)
    # Avoid if session

class Gauge_barre(Widget):
    value = NumericProperty()
    file_background_color = StringProperty("images/couleur1.jpg")
    file_needle = StringProperty("images/needle_fine.png")
    max_slidder = NumericProperty(700)
    min_slidder = NumericProperty(200)