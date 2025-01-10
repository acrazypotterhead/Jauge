from kivy.uix.effectwidget import Rectangle
# gauge.py
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BoundedNumericProperty, ListProperty, BooleanProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Ellipse, Mesh, Scale
from kivy.utils import get_color_from_hex

class Gauge(Widget):

    _start_angle = NumericProperty()
    _end_angle = NumericProperty()
    _min_data = NumericProperty()
    _max_data = NumericProperty()
    
    _angle          = NumericProperty(-90)            # Internal angle calculated from value.


    unit = NumericProperty(1.8)  # 1.8 fait que l'aiguille fasse un arc de cercle de 180°
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
    path = __file__

    file_gauge = StringProperty("images/cercle_blanc.png")
    file_needle = StringProperty("images/aiguille violette.png")
    file_square = StringProperty("images/carré.png")
    file_marker = StringProperty("images/marker.png")
    file_couleur1 = StringProperty("images/couleur1.jpg")

    size_gauge = NumericProperty()
    size_text = NumericProperty()
    
    marker_color = ListProperty([1, 1, 1, 1])
    marker_size = NumericProperty(0.10)
    marker_angle = NumericProperty(90)
    needle_angle = NumericProperty(0)
    marker_startangle = NumericProperty(-90)
    #marker_ahead = NumericProperty(0)
    show_marker = BooleanProperty(True)
    
    radius = NumericProperty()
    width = NumericProperty()   
    number_digits = NumericProperty()
    global_scale = NumericProperty(0.3)
    
    
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
        self._angle = (self.value * self.unit)-50 * self.unit
        
        #self.ids.segment1.value = str(int(self.value))
        #self.ids.segment2.value = str(int(self.value))
        #self.ids.segment3.value = str(int(self.value))

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
                segment = Segment(scale=self.global_scale, value=str(digit), color='2fc827')
                self.ids.segments_box.add_widget(segment)
            segment = Segment(scale=self.global_scale, value='.', color='2fc827')
            self.ids.segments_box.add_widget(segment)

            for digit in decimal_digits:
                segment = Segment(scale=self.global_scale, value=str(digit), color='2fc827')
                self.ids.segments_box.add_widget(segment)

        else:

            digits = self.split_number_integer(number)
            self.ids.segments_box.clear_widgets()

            for digit in digits:
                segment = Segment(scale=self.global_scale, value=str(digit), color='2fc827')
                self.ids.segments_box.add_widget(segment)

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
                20, 215, 0, 0,
                35, 230, 0, 0,
                95, 230, 0, 0,
                110, 215, 0, 0,
                95, 200, 0, 0,
                35, 200, 0, 0,
                ]
        seg_2 = [
                15, 210, 0, 0,
                30, 195, 0, 0,
                30, 135, 0, 0,
                15, 120, 0, 0,
                0, 135, 0, 0,
                0, 195, 0, 0,
                ]
        seg_3 = [
                115, 210, 0, 0,
                130, 195, 0, 0,
                130, 135, 0, 0,
                115, 120, 0, 0,
                100, 135, 0, 0,
                100, 195, 0, 0,
                ]
        seg_4 = [
                20, 115, 0, 0,
                35, 130, 0, 0,
                95, 130, 0, 0,
                110, 115, 0, 0,
                95, 100, 0, 0,
                35, 100, 0, 0,
                ]
        seg_5 = [
                15, 110, 0, 0,
                30, 95, 0, 0,
                30, 35, 0, 0,
                15, 20, 0, 0,
                0, 35, 0, 0,
                0, 95, 0, 0,
                ]
        seg_6 = [
                115, 110, 0, 0,
                130, 95, 0, 0,
                130, 35, 0, 0,
                115, 20, 0, 0,
                100, 35, 0, 0,
                100, 95, 0, 0,
                ]
        seg_7 = [
                20, 15, 0, 0,
                35, 30, 0, 0,
                95, 30, 0, 0,
                110, 15, 0, 0,
                95, 0, 0, 0,
                35, 0, 0, 0,
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
                if key == ".":
                    self.indice = range(0, 8)
                    for segment in val:
                        Mesh(
                            vertices=segment, 
                            indices=self.indice, 
                            mode=self.xmode
                            )
                else:
                    for segment in val:
                        
                        Mesh(
                            vertices=segment, 
                            indices=self.indice, 
                            mode=self.xmode
                            )
             

    # Avoid if session
    