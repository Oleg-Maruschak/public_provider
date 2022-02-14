from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from model import Connect_db
from bitrix import Bitrix
from function import *
from provider.AVDclass import AVD
from provider.NDSAVDclass import NDSAVD
from provider.ELITclass import ELIT
from provider.UNICclass import UNIC
from service.Turbosms import Turbosms
import uvicorn


app = FastAPI()


class Product(BaseModel):
    article: str
    brand: str
    count: int
    order: Optional[str] = None


class GetModel(BaseModel):
    key: str
    provider: str
    orderNumber: Optional[str] = None
    product: List[Product]


class GetBalance(BaseModel):
    key: str
    provider: str
    login: str
    pas: str
    url: str


class GetOrder(BaseModel):
    key: str
    provider: str
    order: str


@app.post("/get_order")
async def get_order(request: GetOrder):
    dic = request.dict()
    api = dic['key']
    provider = dic['provider']
    order = dic['order']
    return get_result_order(api, order, provider)

@app.post("/balance")
async def balance(request: GetBalance):
    dic = request.dict()
    masiv = []
    provider = dic['provider']
    url = dic['url']
    pas = dic['pas']
    login = dic['login']
    try:
        con = Connect_db(dic['key'])
        val = con.select_api()
        con.closes()
    except Exception:
        return {'massege': 'Нет подключения к DB'}
    if val is not True:
        return {"massage": val}
    else:
        go = eval(provider)(str(url), pas, login, masiv, provider, False, True, True)
        ans = go.get_ansver()
        return ans['message']


@app.post("/post")
async def ps(request: GetModel):
    dic = request.dict()
    try:
        con = Connect_db(dic['key'])
        val = con.select_api()
        value = con.select_url(dic['provider'])
        provider = dic['provider']
        url = value['url']
        login = value['login']
        password = value['pass']
        cookie = value['cookie']
        send = con.select_message()
        con.closes()
    except Exception:
        return {'massege': 'Нет подключения к DB'}
    if val is not True:
        return {"massage": val}
    else:
        go = eval(provider)(str(url), password, login, cookie, dic['product'], dic['provider'], dic['key'], dic['orderNumber'], False, True)
        ans = go.get_ansver()
        for len in send['bitrix']:
            Bitrix(send['url'], len, ans)
        for len2 in send['telegram']:
            send_message_telegram(len2, ans)
        return ans


if __name__ == "__main__":
    uvicorn.run("index:app", log_level="info", host='127.0.0.1', port=8000, reload=True)
