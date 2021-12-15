import sys
from typing import Union, Optional
from PySide6.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
from operator import add, sub, mul, truediv, and_, or_, not_, xor, pow, lshift, rshift

operations = {
    "+": add,
    "-": sub,
    "×": mul,
    "/": truediv,
    "x^n": pow
}

logical_operations = {
    "AND": and_,
    "OR": or_,
    "NOT": not_,
    "XOR": xor,
    "<<": lshift,
    ">>": rshift
}

error_zero_div = "Ділення на 0"
error_undefined = "Результат не знайдено"


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()
        self.ui.lbl_temp.clear()

        #digits
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)
        self.ui.btn_a.clicked.connect(self.add_digit)
        self.ui.btn_b.clicked.connect(self.add_digit)
        self.ui.btn_c.clicked.connect(self.add_digit)
        self.ui.btn_d.clicked.connect(self.add_digit)
        self.ui.btn_e.clicked.connect(self.add_digit)
        self.ui.btn_f.clicked.connect(self.add_digit)

        #actions
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negative)
        self.ui.btn_backspace.clicked.connect(self.backspace)
        self.ui.rbtn_hex.toggled.connect(self.radio_checked)
        self.ui.rbtn_dex.toggled.connect(self.radio_checked)
        self.ui.rbtn_bin.toggled.connect(self.radio_checked)

        #math
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(self.math_operation)
        self.ui.btn_sub.clicked.connect(self.math_operation)
        self.ui.btn_mul.clicked.connect(self.math_operation)
        self.ui.btn_div.clicked.connect(self.math_operation)
        self.ui.btn_square.clicked.connect(self.math_operation)
        self.ui.btn_and.clicked.connect(self.bin_operation)
        self.ui.btn_or.clicked.connect(self.bin_operation)
        self.ui.btn_not.clicked.connect(self.bin_operation)
        self.ui.btn_xor.clicked.connect(self.bin_operation)
        self.ui.btn_bit_left.clicked.connect(self.bin_operation)
        self.ui.btn_bit_right.clicked.connect(self.bin_operation)
        self.ui.btn_a.setEnabled(False)
        self.ui.btn_b.setEnabled(False)
        self.ui.btn_c.setEnabled(False)
        self.ui.btn_d.setEnabled(False)
        self.ui.btn_e.setEnabled(False)
        self.ui.btn_f.setEnabled(False)
        self.ui.btn_and.setEnabled(False)
        self.ui.btn_or.setEnabled(False)
        self.ui.btn_not.setEnabled(False)
        self.ui.btn_xor.setEnabled(False)
        self.ui.btn_bit_left.setEnabled(False)
        self.ui.btn_bit_right.setEnabled(False)

    def add_digit(self):
        self.remove_error()
        self.clear_temp_if_equality()
        btn = self.sender()

        digit_buttons = ("btn_0", "btn_1", "btn_2", "btn_3", "btn_4",
                         "btn_5", "btn_6", "btn_7", "btn_8", "btn_9",
                         "btn_a", "btn_b", "btn_c", "btn_d", "btn_e", "btn_f")
        if btn.objectName() in digit_buttons:
            if self.ui.le_entry.text() == "0":
                self.ui.le_entry.setText(btn.text())
            else:
                self.ui.le_entry.setText(self.ui.le_entry.text() + btn.text())

    def backspace(self) -> None:
        self.remove_error()
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and "-" in entry:
                self. ui.le_entry.setText("0")
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText("0")

    def clear_all(self) -> None:
        self.remove_error()
        self.ui.le_entry.setText("0")
        self.ui.lbl_temp.clear()

    def clear_entry(self) -> None:
        self.remove_error()
        self.clear_temp_if_equality()
        self.ui.le_entry.setText("0")

    def negative(self):
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()

        if "-" not in entry:
            if entry != "0":
                entry = "-" + entry
        else:
            entry = entry[1:]
        self.ui.le_entry.setText(entry)

        if len(entry) == self.entry_max_len + 1 and "-" in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)

    def clear_temp_if_equality(self) -> None:
        if self.get_math_sign() == "=":
            self.ui.lbl_temp.clear()

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == ".0" else n

    def add_point(self) -> None:
        self.clear_temp_if_equality()
        if "." not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + ".")

    def add_temp(self) -> None:
        btn = self.sender()

        if not self.ui.lbl_temp.text() or self.get_math_sign() == "=":
            self.ui.lbl_temp.setText(self.ui.le_entry.text() + f" {btn.text()} ")
            self.ui.le_entry.setText("0")

    def get_entry_num(self) -> Union[int, float]:
        entry = self.ui.le_entry.text().strip(".")
        return float(entry) if "." in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip(".").split()[0]
            return float(temp) if "." in temp else int(temp)

    def hex_get_temp_num(self) -> Union[int, None]:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip(".").split()[0]
            return int(temp, 16)

    def hex_get_entry_num(self) -> Union[int]:
        entry = self.ui.le_entry.text().strip(".")
        return int(entry, 16)

    def bin_get_temp_num(self) -> Union[int, None]:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip(".").split()[0]
            return int(temp, 2)

    def bin_get_entry_num(self) -> Union[int]:
        entry = self.ui.le_entry.text().strip(".")
        return int(entry, 2)

    def get_math_sign(self) -> Optional[str]:
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip(".").split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                )
                self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + " =")
                self.ui.le_entry.setText(result)
                return result
            except KeyError:
                pass

            except ZeroDivisionError:
                if self.get_temp_num() == 0:
                    self.show_error(error_undefined)
                else:
                    self.show_error(error_zero_div)

    def bin_calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            try:
                if self.get_math_sign() in operations:
                    result = bin(operations[self.get_math_sign()](self.bin_get_temp_num(), self.bin_get_entry_num()))
                else:
                    result = bin(logical_operations[self.get_math_sign()](self.bin_get_temp_num(), self.bin_get_entry_num()))
                self.ui.lbl_temp.setText(temp + entry + " =")
                self.ui.le_entry.setText(str(result))
                return result
            except KeyError:
                pass

    def hex_calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            try:
                result = hex(operations[self.get_math_sign()](self.hex_get_temp_num(), self.hex_get_entry_num()))
                self.ui.lbl_temp.setText(temp + entry + " =")
                self.ui.le_entry.setText(result[2:])
                return result[2:]
            except KeyError:
                pass

    def math_operation(self):
        temp = self.ui.lbl_temp.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == "=":
                    self.add_temp()
                elif self.get_math_sign() == "x^n":
                    self.ui.lbl_temp.setText(temp[:-4] + f"{btn.text()} ")
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f"{btn.text()} ")
            else:
                self.ui.lbl_temp.setText(self.calculate() + f" {btn.text()}")

    def bin_operation(self):
        temp = self.ui.lbl_temp.text()
        btn = self.sender()

        if not temp:
            self.add_temp()
        else:
            if self.get_math_sign() != btn.text():
                if self.get_math_sign() == "=":
                    self.add_temp()
                elif self.get_math_sign() == "OR" or self.get_math_sign() == "<<" or self.get_math_sign() == ">>":
                    self.ui.lbl_temp.setText(temp[:-3] + f"{btn.text()} ")
                else:
                    self.ui.lbl_temp.setText(temp[:-4] + f"{btn.text()} ")
            else:
                self.ui.lbl_temp.setText(self.bin_calculate() + f" {btn.text()}")

    def radio_checked(self):
        if self.ui.rbtn_hex.isChecked():
            self.ui.lbl_temp.clear()
            self.ui.le_entry.clear()
            self.ui.btn_calc.clicked.disconnect()
            self.ui.btn_calc.clicked.connect(self.hex_calculate)
            self.ui.btn_2.setEnabled(True)
            self.ui.btn_3.setEnabled(True)
            self.ui.btn_4.setEnabled(True)
            self.ui.btn_5.setEnabled(True)
            self.ui.btn_6.setEnabled(True)
            self.ui.btn_7.setEnabled(True)
            self.ui.btn_8.setEnabled(True)
            self.ui.btn_9.setEnabled(True)
            self.ui.btn_a.setEnabled(True)
            self.ui.btn_b.setEnabled(True)
            self.ui.btn_c.setEnabled(True)
            self.ui.btn_d.setEnabled(True)
            self.ui.btn_e.setEnabled(True)
            self.ui.btn_f.setEnabled(True)
            self.ui.btn_and.setEnabled(False)
            self.ui.btn_or.setEnabled(False)
            self.ui.btn_not.setEnabled(False)
            self.ui.btn_xor.setEnabled(False)
            self.ui.btn_bit_left.setEnabled(False)
            self.ui.btn_bit_right.setEnabled(False)

        elif self.ui.rbtn_dex.isChecked():
            self.ui.lbl_temp.clear()
            self.ui.le_entry.clear()
            self.ui.btn_calc.clicked.disconnect()
            self.ui.btn_calc.clicked.connect(self.calculate)
            self.ui.btn_2.setEnabled(True)
            self.ui.btn_3.setEnabled(True)
            self.ui.btn_4.setEnabled(True)
            self.ui.btn_5.setEnabled(True)
            self.ui.btn_6.setEnabled(True)
            self.ui.btn_7.setEnabled(True)
            self.ui.btn_8.setEnabled(True)
            self.ui.btn_9.setEnabled(True)
            self.ui.btn_a.setEnabled(False)
            self.ui.btn_b.setEnabled(False)
            self.ui.btn_c.setEnabled(False)
            self.ui.btn_d.setEnabled(False)
            self.ui.btn_e.setEnabled(False)
            self.ui.btn_f.setEnabled(False)
            self.ui.btn_and.setEnabled(False)
            self.ui.btn_or.setEnabled(False)
            self.ui.btn_not.setEnabled(False)
            self.ui.btn_xor.setEnabled(False)
            self.ui.btn_bit_left.setEnabled(False)
            self.ui.btn_bit_right.setEnabled(False)

        elif self.ui.rbtn_bin.isChecked():
            self.ui.lbl_temp.clear()
            self.ui.le_entry.clear()
            self.ui.btn_calc.clicked.disconnect()
            self.ui.btn_calc.clicked.connect(self.bin_calculate)
            self.ui.btn_square.setEnabled(False)
            self.ui.btn_2.setEnabled(False)
            self.ui.btn_3.setEnabled(False)
            self.ui.btn_4.setEnabled(False)
            self.ui.btn_5.setEnabled(False)
            self.ui.btn_6.setEnabled(False)
            self.ui.btn_7.setEnabled(False)
            self.ui.btn_8.setEnabled(False)
            self.ui.btn_9.setEnabled(False)
            self.ui.btn_a.setEnabled(False)
            self.ui.btn_b.setEnabled(False)
            self.ui.btn_c.setEnabled(False)
            self.ui.btn_d.setEnabled(False)
            self.ui.btn_e.setEnabled(False)
            self.ui.btn_f.setEnabled(False)
            self.ui.btn_and.setEnabled(True)
            self.ui.btn_or.setEnabled(True)
            self.ui.btn_not.setEnabled(True)
            self.ui.btn_xor.setEnabled(True)
            self.ui.btn_bit_left.setEnabled(True)
            self.ui.btn_bit_right.setEnabled(True)

    def show_error(self, text: str) -> None:
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)

    def remove_error(self) -> None:
        if self.ui.le_entry.text() in (error_undefined, error_zero_div):
            self.ui.le_entry.setMaxLength(self.entry_max_len)
            self.ui.le_entry.setText("0")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()
    sys.exit(app.exec())
