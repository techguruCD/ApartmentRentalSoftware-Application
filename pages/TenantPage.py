from typing import Optional
import PySide6.QtCore
from PySide6.QtCore import (
    QCoreApplication,
    QSize
)
from PySide6.QtGui import (
    QIcon
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLineEdit,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QLabel
)

import api.TenantApi as api
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class TenantPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('TenantPage - Title', 'Tenant'))
        self.__init_UI()

    def __init_UI(self):
        self.setObjectName("Window")

        layout = QGridLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # self.label_title = QLabel(tr('TenantPage - Title', 'Tenant'), self)
        # self.label_title.setObjectName('TitleLabel')

        self.first_name = QLineEdit(self)
        self.first_name.setObjectName('Input')
        self.last_name = QLineEdit(self)
        self.last_name.setObjectName('Input')
        
        self.phone = QLineEdit(self)
        self.phone.setObjectName('Input')
        self.mail = QLineEdit(self)
        self.mail.setObjectName('Input')
        
        self.parent_address = QLineEdit(self)
        self.parent_address.setObjectName('Input')
        self.parent_phone = QLineEdit(self)
        self.parent_phone.setObjectName('Input')
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        self.button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        self.button_save.setObjectName('DialogButton')
        self.button_save.clicked.connect(self.save)
        self.button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        self.button_cancel.setObjectName('DialogButton')
        self.button_cancel.clicked.connect(self.cancel)
        
        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - First Name', 'First Name'), self.first_name), 1, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Last Name', 'Last Name'), self.last_name), 1, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Phone', 'Phone'), self.phone), 2, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Mail', 'Mail'), self.mail), 2, 1, 1, 1)

        layout.addWidget(InputWrapper(tr("Widgets - Parents' address", "Parents' address"), self.parent_address), 3, 0, 1, 1)
        layout.addWidget(InputWrapper(tr("Widgets - Parents' phone", "Parents' phone"), self.parent_phone), 3, 1, 1, 1)

        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note), 4, 0, 1, 2)
        layout.addWidget(self.button_save, 5, 0, 1, 1)
        layout.addWidget(self.button_cancel, 5, 1, 1, 1)

        self.widget.setLayout(layout)

    def save(self):
        data = {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'phone': self.phone.text(),
            'mail': self.mail.text(),
            'parent_address': self.parent_address.text(),
            'parent_phone': self.parent_phone.text()
        }
        if not api.tenant_save(data):
            dialog = Dialog(tr('TenantPage - Error title', 'Save error'),
                            tr('TenantPage - Error text', 'An error occurred while updating data!'),
                            'error')
            if dialog.is_accepted:
                self.SignalClose.emit()
    def cancel(self):
        self.SignalClose.emit()