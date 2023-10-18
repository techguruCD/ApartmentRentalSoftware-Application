from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
tr = QtCore.QCoreApplication.translate
import tablemodels.tablemodels as tablemodels
import widgets.dialogs as dialogs

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        dialog =dialogs.UtilityDialog()
        dialog.exec()
        # widget = QtWidgets.QWidget()
        # layout = QtWidgets.QHBoxLayout()
        # widget.setLayout(layout)
        # model = tablemodels.RentPaymentTableModel([{'id': 0, 'paid': False, 'month': '10', 'amount': 1000, 'tenant': {'first_name': 'first_name', 'last_name': 'last_name'}, 'apartment': {'name': 'name'}}, {'id': 0, 'paid': False, 'month': '10', 'amount': 1000, 'tenant': {'first_name': 'first_name', 'last_name': 'last_name'}, 'apartment': {'name': 'name'}}])
        # table = QtWidgets.QTableView()
        # table.setObjectName('Table')
        # table.setModel(model)
        # self.setCentralWidget(widget)
        # layout.addWidget(table)
        # self.show()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()

    styles = open("data/styles.qss", 'r').read()
    app.setStyleSheet(styles)
    app.setStyle('Fusion')

    app.exec()