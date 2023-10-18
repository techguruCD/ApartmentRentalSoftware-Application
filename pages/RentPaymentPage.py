from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from tablemodels.RentPaymentTableModel import (
    RentPaymentTableModel
)
from widgets.elements import InputWrapper

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

class RentPaymentPage(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(tr('RentPaymentPage - Title', 'Rent payments'))
        self.__init_UI()

        self.show()
    
    def __init_UI(self):
        self.setObjectName('Window')

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.search = QtWidgets.QLineEdit()
        self.search.setObjectName('Input')

        self.table_model = RentPaymentTableModel([])
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName('Table')
        self.table_view.setModel(self.table_model)

        self.table_view.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)
        # self.table_view.doubleClicked.connect(self.table_click)
        self.table_view.hideColumn(0)

        self.button_next = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-right.svg'))
        self.button_next.setObjectName('IconButton')
        self.button_next.setIconSize(QtCore.QSize(24, 24))
        # self.button_next.clicked.connect(self.next_page)
        self.button_next.setDisabled(True)
        self.button_previous = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-left.svg'))
        self.button_previous.setObjectName('IconButton')
        self.button_previous.setIconSize(QtCore.QSize(24, 24))
        # self.button_previous.clicked.connect(self.previous_page)
        self.button_previous.setDisabled(True)

        layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search), 0, 0, 1, 3)
        layout.addWidget(self.table_view, 1, 0, 1, 3)
        layout.addWidget(self.button_previous, 2, 0)
        layout.addWidget(self.button_next, 2, 2)

        self.setLayout(layout)

    def update_data(self):
        search = self.search.text()

