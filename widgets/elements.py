from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)

class InputWrapper(QtWidgets.QFrame):
    def __init__(self, text: str, widget: QtWidgets.QWidget):
        super().__init__()

        self.setObjectName('InputWrapper')
        self.border = QtWidgets.QFrame(self)
        self.border.setObjectName('InputWrapperBorder')
        self.border.move(0,10)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        label = QtWidgets.QLabel(text, font=QtGui.QFont('Open Sans', 16, 400))

        layout.addWidget(label, 0, 0, 1, 3)
        layout.addWidget(widget, 1, 0, 1, 3)

        self.border.stackUnder(label)

        self.setLayout(layout)
        label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
    
    def resizeEvent(self, event) -> None:
        self.border.resize(self.width(), self.height() - 10)

