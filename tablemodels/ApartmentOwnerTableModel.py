from PySide6 import (
    QtCore,
    QtGui,
    QtWidgets
)
from settings import colors
tr = QtCore.QCoreApplication.translate

# Name of the apartment, Phone number, First and Last name of the owner
class ApartmentOwnerTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
    
    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 1:
            flags |= QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        return flags

    def data(self, index, role):
        row = index.row()
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            return QtCore.Qt.AlignmentFlag.AlignCenter

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            match index.column():
                case 0: # id
                    return self._data[row]['id']
                case 1: # apartment name
                    return self._data[row]['apartment']['name']
                case 2: # phone
                    return self._data[row]['phone']
                case 3: # owner name
                    return self._data[row]['first_name'] + ' ' + self._data[row]['last_name'],

        # change colors
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 != 0:
                return QtGui.QColor(colors['table_color_1'])
            else:
                return QtGui.QColor(colors['table_color_2'])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                match section:
                    case 0:
                        return 'id'
                    case 1:
                        return tr('ApartmentOwnerTableModel - Apartment name', 'Apartment name')
                    case 2:
                        return tr('ApartmentOwnerTableModel - Phone', 'Phone')
                    case 3:
                        return tr('ApartmentOwnerTableModel - Owner name', 'Owner name')
        
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4