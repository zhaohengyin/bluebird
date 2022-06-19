from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QTextEdit, QLabel
import sys
sys.path += ["./"]
from bluebird import *


class ChatRoom(QWidget):
	def __init__(self, chatroom_addr):
		super().__init__()
		self.initUI()
		self.chatroom_addr = chatroom_addr
		self.past_room_text = []
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_room_text)
		self.timer.start(100)

	def send_message(self):
		call_remote_func(self.chatroom_addr['host'], self.chatroom_addr['port'],
						 'add_msg', {'user': self.user_textbox.toPlainText(), 'text': self.textEdit.toPlainText()})

	def update_room_text(self):
		past_room_text = call_remote_func(self.chatroom_addr['host'], self.chatroom_addr['port'], 'get_history', {})
		if past_room_text is not None:
			self.past_room_text = past_room_text

		scrollbar = self.past_msg.verticalScrollBar()
		value = scrollbar.value()

		all_text = ''
		for (user, time, text) in self.past_room_text:
			all_text += '[{}] {}: {}\n'.format(time, user, text)

		self.past_msg.setText(all_text)
		scrollbar.setValue(value)

	def initUI(self):
		self.send = QPushButton('Send', self)
		self.send.clicked.connect(self.send_message)
		self.send.resize(self.send.sizeHint())
		self.send.move(850, 800)

		self.label = QLabel("Name:", self)
		self.label.move(50, 510)

		self.user_textbox = QTextEdit(self)
		self.user_textbox.resize(850, 50)
		self.user_textbox.move(150, 500)
		self.user_textbox.setText('Alice')

		self.past_msg = QTextEdit(self)
		self.past_msg.setReadOnly(True)
		self.past_msg.resize(950, 450)
		self.past_msg.move(50, 50)

		self.textEdit = QTextEdit(self)
		self.textEdit.resize(950, 250)
		self.textEdit.move(50, 550)

		self.setGeometry(300, 300, 1040, 870)
		self.setFixedHeight(870)
		self.setFixedWidth(1040)
		self.setWindowTitle('Random ChatRoom')
		self.show()


def main():
	app = QApplication(sys.argv)
	chatroom = ChatRoom({'host': 'localhost', 'port': 12347})
	sys.exit(app.exec_())


if __name__ == '__main__':
	import sys
	main()
