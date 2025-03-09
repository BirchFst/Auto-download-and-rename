import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image

class PhotoRenamer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Photo Renamer')

        self.input_label = QLabel('Enter new filename:')
        self.input_text = QLineEdit()
        self.input_text.returnPressed.connect(self.rename_photo)  # 绑定按下 Enter 键触发重命名操作
        self.rename_button = QPushButton('Rename')
        self.rename_button.clicked.connect(self.rename_photo)

        self.image_label = QLabel()
        self.image_label.setScaledContents(True)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.rename_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_next_image()

    def load_next_image(self):
        image_files = [f for f in os.listdir('download') if f.endswith('.jpg') or f.endswith('.png')or f.endswith('.jpeg')]
        if len(image_files) > 0:
            next_image_path = os.path.join('download', image_files[0])
            pixmap = QPixmap(next_image_path)
            self.current_image_path = next_image_path

            # 使用PIL库来调整图片大小为原来的1/3
            image = Image.open(self.current_image_path)
            resized_image = image.resize((image.width // 3, image.height // 3))
            resized_image = resized_image.convert('RGB')
            resized_image.save('temp_image.jpg')  # 保存临时的缩小后的图片
            pixmap = QPixmap('temp_image.jpg')

            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setPixmap(QPixmap())
            self.current_image_path = None

    def rename_photo(self):
        if self.current_image_path and self.input_text.text():
            new_filename = self.input_text.text() + '.jpg'  # You can change the extension if needed
            new_path = os.path.join('output', new_filename)
            image = Image.open(self.current_image_path)
            image = image.convert('RGB')
            image.save(new_path)
            os.remove(self.current_image_path)
            os.remove('temp_image.jpg')  # 删除临时的缩小后的图片
            self.load_next_image()
            self.input_text.clear()  # 清空输入框内容

if __name__ == '__main__':
    if not os.path.exists("./output"):
        os.mkdir("./output")  

    app = QApplication([])
    window = PhotoRenamer()
    window.show()
    app.exec_()
