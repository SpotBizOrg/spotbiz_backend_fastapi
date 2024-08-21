# models.py
from schemas import CategoryKeywordsModel

class CategoryKeywords:
    def __init__(self, data: CategoryKeywordsModel):
        self.data = data.dict()

    def get_keywords(self, category: str):
        return self.data.get(category, [])

    def add_keyword(self, category: str, keyword: str):
        if category in self.data:
            self.data[category].append(keyword)
        else:
            self.data[category] = [keyword]

    def remove_keyword(self, category: str, keyword: str):
        if category in self.data and keyword in self.data[category]:
            self.data[category].remove(keyword)
