from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout, QWidget)
 
import sys
import os
from shutil import copyfile
 
class Dialog(QDialog):
 
    def __init__(self):
        super(Dialog, self).__init__()
        # if file exists, read from file, else use pre-defined variables
        if os.path.exists('input.txt') == True:
            self.read_file()
        else:
            self.parameter_dictionary()

        # decide number of columns according to the amount of variables
        self.devide_row() # calculate column number
        box = [] # box storage each column
        for i in range(self.column_number):
            box.append(self.createFormGroupBox('group'+str(i), self.sub_var[i]))

        # ok and cancel bottons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        mainLayout = QHBoxLayout()
        # add column boxed to the dialog
        for i in range(self.column_number):
            mainLayout.addWidget(box[i])
        mainLayout.addWidget(buttonBox) # add bottons
        self.setLayout(mainLayout)
        self.setWindowTitle("FUNWAVE input parameters") # set window title
 
    def createFormGroupBox(self, var_group, var_dic):
        formGroupBox = QGroupBox(var_group)
        layout = QFormLayout()
        self.values = []
        nn = 0

        if os.path.exists('input.txt') == True:
            for i in var_dic:
                # read the value and fill into the box
                var_dic[i].setText(var_dic[i].value)
                layout.addRow(QLabel(i), var_dic[i])
        else:
            for i in self.vars:
                # creat box
                layout.addRow(QLabel(i), self.vars[i])

        formGroupBox.setLayout(layout)

        return formGroupBox

    ## for here, add pre-defined variables and type line by line
    def parameter_dictionary(self):
        vars = {}
        self.var_to_dic(vars,'nkx','integer')
        self.var_to_dic(vars,'nky','integer')
        self.var_to_dic(vars,'dt','float')
        self.var_to_dic(vars,'path','string')
        self.var_to_dic(vars,'logical_test','logical')
        self.vars = vars

    # add a vew key and value to the dictionary
    def var_to_dic(self, vars, var_name, var_type):
        a = QLineEdit()
        a.value_type = var_type
        vars.update({var_name:a})

    # read from the input.txt file
    def read_file(self):
        self.vars1 = {}
        self.vars = {}
        f = open('input.txt')
        for line in f:
            if ('=' in list(line) and '!' not in list(line)):
                value = line[line.rindex('=')+1:-1]
                var = line[0:line.rindex('=')]
                value = value.strip()
                var = var.strip()
                ed = QLineEdit()
                ed.value = value
                ed.value_type = self.input_type(value)
                self.vars.update({var:ed})

    # determine the input type
    def input_type(self, value):
        value_type = 'unknown'
        if (value == 'T' or value == 'F'):
            value_type = 'logical'
        elif value == '':
            value_type = 'unknown'
        elif value.replace('.','',1).isdigit() == False:
            value_type = 'string'
        elif '.' in list(value):
            value_type = 'float'
        elif value.isdigit():
            value_type = 'integer'

        return value_type

    # devide the columns
    def devide_row(self):
        self.sub_var = []
        self.column_number = 0
        if len(list(self.vars.items())) < 10:
            self.column_number = 1
        elif len(list(self.vars.items())) < 30:
            self.column_number = 2
        elif len(list(self.vars.items())) < 60:
            self.column_number = 3
        elif len(list(self.vars.items())) < 100:
            self.column_number = 4
        else:
            self.column_number = 5

        devide_length = len(list(self.vars.items())) / self.column_number
        for i in range(self.column_number):
            start = int(i * devide_length)
            end = int((i+1) * devide_length)
            self.sub_var.append(dict(list(self.vars.items())[start:end]))

# class for writing to file
class var_to_file():
    def __init__(self, vars):
        self.vars = vars # get value from the QDialog class
        self.debug_tool_for_muggles() # check if there is wrong type
        # if correct, generate the file:
        if self.error_dics == {}:
            self.write_to_file()

    def write_to_file(self):
        f = open('input.txt','w')
        for item in self.vars:
            string_value = self.vars[item].text()
            if self.vars[item].value_type == 'float':
                if '.' not in list(string_value):
                    string_value = string_value+'.0'
                elif list(string_value)[-1] == '.':
                    string_value = string_value+'0'

            f.write(item + ' = ' + string_value + '\n')
            print(item, self.vars[item].value_type)

    # sigh...muggles
    def debug_tool_for_muggles(self):
        self.error_dics = {}
        for item in self.vars:
            v_type = self.vars[item].value_type
            v_type.strip()
            if self.vars[item].text() == '':
                self.vars[item].value_type = 'unknown'
            else:
                if v_type == 'logical':
                    if (self.vars[item].text() != 'T' and self.vars[item].text() != 'F'):
                        self.error_dics.update({item:v_type})
                elif v_type == 'integer':
                    if self.vars[item].text().isdigit() == False:
                        self.error_dics.update({item:v_type})
                elif v_type == 'float':
                    if self.vars[item].text().replace('.','',1).isdigit() == False or '.' not in list(self.vars[item].text()):
                        self.error_dics.update({item:v_type})
                elif v_type == 'string':
                    if self.vars[item].text().replace('.','',1).isdigit() == True or self.vars[item].text() == 'T' or self.vars[item].text() == 'F':
                        self.error_dics.update({item:v_type})

        for item in self.error_dics:
             print(item + ' should be ' + self.error_dics[item] + '. Please correct')

# if the input.txt file exists, make a copy for backup
if os.path.exists('input.txt') == True:
    copyfile('input.txt', 'input_backup.txt')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog() # open dialog window
    if dialog.exec_():
        var_to_file(dialog.vars) # write data to "input.txt"
    sys.exit()
