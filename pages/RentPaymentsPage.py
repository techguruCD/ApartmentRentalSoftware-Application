from PySide6 import(
    QtCore,
    QtGui,
    QtWidgets
)
from widgets.elements import (
    InputWrapper,
    CustomWindow
)
from api import (
    TransactionApi
)
from tablemodels.RentPaymentsTableModel import RentPaymentsTableModel
from widgets.dialogs import Dialog


tr = QtCore.QCoreApplication.translate

class RentPaymentsPage(CustomWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(tr('RentPaymentsPage - Title', 'Rent payments'))
        self._next_page = None
        self._previous_page = None

        self.__init_UI()

        self.update_data()
        self.table_view.resizeColumnsToContents()

        self.show()

    def __init_UI(self):
        self.setObjectName('Window')

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.search = QtWidgets.QLineEdit()
        self.search.setObjectName('Input')
        self.search.setPlaceholderText('🔍')
        self.search.textChanged.connect(lambda _: self.update_data())

        self.table_model = RentPaymentsTableModel([])
        self.table_view = QtWidgets.QTableView()
        self.table_view.setObjectName('Table')
        self.table_view.setModel(self.table_model)

        self.table_view.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)
        self.table_view.doubleClicked.connect(self.__table_click)
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

        button_save = QtWidgets.QPushButton(tr('Buttons - Save', 'Save'))
        button_save.setObjectName('DialogButton')
        button_save.clicked.connect(self.save)

        button_cancel = QtWidgets.QPushButton(tr('Buttons - Cancel', 'Cancel'))
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)

        layout.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search), 0, 0, 1, 5, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.table_view, 1, 0, 1, 5)
        layout.addWidget(self.button_previous, 2, 0)
        layout.addWidget(self.button_next, 2, 4)

        layout.addWidget(button_save, 3, 0, 1, 2)
        layout.addWidget(button_cancel, 3, 3, 1, 2)

        self.widget.setLayout(layout)

    def __table_click(self, index: QtCore.QModelIndex):
        self.Signal.emit({'window': 'lease_contract', 'id': self.table_model._data[index.row()]['lease_contract']['id']})

    def update_data(self, final_url: str = None):
        search = self.search.text()
        if search == '':
            search = None

        success, data = TransactionApi.rent_payments_list(search=search, final_url=final_url)
        if success:
            self.table_model = RentPaymentsTableModel(data['results'])
            self.table_view.setModel(self.table_model)

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

    def save(self):
        for transaction in filter(lambda row: row['changed'], self.table_model._data):
            if not TransactionApi.update_transaction(transaction):
                dialog = Dialog(tr('Dialog - Error title', 'Update error'),
                                tr('Dialog - Error text', 'An error occurred while updating data!'),
                                'error')
                if dialog.is_accepted:
                    self.close()
                return

        self.close()

    def cancel(self):
        self.close()
