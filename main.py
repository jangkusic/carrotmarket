from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3


con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()


# cur.execute(f"""
#     CREATE TABLE IF NOT EXISTS items (
# 	    id INTEGER PRIMARY KEY,
# 	    title TEXT NOT NULL,
# 	    image BLOB,
# 	    price INTEGER NOT NULL,
# 	    description TEXT,
# 	    place TEXT NOT NULL,
# 	    insertAt INTEGER NOT NULL
# );

#             """)

app = FastAPI()

# secret은 access token을 어떻게 encoding할지 정하는 것.
SECRET = "super-coding"
manager = LoginManager(SECRET, '/login')

@manager.user_loader()
# db에 해당 유저가 존재하는지 확인
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type (data) == dict:
        WHERE_STATEMENTS = f'''id="{data['name']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                        SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()],
           password:Annotated[str, Form()]):
    user = query_user(id) 
    # 존재하지 않는 유저이거나 패스워드가 다를경우 에러 보내기   
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    # access token 만들기
    access_token = manager.create_access_token(data={
        'sub': {
            'id' : user['id'],
            'name' : user['name'],
            'email' : user['email']            
        }
    })
    return {'access_token':access_token}

@app.post("/signup")
def signup(id:Annotated[str, Form()],
           password:Annotated[str, Form()],
           name:Annotated[str, Form()],
           email:Annotated[str, Form()]):
    # db에 저장하기
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    # db에 들어가는지 확인하기
    con.commit()
    return '200'

@app.post("/items")
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()], 
                insertAt:Annotated[int, Form()]
                ):
    
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items (title,image,price,description,place,insertAt)
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}',{insertAt})
                """)
    con.commit()
    return '200'

@app.get('/items')
# user=Depends는 유저가 인증된 상태에서만 응답이 보내질 수 있도록 하는 것.
async def get_items(user=Depends(manager)):
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    # 현재의 위치를 업데이트
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                    """).fetchall()
    # dict()는 객체형태로 바꿔주는 문법
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get('/images/{items_id}')
async def get_image(items_id):
    cur = con.cursor() 
    image_bytes = cur.execute(f"""
                              SELECT image FROM items
                              WHERE id={items_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes))



app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

