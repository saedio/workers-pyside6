import sys
import time

# Verifica se o PySide6 está instalado
try:
    from PySide6.QtCore import QObject, QThread, Signal
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
except ImportError:
    print("PySide6 não está instalado. Instale com: python -m pip install PySide6")
    sys.exit(1)

# Worker 1
class Worker1(QObject):
    started = Signal(str)
    progressed = Signal(str)
    finished = Signal(str)

    def doWork(self):
        self.started.emit("0")
        for i in range(5):
            self.progressed.emit(str(i))
            time.sleep(1)
        self.finished.emit("5")

# Worker 2
class Worker2(QObject):
    started = Signal(str)
    progressed = Signal(str)
    finished = Signal(str)

    def executeMe(self):
        self.started.emit("50")
        for i in range(50, 100, 5):
            self.progressed.emit(str(i))
            time.sleep(0.3)
        self.finished.emit("95")

# Interface
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Workers Simultâneos")
        self.resize(300, 150)

        layout = QVBoxLayout()
        self.button1 = QPushButton("Iniciar Worker 1")
        self.label1 = QLabel("Worker 1: 0")
        self.button2 = QPushButton("Iniciar Worker 2")
        self.label2 = QLabel("Worker 2: 50")

        layout.addWidget(self.button1)
        layout.addWidget(self.label1)
        layout.addWidget(self.button2)
        layout.addWidget(self.label2)
        self.setLayout(layout)

        # Conexão dos botões
        self.button1.clicked.connect(self.startWorker1)
        self.button2.clicked.connect(self.startWorker2)

    # Worker 1
    def startWorker1(self):
        self.worker1 = Worker1()
        self.thread1 = QThread()

        self.worker1.moveToThread(self.thread1)
        self.thread1.started.connect(self.worker1.doWork)
        self.worker1.finished.connect(self.thread1.quit)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.worker1.finished.connect(self.worker1.deleteLater)

        self.worker1.started.connect(lambda v: self.label1.setText(f"Worker 1: {v}"))
        self.worker1.progressed.connect(lambda v: self.label1.setText(f"Worker 1: {v}"))
        self.worker1.finished.connect(lambda v: self.label1.setText(f"Worker 1: {v}"))
        self.worker1.finished.connect(lambda: self.button1.setDisabled(False))
        self.button1.setDisabled(True)

        self.thread1.start()

    # Worker 2
    def startWorker2(self):
        self.worker2 = Worker2()
        self.thread2 = QThread()

        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.executeMe)
        self.worker2.finished.connect(self.thread2.quit)
        self.thread2.finished.connect(self.thread2.deleteLater)
        self.worker2.finished.connect(self.worker2.deleteLater)

        self.worker2.started.connect(lambda v: self.label2.setText(f"Worker 2: {v}"))
        self.worker2.progressed.connect(lambda v: self.label2.setText(f"Worker 2: {v}"))
        self.worker2.finished.connect(lambda v: self.label2.setText(f"Worker 2: {v}"))
        self.worker2.finished.connect(lambda: self.button2.setDisabled(False))
        self.button2.setDisabled(True)

        self.thread2.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.exec()
