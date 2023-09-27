import magic
class config:
    def check_mime(self):
        # debug log
        print(self)
        return magic.from_file(self)
    def secret_key():
        return "QhJg4gLABW7JY7mcnmoGOpUpO4iOlRYRU7ZrE33Gr8FWPn5f60V4c3GM2CFrws"