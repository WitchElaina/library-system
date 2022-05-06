"""
book
"""
classify_dict = {
    0: 'Undefined'
}

class Book(object):
    ID = 0
    name = ''
    author = ''
    classify_id = 0
    publishing = ''
    owner_id = 0

    def __init__(self, ID, name, author, classify_id, publishing):
        self.ID = ID
        self.name = name
        self.author = author
        self.classify_id = classify_id

    def export_info(self):
        ret = {
            'ID':self.ID,
            'name': self.name,
            'author': self.author,
            'classify_id': self.classify_id,
            'publishing': self.publishing,
            'owner_id': self.owner_id
        }
        return ret

if __name__ == '__main__':
    book = Book(1, 'test', 'authorname', 0, 'pub')
    print(book.export_info())
