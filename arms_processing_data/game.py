class Game:
    def __init__(self,id,title,description,review,developer:list,publisher:list,category:list):
        self.id=id
        self.title=title
        self.description=description
        self.review=review
        self.developer=developer
        self.publisher=publisher
        self.category=category
    def __str__(self):
        return f"{self.id}\n {self.title}\n {self.description}\n {self.review} \n {self.developer} \n {self.publisher}\n {self.category}"
    def __repr__(self):
        return self