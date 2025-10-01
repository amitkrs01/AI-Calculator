import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QGridLayout, QHBoxLayout, QStackedWidget)
from PyQt5.QtCore import Qt
import math # Needed for scientific functions

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Calculator")
        self.setGeometry(100, 100, 400, 600) # Set initial window size
        self.initUI()
        self.current_expression = "" # Stores the full expression for scientific mode
        self.first_num = None
        self.operator = None
        self.waiting_for_second_operand = False
        self.mode = "normal" # Default mode

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- Display ---
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet("""
            font-size: 35px;
            padding: 5px;
            background-color: #333;
            color: white;
            border: 1px solid #555;
            border-radius: 5px;
        """)
        self.display.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.display)

        # --- Mode Switcher ---
        mode_layout = QHBoxLayout()
        self.normal_btn = QPushButton("Normal")
        self.scientific_btn = QPushButton("Scientific")
        
        self.normal_btn.setFixedSize(120, 40)
        self.scientific_btn.setFixedSize(120, 40)
        
        # Style the mode buttons
        self.normal_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #007bff; color: white; border-radius: 5px; } QPushButton:hover { background-color: #0056b3; }")
        self.scientific_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #6c757d; color: white; border-radius: 5px; } QPushButton:hover { background-color: #5a6268; }")


        self.normal_btn.clicked.connect(lambda: self.set_mode("normal"))
        self.scientific_btn.clicked.connect(lambda: self.set_mode("scientific"))
        
        mode_layout.addWidget(self.normal_btn)
        mode_layout.addWidget(self.scientific_btn)
        mode_layout.addStretch() # Pushes buttons to the left

        main_layout.addLayout(mode_layout)

        # --- Button Layouts (Normal and Scientific) ---
        self.stacked_widget = QStackedWidget() # A widget that allows stacking multiple widgets, showing only one at a time

        # Normal Buttons
        normal_buttons_widget = QWidget()
        normal_grid_layout = QGridLayout()
        normal_buttons = [
            ('C', 0, 0), ('CE', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3)
        ]
        self._add_buttons_to_layout(normal_grid_layout, normal_buttons, self.on_button_click)
        normal_buttons_widget.setLayout(normal_grid_layout)
        self.stacked_widget.addWidget(normal_buttons_widget)


        # Scientific Buttons
        scientific_buttons_widget = QWidget()
        scientific_grid_layout = QGridLayout()
        scientific_buttons = [
            ('(', 0, 0), (')', 0, 1), ('pi', 0, 2), ('e', 0, 3), ('C', 0, 4), ('CE', 0, 5),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('^', 1, 3), ('/', 1, 4), ('%', 1, 5),
            ('asin', 2, 0), ('acos', 2, 1), ('atan', 2, 2), ('sqrt', 2, 3), ('*', 2, 4), ('1/x', 2, 5),
            ('log', 3, 0), ('ln', 3, 1), ('e^x', 3, 2), ('10^x', 3, 3), ('-', 3, 4), ('!', 3, 5),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('+', 4, 3), ('4', 4, 4), ('5', 4, 5),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('0', 5, 3), ('.', 5, 4), ('=', 5, 5) # Example layout, you'd integrate 0-9 and basic ops here better
        ]
        # For simplicity, let's create a more complete scientific layout that includes numbers and basic ops
        # This will be larger, so let's adjust the window size if it's too small for your screen.
        scientific_full_buttons = [
            ('(', 0, 0), (')', 0, 1), ('%', 0, 2), ('C', 0, 3), ('CE', 0, 4), ('/', 0, 5),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('7', 1, 3), ('8', 1, 4), ('9', 1, 5),
            ('asin', 2, 0), ('acos', 2, 1), ('atan', 2, 2), ('4', 2, 3), ('5', 2, 4), ('6', 2, 5),
            ('log', 3, 0), ('ln', 3, 1), ('sqrt', 3, 2), ('1', 3, 3), ('2', 3, 4), ('3', 3, 5),
            ('pi', 4, 0), ('e', 4, 1), ('^', 4, 2), ('0', 4, 3), ('.', 4, 4), ('=', 4, 5),
            ('*', 1, 6), ('-', 2, 6), ('+', 3, 6), ('1/x', 4, 6), ('!', 5, 6), # Add some more ops for column 6
            ('exp', 5, 0), ('mod', 5, 1), ('x^2', 5, 2), ('x^3', 5, 3), ('rad', 5, 4), ('deg', 5, 5)
        ]
        self._add_buttons_to_layout(scientific_grid_layout, scientific_full_buttons, self.on_button_click)
        scientific_buttons_widget.setLayout(scientific_grid_layout)
        self.stacked_widget.addWidget(scientific_buttons_widget)

        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.set_mode("normal") # Set initial mode

        # Global stylesheet for all buttons
        self.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #6c757d; /* Gray for general buttons */
                color: white;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton[text="="] { background-color: #28a745; } /* Green for equals */
            QPushButton[text="="]:hover { background-color: #218838; }
            QPushButton[text="C"], QPushButton[text="CE"] { background-color: #dc3545; } /* Red for clear */
            QPushButton[text="C"]:hover, QPushButton[text="CE"]:hover { background-color: #c82333; }
            QPushButton[text="/"], QPushButton[text="*"], QPushButton[text="-"], QPushButton[text="+"] { background-color: #ffc107; color: #333; } /* Yellow for operators */
            QPushButton[text="/"]:hover, QPushButton[text="*"]:hover, QPushButton[text="-"]:hover, QPushButton[text="+"]:hover { background-color: #e0a800; }
            QPushButton[text="Normal"] { background-color: #007bff; } /* Blue for active normal mode */
            QPushButton[text="Normal"]:hover { background-color: #0056b3; }
            QPushButton[text="Scientific"] { background-color: #6c757d; } /* Gray for inactive scientific mode */
            QPushButton[text="Scientific"]:hover { background-color: #5a6268; }
        """)

    def _add_buttons_to_layout(self, layout, buttons_data, click_handler):
        for btn_text, row, col, *span in buttons_data:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)
            button.clicked.connect(click_handler)
            if span:
                layout.addWidget(button, row, col, *span)
            else:
                layout.addWidget(button, row, col)

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == "normal":
            self.stacked_widget.setCurrentIndex(0) # Show normal buttons
            self.normal_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #007bff; color: white; border-radius: 5px; } QPushButton:hover { background-color: #0056b3; }")
            self.scientific_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #6c757d; color: white; border-radius: 5px; } QPushButton:hover { background-color: #5a6268; }")
        else: # scientific mode
            self.stacked_widget.setCurrentIndex(1) # Show scientific buttons
            self.scientific_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #007bff; color: white; border-radius: 5px; } QPushButton:hover { background-color: #0056b3; }")
            self.normal_btn.setStyleSheet("QPushButton { font-size: 16px; background-color: #6c757d; color: white; border-radius: 5px; } QPushButton:hover { background-color: #5a6268; }")
        self.current_expression = "" # Clear expression on mode switch
        self.display.setText("")


    def on_button_click(self):
        sender = self.sender().text()

        if sender == 'C': # Clear all
            self.current_expression = ""
            self.display.setText("")
        elif sender == 'CE': # Clear entry
            if self.current_expression and self.current_expression[-1].isdigit():
                self.current_expression = self.current_expression[:-1]
            self.display.setText(self.current_expression)
        elif sender == '=':
            try:
                # Use Python's eval for simplicity, but for production, a safer parser is recommended.
                # Replace math functions for eval
                expression_to_evaluate = self.current_expression.replace('^', '**') \
                                                           .replace('log', 'math.log10') \
                                                           .replace('ln', 'math.log') \
                                                           .replace('sqrt', 'math.sqrt') \
                                                           .replace('pi', str(math.pi)) \
                                                           .replace('e', str(math.e)) \
                                                           .replace('sin', 'math.sin') \
                                                           .replace('cos', 'math.cos') \
                                                           .replace('tan', 'math.tan') \
                                                           .replace('asin', 'math.asin') \
                                                           .replace('acos', 'math.acos') \
                                                           .replace('atan', 'math.atan') \
                                                           .replace('x^2', '**2') \
                                                           .replace('x^3', '**3') \
                                                           .replace('1/x', '1/') \
                                                           .replace('exp', 'math.exp') \
                                                           .replace('mod', '%')

                # Handle factorial: find 'x!' and replace with math.factorial(x)
                import re
                def factorial_replacer(match):
                    num = int(match.group(1))
                    return str(math.factorial(num))
                expression_to_evaluate = re.sub(r'(\d+)!', factorial_replacer, expression_to_evaluate)
                
                # Check for radians/degrees
                if 'rad' in expression_to_evaluate:
                    expression_to_evaluate = expression_to_evaluate.replace('rad', '')
                    # Assume angles are input in degrees and convert to radians if 'rad' is used as a modifier
                    # This requires more complex parsing for functions like sin(45rad)
                    # For simplicity, let's assume 'rad' button just changes a global setting or is not a direct part of the expression
                    # For now, we'll just remove it and assume standard math.sin expects radians.
                    # A proper implementation would convert the arguments to sin/cos/tan before calling the math function.
                if 'deg' in expression_to_evaluate:
                    expression_to_evaluate = expression_to_evaluate.replace('deg', '')
                    # Similar to 'rad', this needs careful handling of argument conversion.

                result = str(eval(expression_to_evaluate, {"__builtins__": None}, {'math': math}))
                self.display.setText(result)
                self.current_expression = result # Allow chaining operations
            except Exception as e:
                self.display.setText("Error")
                self.current_expression = ""
        elif sender in ['pi', 'e']:
            self.current_expression += str(math.pi if sender == 'pi' else math.e)
            self.display.setText(self.current_expression)
        elif sender == 'x^2': # Specific scientific operations
            try:
                val = float(eval(self.current_expression, {"__builtins__": None}, {}))
                self.current_expression = str(val**2)
                self.display.setText(self.current_expression)
            except Exception:
                self.display.setText("Error")
                self.current_expression = ""
        elif sender == 'x^3':
            try:
                val = float(eval(self.current_expression, {"__builtins__": None}, {}))
                self.current_expression = str(val**3)
                self.display.setText(self.current_expression)
            except Exception:
                self.display.setText("Error")
                self.current_expression = ""
        elif sender == 'sqrt':
            self.current_expression += "math.sqrt("
            self.display.setText(self.current_expression)
        elif sender == 'log':
            self.current_expression += "math.log10("
            self.display.setText(self.current_expression)
        elif sender == 'ln':
            self.current_expression += "math.log("
            self.display.setText(self.current_expression)
        elif sender == 'e^x':
            self.current_expression += "math.exp("
            self.display.setText(self.current_expression)
        elif sender == '10^x':
            self.current_expression += "10**" # Or a function that takes an arg
            self.display.setText(self.current_expression)
        elif sender == '!':
            # This is a bit tricky with eval. It's better to parse before eval.
            # For simplicity, assume it's applied to the last number entered.
            # A more robust solution would be to use a proper expression parser.
            try:
                num = int(self.current_expression)
                self.current_expression = str(math.factorial(num))
                self.display.setText(self.current_expression)
            except ValueError:
                self.display.setText("Error")
                self.current_expression = ""
            except Exception: # if not a valid number for factorial
                self.display.setText("Error")
                self.current_expression = ""
        elif sender == '1/x':
            try:
                val = float(eval(self.current_expression, {"__builtins__": None}, {}))
                if val == 0:
                    self.display.setText("Error")
                    self.current_expression = ""
                else:
                    self.current_expression = str(1/val)
                    self.display.setText(self.current_expression)
            except Exception:
                self.display.setText("Error")
                self.current_expression = ""
        elif sender in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']:
            # Assume input is in radians for math module functions
            # A future improvement would be to add a Rad/Deg toggle
            self.current_expression += f"math.{sender}("
            self.display.setText(self.current_expression)
        elif sender in ['rad', 'deg']:
            # For now, these buttons don't directly modify the expression string
            # In a real scientific calculator, they would toggle a global setting
            # for angle units (radians vs. degrees)
            self.display.setText(f"Mode set to {sender.upper()}")
            # You would store this mode in a self.angle_unit variable (e.g., "radians", "degrees")
            # and use it to convert values before calling math.sin, math.cos, etc.
        else:
            self.current_expression += sender
            self.display.setText(self.current_expression)

    # Helper function for factorial evaluation if needed
    def factorial(self, n):
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0:
            return 1
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())