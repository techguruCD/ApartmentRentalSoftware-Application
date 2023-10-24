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

import api.TenantApi as api
from widgets.elements import InputWrapper, CustomWindow
from tablemodels.TenantTableModel import TenantTableModel

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class TenantListPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('TenantListPage - Title', 'Tenant List'))
        self._next_page = None
        self._previous_page = None
        self._current_page = None

        self.__init_UI()
        self.update_data()
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.resizeColumnsToContents()

        self.SignalUpdate.connect(self._update_data_signal_handler)

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
        self.combo_status.addItem('Active')
        self.combo_status.addItem('Inactive')
        layout_search = QHBoxLayout()
        layout_search.addWidget(InputWrapper(tr('Widgets - Search', 'Search'), self.search))
        layout_search.addWidget(InputWrapper(tr('Widgets - Status', 'Status'), self.combo_status))

        self.table_model = TenantTableModel([])
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

        self.button_new_tenant = QPushButton(tr('Widgets - New Tenant', 'New Tenant'), self)
        self.button_new_tenant.setObjectName('LightBlueButton')
        self.button_new_tenant.clicked.connect(self.new_tenant_click)
        self.button_tasks_reminders = QPushButton(tr('Widgets - Tasks and Reminders', 'Tasks and Reminders'), self)
        self.button_tasks_reminders.setObjectName('LightBlueButton')
        self.button_reports = QPushButton(tr('Widgets - Reports', 'Reports'), self)
        self.button_reports.setObjectName('LightBlueButton')
        self.button_seal = QPushButton(tr('Widgets - Seal', 'Seal'), self)
        self.button_seal.setObjectName('GreenButton')
        self.button_export = QPushButton(tr('Widgets - Export', 'Export'), self)
        self.button_export.setObjectName('GreenButton')
        self.button_update_rental_fee = QPushButton(tr('Widgets - Update Rental Fee', 'Update Rental Fee'), self)
        self.button_update_rental_fee.setObjectName('BlueButton')

        # button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'))
        # button_cancel.setObjectName('DialogButton')
        # button_cancel.clicked.connect(self.cancel)

        layout_control = QVBoxLayout()
        layout_control.addWidget(self.button_new_tenant)
        layout_control.addWidget(self.button_tasks_reminders)
        layout_control.addWidget(self.button_reports)
        layout_control.addWidget(self.button_seal)
        layout_control.addWidget(self.button_export)
        layout_control.addWidget(self.button_update_rental_fee)
        layout_control.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addLayout(layout_back, 0, 0, 1, 4)
        layout.addLayout(layout_search, 1, 0, 1, 3)
        layout.addWidget(self.table_view, 2, 0, 1, 3)
        layout.addWidget(self.button_previous, 3, 0)
        layout.addWidget(self.button_next, 3, 2)
        layout.addLayout(layout_control, 1, 3, 3, 1)
        # layout.addWidget(button_cancel, 4, 0, 1, 4)
        layout.setRowStretch(2, 1)
        self.widget.setLayout(layout)

    def table_click(self, index: QModelIndex):
        self.Signal.emit({'window': 'tenant', 'id': self.table_model._data[index.row()]['id']})

    def new_tenant_click(self):
        self.Signal.emit({'window': 'tenant'})

    def _update_data_signal_handler(self):
        self.update_data(self._current_page)

    def update_data(self, final_url: str = '1\n'):
        search = self.search.text()

        success, data = api.tenant_list(search, final_url)
        if success:
            self.table_model = TenantTableModel(data['results'])
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
            
            self._current_page = data['current']
    
    def next_page(self):
        self.update_data(final_url=self._previous_page)
    
    def previous_page(self):
        self.update_data(final_url=self._previous_page)