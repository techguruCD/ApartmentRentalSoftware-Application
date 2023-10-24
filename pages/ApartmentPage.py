from typing import Optional
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

from api import ApartmentApi, TransactionApi, TenantApi
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog
from tablemodels.TransactionTableModel import TransactionTableModel
from tablemodels.ApartmentOwnerTableModel import ApartmentOwnerTableModel
from tablemodels.TenantTableModel import TenantTableModel

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class ApartmentPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('ApartmentPage - Title', 'Apartment'))
        
        self._next_page = None
        self._previous_page = None

        self._next_page_tenant = None
        self._previous_page_tenant = None

        self.__init_UI()

        self.update_data()
        self.update_data_tenant()
        # self.table_view.resizeColumnsToContents()

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
        self.table_view.setMinimumWidth(350)
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

        self.rooms = QLineEdit(self)
        self.rooms.setObjectName('Input')
        self.area = QLineEdit(self)
        self.area.setObjectName('Input')
        layout_panel_2 = QHBoxLayout()
        layout_panel_2.setContentsMargins(0, 0, 0, 0)
        layout_panel_2.setSpacing(20)
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Rooms', 'Rooms'), self.rooms))
        layout_panel_2.addWidget(InputWrapper(tr('Widgets - Area', 'Area'), self.area))

        self.floor = QLineEdit(self)
        self.floor.setObjectName('Input')
        self.beds = QLineEdit(self)
        self.beds.setObjectName('Input')
        layout_panel_3 = QHBoxLayout()
        layout_panel_3.setContentsMargins(0, 0, 0, 0)
        layout_panel_3.setSpacing(20)
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Floor', 'Floor'), self.floor))
        layout_panel_3.addWidget(InputWrapper(tr('Widgets - Beds', 'Beds'), self.beds))

        self.owner = QLineEdit(self)
        self.owner.setObjectName('Input')

        # owner_frame start
        self.owner_frame = QFrame(self)
        self.owner_frame.setObjectName('Frame')
        layout_tenant = QGridLayout()
        layout_tenant.setSpacing(20)

        label = QLabel(tr('ApartmentPage - Owner label', 'Owner'), font=QFont('Open Sans', 24, 600))
        label.setObjectName('Label')

        self.search_tenant = QLineEdit(self)
        self.search_tenant.setObjectName('Input')
        self.search_tenant.setPlaceholderText('🔍')

        self.table_model_tenant = ApartmentOwnerTableModel([])
        self.table_view_tenant = QTableView(self)
        self.table_view_tenant.setObjectName('Table')
        self.table_view_tenant.setModel(self.table_model_tenant)
        self.table_view_tenant.hideColumn(0)
        self.table_view_tenant.setMinimumHeight(100)

        self.button_next_tenant = QPushButton(icon=QIcon('data/arrow-long-right.svg'), parent=self)
        self.button_next_tenant.setObjectName('IconButton')
        self.button_next_tenant.setIconSize(QSize(24, 24))
        self.button_next_tenant.clicked.connect(self.next_page_tenant)
        self.button_next_tenant.setDisabled(True)

        self.button_previous_tenant = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_previous_tenant.setObjectName('IconButton')
        self.button_previous_tenant.setIconSize(QSize(24, 24))
        self.button_previous_tenant.clicked.connect(self.previous_page_tenant)
        self.button_previous_tenant.setDisabled(True)

        layout_tenant.addWidget(label, 0, 0, 1, 3)
        layout_tenant.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search_tenant), 1, 0, 1, 3)
        layout_tenant.addWidget(self.table_view_tenant, 2, 0, 1, 3)
        layout_tenant.addWidget(self.button_previous_tenant, 3, 0, 1, 1)
        layout_tenant.addWidget(self.button_next_tenant, 3, 2, 1, 1)

        self.owner_frame.setLayout(layout_tenant)
        # owner_frame end
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        layout_panel = QVBoxLayout()
        layout_panel.addWidget(InputWrapper(tr('Widgets - Identifier', 'Identifier'), self.identifier))
        layout_panel.addLayout(layout_panel_1)
        layout_panel.addLayout(layout_panel_2)
        layout_panel.addLayout(layout_panel_3)
        layout_panel.addWidget(InputWrapper(tr('Widgets - Owner', 'Owner'), self.owner))
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
        layout.addWidget(self.table_view, 2, 0, 1, 3)
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
    
    def update_data_tenant(self, final_url: str = '0\n'):
        search = self.search.text()

        success, data = TenantApi.tenant_list(search, final_url)
        if success:
            self.table_model_tenant = TenantTableModel(data['results'])
            self.table_view_tenant.setModel(self.table_model_tenant)

            if (data['previous']) is None:
                self.button_previous_tenant.setDisabled(True)
            else:
                self.button_previous_tenant.setDisabled(False)
                self._previous_page_tenant = data['previous']
            
            if data['next'] is None:
                self.button_next_tenant.setDisabled(True)
            else:
                self.button_next_tenant.setDisabled(False)
                self._next_page_tenant = data['next']

    def detail_clicked(self):
        self.panel_detail.setVisible(not self.panel_detail.isVisible())
    
    def next_page(self):
        self.update_data(final_url=self._previous_page)
    
    def previous_page(self):
        self.update_data(final_url=self._previous_page)

    def next_page_tenant(self):
        self.update_data(final_url=self._next_page_tenant)

    def previous_page_tenant(self):
        self.update_data(final_url=self._previous_page_tenant)

    def save(self):
        data = {
            'unique_identifier': self.identifier.text(),
            'name': self.name.text(),
            'address': self.address.text(),
            'city': self.city.text(),
            'rooms': self.rooms.text(),
            'apartment_area': self.area.text(),
            'floor': self.floor.text(),
            'beds': self.beds.text(),
            'owner': self.owner.text(),
            'note': self.note.toPlainText()
        }
        success, new_apartment = ApartmentApi.create_apartment(data)
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