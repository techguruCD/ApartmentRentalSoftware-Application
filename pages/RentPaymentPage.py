from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from tablemodels.RentPaymentTableModel import RentPaymentTableModel
import api.RentPaymentApi as api
from widgets.elements import InputWrapper, CustomWindow

tr = QtCore.QCoreApplication.translate
label_font = QtGui.QFont('Open Sans', 16, 400)

class RentPaymentPage(CustomWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(tr('RentPaymentPage - Title', 'Rent payments'))
        self._next_page = None
        self._previous_page = None

        self.__init_UI()
        self.update_data()

        self.show()
    
    def __init_UI(self):
        self.setObjectName('Window')

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.search = QtWidgets.QLineEdit()
        self.search.setObjectName('Input')
        self.search.setPlaceholderText('🔍')

        self.table_model = RentPaymentTableModel([])
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName('Table')
        self.table_view.setModel(self.table_model)

        self.table_view.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)
        self.table_view.doubleClicked.connect(self.table_click)
        self.table_view.hideColumn(0)

        self.button_next = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-right.svg'))
        self.button_next.setObjectName('IconButton')
        self.button_next.setIconSize(QtCore.QSize(24, 24))
        self.button_next.clicked.connect(self.next_page)
        self.button_next.setDisabled(True)
        self.button_previous = QtWidgets.QPushButton(icon=QtGui.QIcon('data/arrow-long-left.svg'))
        self.button_previous.setObjectName('IconButton')
        self.button_previous.setIconSize(QtCore.QSize(24, 24))
        self.button_previous.clicked.connect(self.previous_page)
        self.button_previous.setDisabled(True)

        layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search), 0, 0, 1, 3)
        layout.addWidget(self.table_view, 1, 0, 1, 3)
        layout.addWidget(self.button_previous, 2, 0)
        layout.addWidget(self.button_next, 2, 2)

        self.widget.setLayout(layout)

    def table_click(self, index: QtCore.QModelIndex):
        pass

    def update_data(self, final_url: str = 0):
        search = self.search.text()

        success, data = api.rent_payment_list(search, final_url)
        if success:
            self.table_model = RentPaymentTableModel(data['results'])

            if data['previous'] is None:
                self.button_previous.setDisabled(True)
            else:
                self.button_previous.setDisabled(False)
                self._previous_page = data['previous']
            
            if data['next'] is None:
                self.button_next.setDisabled(True)
            else:
                self.button_next.setDisabled(False)
                self._next_page = data['next']
            
    def next_page(self):
        self.update_data(final_url=self._next_page)

    def previous_page(self):
        self.update_data(final_url=self._previous_page)
