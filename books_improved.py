from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

#created object
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title= title
        self.author= author
        self.description= description
        self.rating = rating
        self.published_date= published_date

# for validation via Pydantic
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length= 1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int= Field(gt=1990)

    class Config:
        json_schema_extra = {
            'example':{
                'title': 'A new book',
                'author': 'codingwiththroby',
                'description': 'This is a new book',
                'rating': 5,
                'published_date': 1991
            }
        }
    

Books =[
    Book(1,"The Great Gatsby","F. Scott Fitzgerald","A novel about the American Dream","4", 1992),
    Book(2,"To Kill a Mockingbird","Harper Lee","A novel about racism and injustice","5", 1993),
    Book(3,"1984","George Orwell","A dystopian novel about totalitarianism","4", 2012),
    Book(4,"The Catcher in the Rye","J.D. Salinger","A novel about teenage angst","3", 2003),
    Book(5,"The Hitchhiker's Guide to the Galaxy","Douglas Adams","A science fiction novel about the meaning of life","4",1992)
]

#get
@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books

@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='No book found')
        
@app.get('/books/',status_code=status.HTTP_200_OK)
def get_by_rating(rating:str = Query(gt='0', lt='6')):
    result=[]
    for book in Books:
        if book.rating == rating:
            result.append(book)
    return result

@app.get('/books/published/{year}',status_code=status.HTTP_200_OK)
def get_by_published_date(year:int = Path(gt=1990)):
    result=[]
    for book in Books:
        if book.published_date== year:
            result.append(book)
    return result

# post
# here if you look closely we used book_request: BookRequest not book_request= Body() coz when we get body it directly passed to this BookRequest
# via pydantic aslso provides request body example
@app.post('/create_book',status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    Books.append(find_book_id(new_book))

#put
@app.put("/books/update", status_code= status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed= False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i]=book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found')

#delete
@app.delete('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int = Path(gt=0)):
    book_deleted= False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_deleted= True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Book not found')


def find_book_id(book:Book):
    book.id=1 if len(Books)==0 else Books[-1].id + 1
    # if len(Books)>0:
    #     book.id = Books[-1].id + 1
    # else:
    #     book.id = 1
    return book





