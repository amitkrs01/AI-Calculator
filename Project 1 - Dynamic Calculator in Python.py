import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Calculator")
        self.initUI()
        self.current_operand = ""
        self.first_num = None
        self.operator = None

    def initUI(self):
        main_layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setStyleSheet("font-size: 30px; padding: 5px;")
        self.display.setAlignment(QtCore.Qt.AlignRight) # Need to import QtCore
        main_layout.addWidget(self.display)

        grid_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4) # C button spans all 4 columns
        ]

        for btn_text, row, col, *span in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.on_button_click)
            if span:
                grid_layout.addWidget(button, row, col, *span)
            else:
                grid_layout.addWidget(button, row, col)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def on_button_click(self):
        sender = self.sender().text()

        if sender.isdigit() or sender == '.':
            self.current_operand += sender
            self.display.setText(self.current_operand)
        elif sender in ['+', '-', '*', '/']:
            if self.first_num is None:
                self.first_num = float(self.current_operand)
            else:
                self.calculate() # Calculate previous operation if one exists
            self.operator = sender
            self.current_operand = ""
        elif sender == '=':
            self.calculate()
            self.operator = None # Reset operator after equals
        elif sender == 'C':
            self.current_operand = ""
            self.first_num = None
            self.operator = None
            self.display.setText("")

    def calculate(self):
        if self.first_num is None or not self.current_operand:
            return

        try:
            second_num = float(self.current_operand)
            result = 0
            if self.operator == '+':
                result = self.first_num + second_num
            elif self.operator == '-':
                result = self.first_num - second_num
            elif self.operator == '*':
                result = self.first_num * second_num
            elif self.operator == '/':
                if second_num == 0:
                    self.display.setText("Error")
                    self.first_num = None
                    self.current_operand = ""
                    return
                result = self.first_num / second_num
            
            self.display.setText(str(result))
            self.first_num = result # Allow chaining operations
            self.current_operand = str(result) # Set current operand to result for display/next operation
        except Exception as e:
            self.display.setText("Error")
            self.first_num = None
            self.current_operand = ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Import QtCore for AlignRight
    from PyQt5 import QtCore 
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())