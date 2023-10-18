from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
tr = QtCore.QCoreApplication.translate
from tablemodels.RentPaymentTableModel import (
    RentPaymentTableModel
)
import widgets.dialogs as dialogs
from pages.RentPaymentPage import (
    RentPaymentPage
)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setCentralWidget(RentPaymentPage())

        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    styles = open("data/styles.qss", 'r').read()
    app.setStyleSheet(styles)
    app.setStyle('Fusion')

    window = MainWindow()
    app.exec()