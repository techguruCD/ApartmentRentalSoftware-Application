from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from widgets.elements import InputWrapper, CustomWindow

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

def get_dialog_icon(icon_type: str) -> QtWidgets.QLabel:
    pixmap = QtGui.QPixmap(f'data/{icon_type}.svg')
    pixmap.setDevicePixelRatio(2)
    label_icon = QtWidgets.QLabel(pixmap=pixmap)
    label_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    return label_icon

class UtilityBillsDialog(QtWidgets.QDialog):
    def __init__(self, electricity: float = 0, water: float = 0, tax: float = 0) -> None:
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.is_accepted = False

        self.setObjectName('Window')

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.electricity_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=electricity)
        self.electricity_field.setObjectName('Input')

        self.water_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=water)
        self.water_field.setObjectName('Input')

        self.tax_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=tax)
        self.tax_field.setObjectName('Input')

        button_accept = QtWidgets.QPushButton(tr('Buttons - Save', 'Save'))
        button_accept.setObjectName('DialogButton')
        button_accept.clicked.connect(self.accept)

        button_reject = QtWidgets.QPushButton(tr('Buttons - Cancel', 'Cancel'))
        button_reject.setObjectName('DialogButton')
        button_reject.clicked.connect(self.reject)

        layout.addWidget(InputWrapper(tr('UtilityDialog - Electricity', 'Electricity'), self.electricity_field), 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('UtilityDialog - Water', 'Water'), self.water_field), 1, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('UtilityDialog - Tax', 'Tax'), self.tax_field), 2, 0, 1, 2)
        layout.addWidget(button_accept, 3, 0)
        layout.addWidget(button_reject, 3, 1)

        self.wrapper = CustomWindow()
        self.wrapper.setWindowTitle(tr('UtilityDialog - Title', 'Enter utility payment details'))
        self.wrapper.connect_control_signals(self)
        self.wrapper.widget.setLayout(layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.wrapper)
        self.setLayout(main_layout)

        self.exec()

    def accept(self):
        self.is_accepted = True
        super().accept()
    
    def reject(self):
        return super().reject()

    def __call__(self):
        return {
            'electricity': self.electricity_field.value(),
            'water': self.water_field.value(),
            'tax': self.tax_field.value()
        }

class Dialog(QtWidgets.QDialog):
    def __init__(self, title: str, text: str, icon_type: str):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.is_accepted = False
        self.__init_UI(title, text, icon_type)

        self.exec()

    def __init_UI(self, title: str, text: str, icon_type: str):
        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        btn_ok = QtWidgets.QPushButton(tr('Buttons - Ok', 'Ok'))
        btn_ok.setObjectName('DialogButton')
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QtWidgets.QPushButton(tr('Buttons - Cancel', 'Cancel'))
        btn_cancel.setObjectName('DialogButton')
        btn_cancel.clicked.connect(self.reject)

        title = QtWidgets.QLabel(title, font=QtGui.QFont('Open Sans', 24, 600))
        title.setObjectName('Label')
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        text = QtWidgets.QLabel(text, font=QtGui.QFont('Open Sans', 18, 400))
        text.setObjectName('Label')
        text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(get_dialog_icon(icon_type), 0, 2)
        layout.addWidget(title, 1, 0, 1, 5)
        layout.addWidget(text, 2, 0, 1, 5)
        layout.addWidget(btn_cancel, 3, 0, 1, 2)
        layout.addWidget(btn_ok, 3, 3, 1, 2)

        self.wrapper = QtWidgets.QWidget()
        self.wrapper.setObjectName('Wrapper')
        self.wrapper.setLayout(layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.wrapper)

        self.setLayout(main_layout)

    def accept(self) -> None:
        self.is_accepted = True
        return super().accept()

    def reject(self) -> None:
        return super().reject()
