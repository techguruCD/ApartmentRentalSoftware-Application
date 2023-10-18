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
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

from widgets.elements import (
    InputWrapper
)

tr = QCoreApplication.translate
# Name!, Last Name!, Phone!, Mail!, Parents' Address, Parents' Phone, Note [text field]
class TenantPage(QFrame):
    def __init__(self, parent: QWidget | None):
        super().__init__(parent)
        self.setWindowTitle(tr('TenantPage - Title', 'Tenant'))
        self.__init_UI()
    def __init_UI(self):
        self.setObjectName("Window")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.name = QLineEdit(self)
        self.name.setObjectName('Input')
        self.last_name = QLineEdit(self)
        self.last_name.setObjectName('Input')
        name_layout = QHBoxLayout()
        name_layout.addWidget(InputWrapper(tr('Widgets - First Name', 'First Name'), self.name))
        name_layout.addWidget(InputWrapper(tr('Widgets - Last Name', 'Last Name'), self.last_name))

        self.phone = QLineEdit(self)
        self.phone.setObjectName('Input')
        self.mail = QLineEdit(self)
        self.mail.setObjectName('Input')
        contact_layout = QHBoxLayout()
        contact_layout.addWidget(InputWrapper(tr('Widgets - Phone', 'Phone'), self.phone))
        contact_layout.addWidget(InputWrapper(tr('Widgets - Mail', 'Mail'), self.mail))

        self.parent_address = QLineEdit(self)
        self.parent_address.setObjectName('Input')
        self.parent_phone = QLineEdit(self)
        self.parent_phone.setObjectName('Input')
        parent_contact_layout = QHBoxLayout()
        parent_contact_layout.addWidget(InputWrapper(tr("Widgets - Parents' address", "Parents' address"), self.parent_address))
        parent_contact_layout.addWidget(InputWrapper(tr("Widgets - Parents' phone", "Parents' phone"), self.parent_phone))

        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        self.button_back = QPushButton(icon=QIcon('data/arrow-long-left.svg'), parent=self)
        self.button_back.setObjectName('IconButton')
        self.button_back.setIconSize(QSize(24, 24))
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.button_back)
        back_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.button_save = QPushButton(tr('Widgets - Save', 'Save'), self)
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.button_save)
        control_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(back_layout)
        layout.addLayout(name_layout)
        layout.addLayout(contact_layout)
        layout.addLayout(parent_contact_layout)
        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note))
        layout.addLayout(control_layout)

        self.setLayout(layout)