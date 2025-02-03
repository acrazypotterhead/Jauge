from kivy.uix.accordion import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty, BoundedNumericProperty
from kivy.graphics import Color, Mesh, Scale
from kivy.utils import get_color_from_hex
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock


class Jauge(RelativeLayout):
    #Borne de la jauge
    min_slidder = NumericProperty(0)
    max_slidder = NumericProperty(10)

    variable = NumericProperty()
    unit = BoundedNumericProperty(3, min=1.8, max=3.6, errorvalue=1.8) 
    _angle          = NumericProperty(-180)  
    marker_startangle = NumericProperty()
    needle_start_angle = NumericProperty(90)
    size_center = NumericProperty(217)
    value = NumericProperty()
    path = __file__

    # Importation images
    file_gauge = StringProperty("images/cadran 1.png")
    file_needle = StringProperty("images/aiguille 1.png")
    file_marker = StringProperty("images/marker.png")
    file_background_color = StringProperty("images/couleur1.jpg")
    file_value_marker = StringProperty("images/trait_rouge.png")

    size_gauge = NumericProperty()
    marker_color = ListProperty([1, 1, 1, 1])
    max_value_encountered = NumericProperty()
    show_marker = BooleanProperty(True)
    segment_color = StringProperty('2fc827')
    number_digits = NumericProperty()
    segment_scale = NumericProperty(0.3)
    
    def __init__(self, **kwargs):
        super(Jauge, self).__init__(**kwargs)
        
        self.bind(value=self._turn)
        self.marker_startangle = kwargs.get('marker_startangle', -self.unit * 100 / 2)  
        self.needle_start_angle = kwargs.get('needle_start_angle', self.unit * 100 / 2)
        #self.min_slidder = kwargs.get('min_slidder',-10)
        
   
    def _turn(self, *args):
        

        self.ids.needle.rotation = (50 * self.unit) - ((self.value - self.min_slidder)*(100/(self.max_slidder-self.min_slidder)) * self.unit) #50 fait que l'aiguille n'aille pas dans les negatifs 
        self._angle = ((self.value - self.min_slidder)*(100/(self.max_slidder-self.min_slidder)) * self.unit)-50 * self.unit
        
        

        if self.value > self.max_value_encountered:
            self.max_value_encountered = self.value
            

        # Mettre à jour la rotation du value_marker
        self.ids.value_marker.rotation = (50 * self.unit) - ((self.max_value_encountered - self.min_slidder) * (100 / (self.max_slidder - self.min_slidder)) * self.unit)
        
    

    def round_value(self, value):
        print(f"round_value appelé avec {value}")
        self.value = value #round(value, 2)  # Limiter la valeur à deux chiffres après la virgule
        #self.create_segments(self.value)

    def reset_max_value(self):
        print("reset_max_value appelé")
        self.max_value_encountered = 0
        self.ids.value_marker.rotation = self.needle_start_angle

    
        

    def contains_value(self, string, value):
        return value in string

    def split_number_integer(self, number):
        return [int(digit) for digit in str(number)]
    
    def split_number_decimal(self, number):
        number_str = str(number)
        is_negative = number_str.startswith('-')
        
        if is_negative:
            number_str = number_str[1:]  # Supprimer le signe négatif pour le traitement

        integer_part, decimal_part = number_str.split('.')
        integer_digits = [int(digit) for digit in integer_part]
        decimal_digits = [int(digit) for digit in decimal_part]

        if is_negative:
            integer_digits.insert(0, '-')  # Ajouter le signe négatif à la partie entière

        return integer_digits, decimal_digits
    
    def create_segments(self, number):
        self.ids.segments_box.clear_widgets()
        number_str = str(number)

        if number_str.startswith('-'):
            segment = Segment(scale=self.segment_scale, value='-', color=self.segment_color)
            self.ids.segments_box.add_widget(segment)
            number_str = number_str[1:]  # Remove the negative sign for further processing
            
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
        
        seg_moins = [
                30, 115, 0, 0,
                40, 120, 0, 0,
                85, 120, 0, 0,
                95, 115, 0, 0,
                85, 110, 0, 0,
                40, 110, 0, 0,
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
        type_moins = [seg_moins]
       
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
                "-" : type_moins,
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