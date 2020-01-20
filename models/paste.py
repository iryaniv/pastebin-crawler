
class Paste:
    def __init__(self, paste_id, name, user, date, content):
        self.id = paste_id
        self.name = name
        self.user = user
        self.date = date
        self.content = content

    def __str__(self):
        return "{} - {} - by {} at {} \n {}".format(self.id, self.name, self.user, self.date, self.content)
