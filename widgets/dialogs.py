from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from PySide_Widgets import NamedHObjectLayout

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

class UtilityDialog(QtWidgets.QDialog):
    def __init__(self, electricity: float = 0, water: float = 0, tax: float = 0) -> None:
        super().__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        electricity_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=electricity)
        water_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=water)
        tax_field = QtWidgets.QDoubleSpinBox(minimum=0, maximum=999999999, value=tax)

        layout.addLayout(NamedHObjectLayout(tr('UtilityDialog - Electricity', 'Electricity'), electricity_field, 'left', font=label_font))
        layout.addLayout(NamedHObjectLayout(tr('UtilityDialog - Water', 'Water'), water_field, 'left', font=label_font))
        layout.addLayout(NamedHObjectLayout(tr('UtilityDialog - Tax', 'Tax'), tax_field, 'left', font=label_font))

        self.setLayout(layout)
