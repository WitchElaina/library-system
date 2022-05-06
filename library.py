import json

import book

file_dir = './'


class Library(object):
    books = []
    book_id = -1

    def __init__(self):
        """init library.json file"""
        pass

    def book_id_gen(self):
        """gen book id start from 0"""
        self.book_id += 1
        return self.book_id

    def add_book(self, name, author, classify_id, publishing):
        """create a new book and add to library"""
        new_book = book.Book(self.book_id_gen(), name, author, classify_id, publishing)
        self.books.append(new_book)
        self.save()

    def del_book(self, ID):
        """delete a book in library by ID"""
        for i in self.books:
            if i.ID == ID:
                self.books.remove(i)
                return True
        return False

    def id_search(self, ID):
        """search book by """
        for i in self.books:
            if i.ID == ID:
                return i.ID
        return []

    def keyword_search(self, keyword, attribute):
        """search book by keyword"""
        ret = []  # result id list
        for i in self.books:
            if i.keyword_match(keyword)[attribute]:
                ret.append(i.ID)
        return ret

    def filter(self, filter_index):
        """filter book by class"""
        ret = []
        for i in self.books:
            if i.classify_id == filter_index:
                ret.append(i.ID)
        return ret

    def save(self):
        """save current data to json file"""
        # gen data dictionary
        data_dict = {'id_gen': self.book_id, 'data':{}}
        for i in self.books:
            data_dict['data'][i.ID] = i.export_info()

        # write to json
        data_json = json.dumps(data_dict)
        with open(file_dir + 'library.json', 'w+') as data_f:
            data_f.write(data_json)

    def load(self):
        """load data from library.json"""
        with open(file_dir + 'library.json', 'r') as data_f:
            data_dict = json.loads(data_f.read())
        self.book_id = data_dict['id_gen']
        data = data_dict['data']
        for key_id in data:
            new_book = book.Book(key_id, data[key_id]['name'], data[key_id]['author'], data[key_id]['classify_id'], data[key_id]['publishing'])
            self.books.append(new_book)


if __name__ == '__main__':
    libr = Library()
    libr.load()
    # print(libr.keyword_search('t1', 0))
    # print(libr.keyword_search('ms', 1))
    # print(libr.keyword_search('pub', 2))
    # print(libr.keyword_search('pub', 2))
    # print(libr.keyword_search('t', 0))
    print(libr.filter(0))
