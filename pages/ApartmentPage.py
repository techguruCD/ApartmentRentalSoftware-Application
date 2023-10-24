from typing import Optional
import uuid
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize,
    QModelIndex
)
from PySide6.QtGui import (
    QIcon,
    QFont
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QScrollArea,
    QSpinBox,
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

from api import ApartmentApi, TransactionApi, OwnerApi
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.TransactionTableModel import TransactionTableModel
from tablemodels.ApartmentOwnerTableModel import ApartmentOwnerTableModel

tr = QCoreApplication.translate
class ApartmentPage(CustomWindow):
    def __init__(self, id: int = None):
        super().__init__()
        self.setWindowTitle(tr('ApartmentPage - Title', 'Apartment'))

        self.__owner = None
        self.__id = id
        
        self._next_page_transaction = None
        self._previous_page_transaction = None

        self._next_page_owner = None
        self._previous_page_owner = None

        self.__init_UI()

        self.update_data_owner()
        self.table_view_transaction.resizeColumnsToContents()

        if self.__id is not None:
            self.__load_apartment()
            self.owner.setText(self.__owner['first_name'] + ' ' + self.__owner['last_name'])
            self.owner_frame.hide()
            self.owner_wrapper.show()
            self.update_data_transaction()
        else:
            self.identifier.setText(str(uuid.uuid4()))

    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        self.button_back.clicked.connect(self.cancel)
        layout_back = QHBoxLayout()
        layout_back.addWidget(self.button_back)
        layout_back.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.search_transaction = QLineEdit(self)
        self.search_transaction.setObjectName('Input')
        self.search_transaction.setPlaceholderText('🔍')
        self.combo_status = QComboBox(self)
        self.combo_status.setObjectName('Input')
        self.combo_status.addItem(tr('TransactionType - All', 'All'))
        self.combo_status.addItem(tr('TransactionType - Income', 'Income'))
        self.combo_status.addItem(tr('TransactionType - Expense', 'Expense'))
        layout_search = QHBoxLayout()
        layout_search.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_transaction))
        layout_search.addWidget(InputWrapper(tr('Widgets - Status', 'Status'), self.combo_status))
        layout_search.setStretch(0, 1)

        self.table_model_transaction = TransactionTableModel([])
        self.table_view_transaction = QTableView(self)
        self.table_view_transaction.setMinimumWidth(350)
        self.table_view_transaction.setObjectName('Table')
        self.table_view_transaction.setModel(self.table_model_transaction)

        self.table_view_transaction.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_view_transaction.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table_view_transaction.horizontalHeader().setStretchLastSection(True)
        self.table_view_transaction.doubleClicked.connect(self.table_click)
        self.table_view_transaction.hideColumn(0)

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

        self.identifier = QLineEdit(self)
        self.identifier.setObjectName('Input')

        self.name = QLineEdit(self)
        self.name.setObjectName('Input')
        self.address = QLineEdit(self)
        self.address.setObjectName('Input')
        self.city = QLineEdit(self)
        self.city.setObjectName('Input')
        layout_panel_1 = QHBoxLayout()
        layout_panel_1.setContentsMargins(0, 0, 0, 0)
        layout_panel_1.setSpacing(20)
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - Name', 'Name'), self.name))
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - Address', 'Address'), self.address))
        layout_panel_1.addWidget(InputWrapper(tr('Widgets - City', 'City'), self.city))

        self.rooms = QSpinBox(self)
        self.rooms.setObjectName('Input')
        self.area = QSpinBox(self)
        self.area.setObjectName('Input')
        layout_panel_2 = QHBoxLayout()
        layout_panel_2.setContentsMargins(0, 0, 0, 0)
        layout_panel_2.setSpacing(20)
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Rooms', 'Rooms'), self.rooms))
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Area', 'Area'), self.area))

        self.floor = QSpinBox(self)
        self.floor.setObjectName('Input')
        self.beds = QSpinBox(self)
        self.beds.setObjectName('Input')
        layout_panel_3 = QHBoxLayout()
        layout_panel_3.setContentsMargins(0, 0, 0, 0)
        layout_panel_3.setSpacing(20)
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Floor', 'Floor'), self.floor))
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Beds', 'Beds'), self.beds))

        self.owner = QPushButton(self)
        self.owner.setObjectName('Input')
        self.owner_wrapper = InputWrapper(tr('Widgets - Owner', 'Owner'), self.owner)
        self.owner_wrapper.hide()

        # owner_frame start
        self.owner_frame = QFrame(self)
        self.owner_frame.setObjectName('Frame')
        layout_owner = QGridLayout()
        layout_owner.setSpacing(20)

        label = QLabel(tr('ApartmentPage - Owner label', 'Owner'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_owner = QLineEdit(self)
        self.search_owner.setObjectName('Input')
        self.search_owner.setPlaceholderText('🔍')

        self.table_model_owner = ApartmentOwnerTableModel([])
        self.table_view_owner = QTableView(self)
        self.table_view_owner.setObjectName('Table')
        self.table_view_owner.setModel(self.table_model_owner)
        self.table_view_owner.hideColumn(0)
        self.table_view_owner.horizontalHeader().setStretchLastSection(True)
        self.table_view_owner.setMinimumHeight(200)
        self.table_view_owner.doubleClicked.connect(self.table_owner_click)

        self.button_next_owner = QPushButton(icon=QIcon('data/arrow-long-right.svg'), parent=self)
        self.button_next_owner.setObjectName('IconButton')
        self.button_next_owner.setIconSize(QSize(24, 24))
        self.button_next_owner.clicked.connect(self.next_page_owner)
        self.button_next_owner.setDisabled(True)

        self.button_previous_owner = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_previous_owner.setObjectName('IconButton')
        self.button_previous_owner.setIconSize(QSize(24, 24))
        self.button_previous_owner.clicked.connect(self.previous_page_owner)
        self.button_previous_owner.setDisabled(True)

        layout_owner.addWidget(label, 0, 0, 1, 3)
        layout_owner.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_owner), 1, 0, 1, 3)
        layout_owner.addWidget(self.table_view_owner, 2, 0, 1, 3)
        layout_owner.addWidget(self.button_previous_owner, 3, 0, 1, 1)
        layout_owner.addWidget(self.button_next_owner, 3, 2, 1, 1)

        self.owner_frame.setLayout(layout_owner)
        self.owner.clicked.connect(self.owner_wrapper.hide)
        self.owner.clicked.connect(self.owner_frame.show)
        # owner_frame end
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        layout_panel = QVBoxLayout()
        layout_panel.addWidget(InputWrapper(tr('Widgets - Identifier', 'Identifier'), self.identifier))
        layout_panel.addLayout(layout_panel_1)
        layout_panel.addLayout(layout_panel_2)
        layout_panel.addLayout(layout_panel_3)
        layout_panel.addWidget(self.owner_wrapper)
        layout_panel.addWidget(self.owner_frame)
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
        layout.addWidget(self.table_view_transaction, 2, 0, 1, 3)
        layout.addWidget(self.button_previous, 3, 0)
        layout.addWidget(self.button_next, 3, 2)
        layout.addLayout(layout_control, 1, 3, 3, 1)
        layout.addWidget(self.panel_detail, 4, 0, 1, 4)
        layout.addLayout(layout_save, 5, 0, 1, 4)
        # layout.addWidget(self.panel_detail, 2, 4, 2, 1)
        # layout.addLayout(layout_save, 4, 0, 1, 5)
        layout.setRowStretch(2, 1)


        scroll_widget = QWidget(self)
        scroll_widget.setObjectName('Window')
        scroll_widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(scroll)

        self.widget.setLayout(scroll_layout)

    def table_click(self, index: QModelIndex):
        self.Signal.emit({'window': 'transaction', 'id': self.table_model_transaction._data[index.row()]['id']})

    def table_owner_click(self, index: QModelIndex):
        self.owner_frame.hide()
        self.owner_wrapper.show()
        self.__owner = self.table_model_owner._data[index.row()]
        self.owner.setText(self.__owner['first_name'] + ' ' + self.__owner['last_name'])

    def update_data_transaction(self, final_url: str = 0):
        search = self.search_transaction.text()

        success, data = TransactionApi.transaction_list(search, final_url)
        if success:
            self.table_model_transaction = TransactionTableModel(data['results'])
            self.table_view_transaction.setModel(self.table_model_transaction)

            if (data['previous']) is None:
                self.button_previous.setDisabled(True)
            else:
                self.button_previous.setDisabled(False)
                self._previous_page_transaction = data['previous']
            
            if data['next'] is None:
                self.button_next.setDisabled(True)
            else:
                self.button_next.setDisabled(False)
                self._next_page_transaction = data['next']
    
    def update_data_owner(self, final_url: str = '0\n'):
        search = self.search_transaction.text()

        success, data = OwnerApi.owner_list(search, final_url)
        if success:
            self.table_model_owner = ApartmentOwnerTableModel(data['results'])
            self.table_view_owner.setModel(self.table_model_owner)

            if (data['previous']) is None:
                self.button_previous_owner.setDisabled(True)
            else:
                self.button_previous_owner.setDisabled(False)
                self._previous_page_owner = data['previous']
            
            if data['next'] is None:
                self.button_next_owner.setDisabled(True)
            else:
                self.button_next_owner.setDisabled(False)
                self._next_page_owner = data['next']

    def detail_clicked(self):
        self.panel_detail.setVisible(not self.panel_detail.isVisible())
    
    def next_page(self):
        self.update_data_transaction(final_url=self._next_page_transaction)
    
    def previous_page(self):
        self.update_data_transaction(final_url=self._previous_page_transaction)

    def next_page_owner(self):
        self.update_data_transaction(final_url=self._next_page_owner)

    def previous_page_owner(self):
        self.update_data_transaction(final_url=self._previous_page_owner)

    def save(self):
        data = {
            'unique_identifier': self.identifier.text(),
            'name': self.name.text(),
            'address': self.address.text(),
            'city': self.city.text(),
            'rooms': self.rooms.value(),
            'apartment_area': self.area.value(),
            'floor': self.floor.value(),
            'beds': self.beds.value(),
            'owner': self.__owner,
            'note': self.note.toPlainText()
        }
        if self.__id != None:
            data['id'] = self.__id
        success, apartment = ApartmentApi.update_apartment(data) if self.__id != None else ApartmentApi.create_apartment(data)
        if not success:
            dialog = Dialog(tr('Dialog - Error title', 'Update error'),
                            tr('Dialog - Error text', 'An error occurred while updating data!'),
                            'error')
            # if dialog.is_accepted:
            #     self.SignalClose.emit()
        else:
            dialog = Dialog(tr('ApartmentPage - Success title', 'Save success'),
                            tr('ApartmentPage - Success text', 'Save Success'),
                            'success')
            self.cancel()

    def cancel(self):
        self.Signal.emit({'window': 'back'})

    def __load_apartment(self):
        success, apartment = ApartmentApi.get_apartment(self.__id)
        if success:
            print(apartment)
            self.identifier.setText(apartment['unique_identifier'])
            self.name.setText(apartment['name'])
            self.address.setText(apartment['address'])
            self.city.setText(apartment['city'])
            self.rooms.setValue(apartment['rooms'])
            self.area.setValue(apartment['apartment_area'])
            self.floor.setValue(apartment['floor'])
            self.beds.setValue(apartment['beds'])
            self.note.setPlainText(apartment['note'])
            self.__owner = apartment['owner']
        else:
            Dialog(tr('Dialog - Error title', 'Update error'),
                tr('Dialog - Error text', 'An error occurred while load data!'),
                'error')