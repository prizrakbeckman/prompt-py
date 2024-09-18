from datetime import datetime
from typing import List, Optional

class Movie:
    def __init__(self, _id: int, title: str, isbn: str, page_count: int, published_date: datetime,
                 thumbnail_url: str, short_description: str, long_description: str, status: str,
                 authors: List[str], categories: List[str]):
        self._id = _id
        self.title = title
        self.isbn = isbn
        self.page_count = page_count
        self.published_date = published_date
        self.thumbnail_url = thumbnail_url
        self.short_description = short_description
        self.long_description = long_description
        self.status = status
        self.authors = authors
        self.categories = categories

    @classmethod
    def from_dict(cls, data: dict):
        published_date = datetime.strptime(data['publishedDate']['$date'], "%Y-%m-%dT%H:%M:%S.%f%z")
        return cls(
            _id=data['_id'],
            title=data['title'],
            isbn=data['isbn'],
            page_count=data['pageCount'],
            published_date=published_date,
            thumbnail_url=data['thumbnailUrl'],
            short_description=data['shortDescription'],
            long_description=data['longDescription'],
            status=data['status'],
            authors=data['authors'],
            categories=data['categories']
        )

    def to_dict(self):
        return {
            "_id": self._id,
            "title": self.title,
            "isbn": self.isbn,
            "pageCount": self.page_count,
            "publishedDate": {"$date": self.published_date.isoformat()},
            "thumbnailUrl": self.thumbnail_url,
            "shortDescription": self.short_description,
            "longDescription": self.long_description,
            "status": self.status,
            "authors": self.authors,
            "categories": self.categories
        }