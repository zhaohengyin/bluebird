from bluebird import FunctionServer, FunctionHandler
import datetime

class ChatRoomFunctionHandler(FunctionHandler):
       def __init__(self):
               super(ChatRoomFunctionHandler, self).__init__()
               self.past_text = []

       def init_class_function(self):
               self.add_class_func('add_msg', self.add_msg)
               self.add_class_func('get_history', self.get_history)

       def add_msg(self, user, text):
               time_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
               self.past_text.append((user, time_string, text))

       def get_history(self, n=5):
               return self.past_text


if __name__ == '__main__':
       server = FunctionServer(host = 'localhost', port = 12347)
       server.function_handler = ChatRoomFunctionHandler()
       server.run()