from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from PySide_Widgets import NamedVObjectLayout
from widgets.elements import ImputWrapper

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

class UtilityDialog(QtWidgets.QDialog):
    def __init__(self, electricity: float = 0, water: float = 0, tax: float = 0) -> None:
        super().__init__()

        self.setObjectName('Window')

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.electricity_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=electricity)
        self.electricity_field.setObjectName('Input')

        self.water_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=water)
        self.water_field.setObjectName('Input')

        self.tax_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=tax)
        self.tax_field.setObjectName('Input')

        button_accept = QtWidgets.QPushButton('Ok')
        button_accept.setObjectName('DialogButton')

        layout.addWidget(ImputWrapper(tr('UtilityDialog - Electricity', 'Electricity'), self.electricity_field))
        layout.addWidget(ImputWrapper(tr('UtilityDialog - Water', 'Water'), self.water_field))
        layout.addWidget(ImputWrapper(tr('UtilityDialog - Tax', 'Tax'), self.tax_field))
        layout.addWidget(button_accept)

        self.setLayout(layout)
