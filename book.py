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
        self.publishing = publishing

    def export_info(self):
        ret = {
            'name': self.name,
            'author': self.author,
            'classify_id': self.classify_id,
            'publishing': self.publishing,
            'owner_id': self.owner_id
        }
        return ret

    def keyword_match(self, keyword):
        """match keyword in book info"""
        # return if match success in each item
        # example:
        #   [0,1,0]: name False, author True, publishing False
        ret_truth_table = [False, False, False]

        # find author
        if self.name.find(keyword) != -1:
            ret_truth_table[0] = True
        if self.author.find(keyword) != -1:
            ret_truth_table[1] = True
        if self.publishing.find(keyword) != -1:
            ret_truth_table[2] = True

        return ret_truth_table



if __name__ == '__main__':
    book = Book(1, 'test', 'authorname', 0, 'pub')
    print(book.export_info())
    print(book.keyword_match('te'))
