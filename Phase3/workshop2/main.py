import sys
from PySide6.QtWidgets import QApplication
from window import Window


def main() -> None:
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()