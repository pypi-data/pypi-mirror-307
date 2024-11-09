import s21 as jj

class ServerManager:
  def __init__(self):
    self.server = None
    self.clean_on_exit = True
    self.filename = 'server1.txt'
    if os.getenv('S21_NOCLEAN') is not None and os.getenv('S21_NOCLEAN').lower() in ('false', '0', 'f', 'n', 'no'):
      self.clean_on_exit = False

  def __enter__(self):
    self.server = create_server1()
    return self.server

  def __exit__(self, exc_type, exc_value, traceback):
    if os.path.exists(self.filename) and self.clean_on_exit:
      os.remove(self.filename)

def create_server1():
  keys = os.getenv('S21_KEYS').split(',')
  filename = os.getenv('S21_FILENAME')
  trusted = os.getenv('S21_TRUSTED', 'False').lower() in ('true', '1', 't', 'y', 'yes')
  print(trusted)
  server = jj.MyServer(keys, trusted, filename)
  jj.setup_s21(server.keys, server.trusted, server.filename, dataOut=True)
  return server.get_my_srv()