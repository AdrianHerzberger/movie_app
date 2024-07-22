from  abc import ABC, abstractclassmethod

class IStorage(ABC):
    @abstractclassmethod
    def list_movie(self):
        pass
    
    @abstractclassmethod
    def save_movie(self):
        pass
    
    @abstractclassmethod
    def add_movie(self, title, year, rating, poster):
        pass
    
    @abstractclassmethod
    def delete_movie(self, title):
        pass

    @abstractclassmethod
    def update_movie(self, title, rating):
        pass
    