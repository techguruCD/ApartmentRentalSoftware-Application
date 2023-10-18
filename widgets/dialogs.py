from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from widgets.elements import InputWrapper

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

class UtilityDialog(QtWidgets.QDialog):
    def __init__(self, electricity: float = 0, water: float = 0, taxes: float = 0) -> None:
        super().__init__()

        self.is_accepted = False

        self.setObjectName('Window')

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.electricity_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=electricity)
        self.electricity_field.setObjectName('Input')

        self.water_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=water)
        self.water_field.setObjectName('Input')

        self.taxes_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=taxes)
        self.taxes_field.setObjectName('Input')

        button_accept = QtWidgets.QPushButton(tr('Buttons - Save', 'Save'))
        button_accept.setObjectName('DialogButton')
        button_accept.clicked.connect(self.accept)

        button_reject = QtWidgets.QPushButton(tr('Buttons - Cancel', 'Cancel'))
        button_reject.setObjectName('DialogButton')
        button_reject.clicked.connect(self.reject)

        layout.addWidget(InputWrapper(tr('UtilityDialog - Electricity', 'Electricity'), self.electricity_field), 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('UtilityDialog - Water', 'Water'), self.water_field), 1, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('UtilityDialog - Taxes', 'Taxes'), self.taxes_field), 2, 0, 1, 2)
        layout.addWidget(button_accept, 3, 0)
        layout.addWidget(button_reject, 3, 1)

        self.setLayout(layout)

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
            'taxes': self.taxes_field.value()
        }
