from fastapi import FastAPI
from fastapi.params import Body

app= FastAPI()

Books=[
    {"title":"Python","author":"Sachin","price":1000},
    {"title":"C","author":"AK","price":200},
    {"title":"C++","author":"ABhi","price":400},
    {"title":"Java","author":"Af","price":600},
    {"title":"Web","author":"Var","price":800},
]


#get
@app.get("/books")
async def read_all_books():
    return Books

@app.get("/books/{book_title}")
async def get_book(book_title:str):
    for book in Books:
        if book.get('title').lower()==book_title.lower():
            return book
    return {'response': "no book found"}

@app.get("/price/")
async def get_category_price(price:int):
    result=[]
    for book in Books:
        if book.get('price')==price:
            result.append(book)
    return result

@app.get("/books/{book_author}/")
async def get_book_author_price(book_author:str,price:int):
    result=[]
    for book in Books:
        if book.get('author').lower()==book_author.lower() and book.get('price')==price:
            result.append(book)
    return result

@app.get("/author_books/{book_author}")
async def get_book_author_price(book_author:str):
    result=[]
    for book in Books:
        if book.get('author').lower()==book_author.lower():
            result.append(book)
    return result

#post
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    Books.append(new_book)
    return "Success"
        
#put
@app.put("/books/update_book")
async def update_book(updated_body=Body()):
    for i in range(len(Books)):
        if Books[i].get('title').lower()==updated_body.get("title").lower():
            Books[i]= updated_body
    return 'success'

#delete
@app.delete("/books/delete_book/{author}")
async def delete_book(author:str):
    for i in range(len(Books)):
        print(i)
        if Books[i].get('author').lower()==author.lower():
            del Books[i]
            break
    return f'success'

