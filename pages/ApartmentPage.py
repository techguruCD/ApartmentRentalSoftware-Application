from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize,
    QModelIndex
)
from PySide6.QtGui import (
    QIcon
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QPlainTextEdit,
    QTableView,
    QLabel,
    QComboBox,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

from api import ApartmentApi, TransactionApi
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.TransactionTableModel import TransactionTableModel

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class ApartmentPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('ApartmentPage - Title', 'Apartment'))
        self._next_page = None
        self._previous_page = None

        self.__init_UI()

        self.update_data()
        self.table_view.resizeColumnsToContents()

    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        layout_back = QHBoxLayout()
        layout_back.addWidget(self.button_back)
        layout_back.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # self.label_title = QLabel(tr('TenantListPage - Title', 'Tenant List'), self)
        # self.label_title.setObjectName('TitleLabel')

        self.search = QLineEdit(self)
        self.search.setObjectName('Input')
        self.search.setPlaceholderText('🔍')
        self.combo_status = QComboBox(self)
        self.combo_status.setObjectName('Input')
        self.combo_status.addItem('All')
        self.combo_status.addItem('Income')
        self.combo_status.addItem('Expense')
        layout_search = QHBoxLayout()
        layout_search.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search))
        layout_search.addWidget(InputWrapper(tr('Widgets - Status', 'Status'), self.combo_status))

        self.table_model = TransactionTableModel([])
        self.table_view = QTableView(self)
        self.table_view.setObjectName('Table')
        self.table_view.setModel(self.table_model)

        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table_view.doubleClicked.connect(self.table_click)
        self.table_view.hideColumn(0)

        self.button_next = QPushButton(icon=QIcon('data/arrow-long-right.svg'))
        self.button_next.setObjectName('IconButton')
        self.button_next.setIconSize(QSize(24, 24))
        self.button_next.clicked.connect(self.next_page)
        self.button_next.setDisabled(True)
        self.button_previous = QPushButton(icon=QIcon('data/arrow-long-left.svg'))
        self.button_previous.setObjectName('IconButton')
        self.button_previous.setIconSize(QSize(24, 24))
        self.button_previous.clicked.connect(self.previous_page)
        self.button_previous.setDisabled(True)

        self.button_new_transaction = QPushButton(tr('Buttons - New Transaction', 'New Transaction'), self)
        self.button_new_transaction.setObjectName('LightBlueButton')
        self.button_tasks_reminders = QPushButton(tr('Buttons - Tasks and Reminders', 'Tasks and Reminders'), self)
        self.button_tasks_reminders.setObjectName('LightBlueButton')
        self.button_reports = QPushButton(tr('Buttons - Reports', 'Reports'), self)
        self.button_reports.setObjectName('LightBlueButton')
        self.button_seal = QPushButton(tr('Buttons - Seal', 'Seal'), self)
        self.button_seal.setObjectName('GreenButton')
        self.button_export = QPushButton(tr('Buttons - Export', 'Export'), self)
        self.button_export.setObjectName('GreenButton')
        self.button_details = QPushButton(tr('Buttons - Details', 'Details'), self)
        self.button_details.setObjectName('BlueButton')
        self.button_details.clicked.connect(self.detail_clicked)

        self.panel_detail = QWidget(self)
        self.name = QLineEdit(self)
        self.name.setObjectName('Input')
        self.address = QLineEdit(self)
        self.address.setObjectName('Input')
        self.city = QLineEdit(self)
        self.city.setObjectName('Input')
        layout_panel_1 = QHBoxLayout()
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - Name', 'Name'), self.name))
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - Address', 'Address'), self.address))
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - City', 'City'), self.city))

        self.rooms = QLineEdit(self)
        self.rooms.setObjectName('Input')
        self.area = QLineEdit(self)
        self.area.setObjectName('Input')
        self.floor = QLineEdit(self)
        self.floor.setObjectName('Input')
        layout_panel_2 = QHBoxLayout()
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Rooms', 'Rooms'), self.rooms))
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Area', 'Area'), self.area))
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Floor', 'Floor'), self.floor))

        self.beds = QLineEdit(self)
        self.beds.setObjectName('Input')
        self.owner = QLineEdit(self)
        self.owner.setObjectName('Input')
        layout_panel_3 = QHBoxLayout()
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Beds', 'Beds'), self.beds))
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Owner', 'Owner'), self.owner))
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        layout_panel = QVBoxLayout()
        layout_panel.addLayout(layout_panel_1)
        layout_panel.addLayout(layout_panel_2)
        layout_panel.addLayout(layout_panel_3)
        layout_panel.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note))

        self.panel_detail.setLayout(layout_panel)
        self.panel_detail.hide()

        button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        button_save.setObjectName('DialogButton')
        button_save.clicked.connect(self.save)
        button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)
        layout_save = QHBoxLayout()
        layout_save.addWidget(button_save)
        layout_save.addWidget(button_cancel)

        layout_control = QVBoxLayout()
        layout_control.addWidget(self.button_new_transaction)
        layout_control.addWidget(self.button_tasks_reminders)
        layout_control.addWidget(self.button_reports)
        layout_control.addWidget(self.button_seal)
        layout_control.addWidget(self.button_export)
        layout_control.addWidget(self.button_details)
        layout_control.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(layout_back, 0, 0, 1, 4)
        layout.addLayout(layout_search, 1, 0, 1, 3)
        layout.addWidget(self.table_view, 2, 0, 1, 3)
        layout.addWidget(self.button_previous, 3, 0)
        layout.addWidget(self.button_next, 3, 2)
        layout.addLayout(layout_control, 2, 3, 2, 1)
        layout.addWidget(self.panel_detail, 4, 0, 1, 4)
        layout.addLayout(layout_save, 5, 0, 1, 4)
        # layout.addWidget(self.panel_detail, 2, 4, 2, 1)
        # layout.addLayout(layout_save, 4, 0, 1, 5)
        layout.setRowStretch(2, 1)
        self.widget.setLayout(layout)

    def table_click(self, index: QModelIndex):
        self.Signal.emit({'window': 'tenantList', 'id': self.table_model._data[index.row()]['id']})

    def update_data(self, final_url: str = 0):
        search = self.search.text()

        success, data = TransactionApi.transaction_list(search, final_url)
        if success:
            self.table_model = TransactionTableModel(data['results'])
            self.table_view.setModel(self.table_model)

            if (data['previous']) is None:
                self.button_previous.setDisabled(True)
            else:
                self.button_previous.setDisabled(False)
                self._previous_page = data['previous']
            
            if data['next'] is None:
                self.button_next.setDisabled(True)
            else:
                self.button_next.setDisabled(False)
                self._next_page = data['next']

    def detail_clicked(self):
        self.panel_detail.setVisible(not self.panel_detail.isVisible())
    
    def next_page(self):
        self.update_data(final_url=self._previous_page)
    
    def previous_page(self):
        self.update_data(final_url=self._previous_page)

    def save(self):
        # data = {
        #     'first_name': self.first_name.text(),
        #     'last_name': self.last_name.text(),
        #     'phone': self.phone.text(),
        #     'mail': self.mail.text(),
        #     'parent_address': self.parent_address.text(),
        #     'parent_phone': self.parent_phone.text(),
        #     'note': self.note.toPlainText()
        # }
        if not ApartmentApi.apartment_save(None):
            dialog = Dialog(tr('TenantPage - Error title', 'Save error'),
                            tr('TenantPage - Error text', 'An error occurred while updating data!'),
                            'error')
            if dialog.is_accepted:
                self.SignalClose.emit()

    def cancel(self):
        self.SignalClose.emit()