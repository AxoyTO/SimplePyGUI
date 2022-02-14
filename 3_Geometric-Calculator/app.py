from xml.etree.ElementTree import QName
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QWidget, QMainWindow, QComboBox, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox)
from figures import *
from drawer import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Geometric Calculator")
        self.setFixedSize(QSize(600, 500))

        self.shape = 'Square'
        self.shapes = ['Square', 'Rectangle', 'Cube', 'Parallelepiped',
                       'Circle', 'Sphere', 'Triangle', 'Pyramid', 'Trapezoid', 'Rhombus', 'Cylinder', 'Cone']
        self.calc_call_count = 0
        self.object_changed = False

        self.combobox = QComboBox()
        self.combobox.addItems(self.shapes)
        self.plotbutton = QPushButton('Plot')
        self.calc_button = QPushButton('Calculate')
        self.side_a_input = QLineEdit()

        self.init_layout()
        self.combobox.currentTextChanged.connect(self.chosen_shape)
        self.calc_button.clicked.connect(self.calculate)
        self.plotbutton.clicked.connect(self.plot)

        self.set_widget()

    def set_widget(self):
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def init_layout(self):
        self.sc = DrawFigures(width=5, height=4, dpi=100)
        # toolbar = NavigationToolbar(self.sc, self)

        self.main_layout = QHBoxLayout()
        self.text_layout = QFormLayout()
        self.options_layout = QVBoxLayout()
        self.top_layout = QFormLayout()

        # self.top_layout.addWidget(toolbar)
        # Необъязательно + ошибочно при работе с трехмерными моделями

        self.top_layout.addRow("Author :", QLabel("github.com/AxoyTO"))
        self.top_layout.addRow("", QLabel("Made for YLAB with ♥"))
        self.top_layout.addWidget(self.sc)
        self.top_layout.setVerticalSpacing(20)

        self.text_layout.addRow("Select shape:", self.combobox)
        self.text_layout.addRow("Enter side_a:", self.side_a_input)

        self.options_layout.addSpacing(150)
        self.options_layout.addLayout(self.text_layout)
        self.options_layout.addWidget(self.calc_button)
        self.options_layout.addWidget(self.plotbutton)
        self.options_layout.addSpacing(300)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.options_layout)
        self.main_layout.addSpacing(20)

    def change_layout(self):
        self.object_changed = True
        self.calc_call_count = 0

        for i in reversed(range(1, self.text_layout.rowCount())):
            self.text_layout.removeRow(i)

        if self.shape in ['Square', 'Rectangle', 'Cube', 'Triangle', 'Pyramid', 'Trapezoid', 'Parallelepiped']:
            self.side_a_input = QLineEdit()
            self.text_layout.addRow("Enter side a:", self.side_a_input)
            if self.shape in ['Triangle', 'Pyramid']:
                self.height_input = QLineEdit()
                self.text_layout.addRow("Enter height:", self.height_input)
            elif self.shape in ['Rectangle', 'Rhombus', 'Trapezoid', 'Parallelepiped']:
                self.side_b_input = QLineEdit()
                self.text_layout.addRow("Enter side b:", self.side_b_input)
                if self.shape == 'Trapezoid':
                    self.height_input = QLineEdit()
                    self.text_layout.addRow("Enter height:", self.height_input)
                elif self.shape == 'Parallelepiped':
                    self.side_c_input = QLineEdit()
                    self.text_layout.addRow("Enter side c:", self.side_c_input)
        elif self.shape == 'Rhombus':
            self.side_a_input = QLineEdit()
            self.side_b_input = QLineEdit()
            self.text_layout.addRow("Enter diagonal p:", self.side_a_input)
            self.text_layout.addRow("Enter diagonal q:", self.side_b_input)
        elif self.shape in ['Circle', 'Sphere', 'Cylinder', 'Cone']:
            self.radius_input = QLineEdit()
            self.text_layout.addRow("Pi:", QLabel(str(f"{math.pi:6f}")))
            self.text_layout.addRow("Enter radius:", self.radius_input)
            if self.shape not in ['Circle', 'Sphere']:
                self.height_input = QLineEdit()
                self.text_layout.addRow("Enter height:", self.height_input)

    def handle_inputs(self):
        ret_val = 0
        if self.shape in ['Cylinder', 'Cone', 'Triangle', 'Pyramid', 'Trapezoid']:
            if not(self.handle_height_input()):
                ret_val = -1
        if self.shape in ['Square', 'Rectangle', 'Cube', 'Triangle', 'Pyramid', 'Rhombus', 'Trapezoid', 'Parallelepiped']:
            if not(self.handle_side_input()):
                ret_val = -1
        if self.shape in ['Circle', 'Sphere', 'Cylinder', 'Cone']:
            if not(self.handle_radius_input()):
                ret_val = -1

        if ret_val == -1:
            return False

        return True

    def handle_side_input(self):
        side_a = self.side_a_input.text()
        if self.shape in ['Cube', 'Square', 'Triangle', 'Pyramid']:
            if self.check_side(side_a):
                return True
        else:
            side_b = self.side_b_input.text()
            if self.shape in ['Rectangle', 'Rhombus', 'Trapezoid']:
                if self.check_side(side_a, side_b):
                    return True
            else:
                side_c = self.side_c_input.text()
                if self.shape == 'Parallelepiped':
                    if self.check_side(side_a, side_b, side_c):
                        return True

    def check_side(self, side_a, side_b=0, side_c=0):
        try:
            side_a, side_b, side_c = int(side_a), int(side_b), int(side_c)
            if side_a < 0 or side_b < 0 or side_c < 0:
                QMessageBox.about(self, 'Wrong Input',
                                  'Side can only be greater than 0!')
                return False
        except Exception:
            QMessageBox.about(self, 'Wrong Input',
                              'Side can only be a number!')
            return False
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        return True

    def handle_radius_input(self):
        radius = self.radius_input.text()
        try:
            radius = int(radius)
            if radius < 0:
                QMessageBox.about(self, 'Wrong Input',
                                  'Radius can only be greater than 0!')
                return False
        except Exception:
            QMessageBox.about(self, 'Wrong Input',
                              'Radius can only be a number!')
            return False
        self.radius = radius
        return True

    def handle_height_input(self):
        height = self.height_input.text()
        try:
            height = int(height)
            if height < 0:
                QMessageBox.about(self, 'Wrong Input',
                                  'Height can only be greater than 0!')
                return False
        except Exception:
            QMessageBox.about(self, 'Wrong Input',
                              'Height can only be a number!')
            return False
        self.height = height
        return True

    def plot(self):
        if not(self.handle_inputs()):
            return

        if self.shape == 'Square':
            shape = Square()
            shape.create(self.side_a)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawRectangle('Square', self.side_a, self.side_a)

        elif self.shape == 'Cube':
            shape = Cube()
            shape.create(self.side_a)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawCube(self.side_a)

        elif self.shape == 'Triangle':
            shape = Triangle()
            shape.create(self.side_a, self.height)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawTriangle(self.side_a, self.height)

        elif self.shape == 'Pyramid':
            shape = Pyramid()
            shape.create(self.side_a, self.height)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawPyramid(self.side_a, self.height)

        elif self.shape == 'Rectangle':
            shape = Rectangle()
            shape.create(self.side_a, self.side_b)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawRectangle('Rectangle', self.side_a, self.side_b)

        elif self.shape == 'Rhombus':
            shape = Rhombus()
            shape.create(self.side_a, self.side_b)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawRhombus(self.side_a, self.side_b)

        elif self.shape == 'Trapezoid':
            shape = Trapezoid()
            shape.create(self.side_a, self.side_b, self.height)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawTrapezoid(self.side_a, self.side_b, self.height)

        elif self.shape == 'Parallelepiped':
            shape = Parallelepiped()
            shape.create(self.side_a, self.side_b, self.side_c)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawParallelepiped(self.side_a, self.side_b, self.side_c)

        elif self.shape == 'Circle':
            shape = Circle()
            shape.create(self.radius)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawCircle(self.radius, shape.perimeter())

        elif self.shape == 'Sphere':
            shape = Sphere()
            shape.create(self.radius)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawSphere(self.radius)

        elif self.shape == 'Cylinder':
            shape = Cylinder()
            shape.create(self.radius, self.height)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawCylinder(self.radius, self.height)

        elif self.shape == 'Cone':
            shape = Cone()
            shape.create(self.radius, self.height)
            self.top_layout.removeRow(self.top_layout.rowCount()-1)
            self.sc = DrawCone(self.radius, self.height)

        self.top_layout.addWidget(self.sc)

    def calculate(self):
        if not(self.handle_inputs()):
            if self.calc_call_count >= 1:
                self.text_layout.removeRow(self.text_layout.rowCount()-1)
                self.text_layout.removeRow(self.text_layout.rowCount()-1)
                self.calc_call_count = 0
            return

        if self.calc_call_count >= 1:
            self.text_layout.removeRow(self.text_layout.rowCount()-1)
            self.text_layout.removeRow(self.text_layout.rowCount()-1)

        if self.shape == 'Square':
            shape = Square()
            shape.create(self.side_a)
        elif self.shape == 'Cube':
            shape = Cube()
            shape.create(self.side_a)
        elif self.shape == 'Triangle':
            shape = Triangle()
            shape.create(self.side_a, self.height)
        elif self.shape == 'Pyramid':
            shape = Pyramid()
            shape.create(self.side_a, self.height)
        elif self.shape == 'Rectangle':
            shape = Rectangle()
            shape.create(self.side_a, self.side_b)
        elif self.shape == 'Rhombus':
            shape = Rhombus()
            shape.create(self.side_a, self.side_b)
        elif self.shape == 'Trapezoid':
            shape = Trapezoid()
            shape.create(self.side_a, self.side_b, self.height)
        elif self.shape == 'Parallelepiped':
            shape = Parallelepiped()
            shape.create(self.side_a, self.side_b, self.side_c)
        elif self.shape == 'Circle':
            shape = Circle()
            shape.create(self.radius)
        elif self.shape == 'Sphere':
            shape = Sphere()
            shape.create(self.radius)
        elif self.shape == 'Cylinder':
            shape = Cylinder()
            shape.create(self.radius, self.height)
        elif self.shape == 'Cone':
            shape = Cone()
            shape.create(self.radius, self.height)

        if self.shape not in ['Sphere', 'Pyramid', 'Cylinder', 'Cone', 'Cube']:
            self.text_layout.addRow(
                "Area:", QLabel(str(f"{shape.area()}")))
            self.text_layout.addRow(
                "Perimeter:", QLabel(str(f"{shape.perimeter()}")))
        else:
            self.text_layout.addRow(
                "Volume:", QLabel(str(f"{shape.volume()}")))
            self.text_layout.addRow(
                "Surface Area:", QLabel(str(f"{shape.surface_area()}")))

        self.calc_call_count += 1

    def chosen_shape(self):
        self.shape = self.combobox.currentText()
        self.change_layout()
