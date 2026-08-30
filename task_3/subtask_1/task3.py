from abc import ABC,abstractmethod
from enum import Enum

class ItemStatus(Enum):
    AVAILABLE='AVAILABLE'
    CHECKED_OUT='CHECKED_OUT'
    LOST='LOST'


class LibraryItem(ABC):

    def __init__(self,title,status=ItemStatus.AVAILABLE):
        self.title=title
        self._status=status

    _registry={}

    @abstractmethod
    def get_loan_period(self):
        pass

    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError(f'Can\'t check out {self.title}, currently {self._status}')
        else:
            self._status=ItemStatus.CHECKED_OUT

    def return_item(self):

        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError(f'Can\'t return {self.title}, not checked out.')
        else:
            self._status = ItemStatus.AVAILABLE

    def mark_lost(self):
        if self._status != ItemStatus.LOST:
            self._status=ItemStatus.LOST
        else:
            raise ValueError('Can\'t mark an already lost item')

    @property
    def status(self):
        return self._status

    def __lt__(self, other):

        return self.title.lower() < other.title.lower()

    def __repr__(self):
        return f"{type(self).__name__}(title={self.title!r}, status={self._status})"
    
    def __str__(self):
        return f"{self.title} ({type(self).__name__}) — {self._status.value.title()}"

    
    def __init_subclass__(cls, type_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if type_name:
            LibraryItem._registry[type_name] = cls

    @classmethod
    def from_dict(cls, data):
        item_cls = LibraryItem._registry[data["type"]]
        return item_cls._build(data)

class Book(LibraryItem,type_name='Book'):

    def __init__(self,title,author,isbn,status=ItemStatus.AVAILABLE):
        super().__init__(title,status)
        self.loan_period=21
        self.author=author
        self.isbn=isbn

    def get_loan_period(self):
        return self.loan_period

    @classmethod
    def _build(cls,data):
        return cls(title=data['title'],author=data['author'],isbn=data['isbn'],status=ItemStatus(data['status']))

    @staticmethod
    def validate_isbn(isbn): ##ISBN 13 is used
        sum_isbn=0
        if not isbn.isdigit() or len(isbn) != 13:
            return False
                    

        for i in range(len(isbn)):

           
            if (i+1)%2==0:
                sum_isbn+= int(isbn[i])*3
            else:
                sum_isbn+=int(isbn[i])*1


        if sum_isbn%10==0:
            return True
        else: 
            return False

    def to_dict(self):
        return {
            'type':'Book',
            'title': self.title,
            'status':self._status.value,
            'isbn':self.isbn,
            'author':self.author

        }


class DVD(LibraryItem,type_name='DVD'):

    def __init__(self,title,director,status=ItemStatus.AVAILABLE):
        super().__init__(title,status)
        self.loan_period=5
        self.director=director

    def get_loan_period(self):
        return self.loan_period

    @classmethod
    def _build(cls,data):
        return cls(title=data['title'],director=data['director'],status=ItemStatus(data['status']))

    def to_dict(self):
        return{
            'type':'DVD',
            'title':self.title,
            'director':self.director,
            'status':self._status.value
        }

class Magazine(LibraryItem,type_name='Magazine'):

    def __init__(self,title,issue,status=ItemStatus.AVAILABLE):
        super().__init__(title,status)
        self.loan_period=14
        self.issue=issue

    def get_loan_period(self):
        return self.loan_period

    @classmethod

    def _build(cls,data):
        return cls(title=data['title'],issue=data['issue'],status=ItemStatus(data['status']))


    def to_dict(self):

        return{
            'type':'Magazine',
            'title':self.title,
            'issue':self.issue,
            'status':self._status.value
        }

class Database():

    def save_file(self,items:LibraryItem):

        with open('Database.txt','w') as f:

            for item in items:
                d=item.to_dict()
                if d['type']=='Book':
                    line = f"type={d['type']}|title={d['title']}|author={d['author']}|isbn={d['isbn']}|status={d['status']}"
                elif d['type']=='DVD':
                    line = f'type={d['type']}|title={d['title']}|director={d['director']}|status={d['status']}'
                elif d['type'] == 'Magazine':
                    line=f'type={d['type']}|title={d['title']}|issue={d['issue']}|status={d['status']}'

                f.write(line+'\n')
                

    def load_file(self):

        try:
            with open('Database.txt','r') as f:
                items=[]

                for line in f:

                    line=line.strip()

                    if not line:
                        continue

                    fields=line.split('|')
                    data=dict(field.split('=',1) for field in fields)
                    items.append(LibraryItem.from_dict(data))
        except FileNotFoundError:
            items=[]

        return items


class Library:
    def __init__(self, database):
        self._database = database
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def find_by_title(self, title):
        for item in self._items:
            if item.title == title:
                return item
        return None

    def checkout(self, title):
        item = self.find_by_title(title)
        if item is None:
            raise ValueError(f"No item titled {title!r}")
        item.checkout()

    def return_item(self, title):
        item = self.find_by_title(title)
        if item is None:
            raise ValueError(f"No item titled {title!r}")
        item.return_item()

    def list_available(self):
        return [item for item in self._items if item.status == ItemStatus.AVAILABLE]

    def load(self):
        self._items = self._database.load_file()

    def save(self):
        self._database.save_file(self._items)