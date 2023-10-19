from typing import Optional
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
    QLabel,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

import api.ApartmentOwnerApi as api
from widgets.elements import InputWrapper, CustomWindow
from widgets.dialogs import Dialog

tr = QCoreApplication.translate
# First name!, Last name!, Phone!, Mail!, Note[Text field]
class ApartmentOwnerPage(CustomWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('ApartmentOwnerPage - Title', 'Apartment Owner'))
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

        # self.label_title = QLabel(tr('ApartmentOwnerPage - Title', 'Apartment Owner'), self)
        # self.label_title.setObjectName('TitleLabel')

        self.first_name = QLineEdit(self)
        self.first_name.setObjectName('Input')
        self.last_name = QLineEdit(self)
        self.last_name.setObjectName('Input')
        
        self.phone = QLineEdit(self)
        self.phone.setObjectName('Input')
        self.mail = QLineEdit(self)
        self.mail.setObjectName('Input')
        
        self.note = QPlainTextEdit(self)
        self.note.setObjectName('Input')

        button_save = QPushButton(tr('Buttons - Save', 'Save'), self)
        button_save.setObjectName('DialogButton')
        button_save.clicked.connect(self.save)
        button_cancel = QPushButton(tr('Buttons - Cancel', 'Cancel'), self)
        button_cancel.setObjectName('DialogButton')
        button_cancel.clicked.connect(self.cancel)
        
        layout.addLayout(back_layout, 0, 0, 1, 2)
        layout.addWidget(InputWrapper(tr('Widgets - First Name', 'First Name'), self.first_name), 1, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Last Name', 'Last Name'), self.last_name), 1, 1, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Phone', 'Phone'), self.phone), 2, 0, 1, 1)
        layout.addWidget(InputWrapper(tr('Widgets - Mail', 'Mail'), self.mail), 2, 1, 1, 1)

        layout.addWidget(InputWrapper(tr('Widgets - Note', 'Note'), self.note), 3, 0, 1, 2)
        layout.addWidget(button_save, 4, 0, 1, 1)
        layout.addWidget(button_cancel, 4, 1, 1, 1)

        self.widget.setLayout(layout)
    
    def save(self):
        data = {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'phone': self.phone.text(),
            'mail': self.mail.text(),
            'note': self.note.toPlainText()
        }
        if not api.apartment_owner_save(data):
            dialog = Dialog(tr('ApartmentOwnerPage - Error title', 'Update error'),
                            tr('ApartmentOwnerPage - Error text', 'An error occurred while updating data!'),
                            'error')
            if dialog.is_accepted:
                self.SignalClose.emit()

    def cancel(self):
        self.SignalClose.emit()
