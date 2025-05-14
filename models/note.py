from datetime import datetime

class Note:
    def __init__(self, title, content, created_at=None):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at
        }
        
    @staticmethod
    def from_dict(data):
        return Note (
            title = data["title"],
            content = data["content"],
            created_at = data["created_at"]
        )
