class Video:
    def __init__(self, file_path, title, tags, description):
        self.file_path = file_path
        self.title = title
        self.tags = tags
        self.description = description

    def to_dict(self):
        return {
            'file_path': self.file_path,
            'title': self.title,
            'tags': self.tags,
            'description': self.description
        }

    @staticmethod
    def from_dict(data):
        return Video(data['file_path'], data['title'], data['tags'], data['description'])
