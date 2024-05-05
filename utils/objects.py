

class Track:
    def __init__(self, title: str, performer: str, filepath: str, duration: str = None, description: str = None):
        self.title = title
        self.duration = duration
        self.performer = performer
        self.description = description
        self.filepath = filepath
