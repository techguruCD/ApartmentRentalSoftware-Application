from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
tr = QtCore.QCoreApplication.translate

from pages.ReminderPage import (
    ReminderPage
)
import widgets.dialogs as dialogs

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
                
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        central = ReminderPage()
        central.connect_control_signals(self)
        self.setCentralWidget(central)

        self.show()

def addFont(file_name):
    with open(file_name, 'rb') as file:
        font = file.read()
        QtGui.QFontDatabase.addApplicationFontFromData(font)

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    addFont('data/Open_Sans/OpenSans-ExtraBold.ttf')
    addFont('data/Open_Sans/OpenSans-Bold.ttf')
    addFont('data/Open_Sans/OpenSans-SemiBold.ttf')
    addFont('data/Open_Sans/OpenSans-Medium.ttf')
    addFont('data/Open_Sans/OpenSans-Regular.ttf')
    addFont('data/Open_Sans/OpenSans-Light.ttf')

    styles = open("data/styles.qss", 'r').read()
    app.setStyleSheet(styles)
    app.setStyle('Fusion')

    window = MainWindow()
    app.exec()