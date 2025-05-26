from fastapi import FastAPI
from upstash_redis import Redis
import random
import time
from pydantic import BaseModel, ValidationError


class Base(BaseModel):
    ip: str | None
    spot: str | None
    move: str | None
    score: str | None
    

try:
    Base()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
app = FastAPI()
kv = Redis(url="https://full-walrus-28914.upstash.io", token="AXDyAAIjcDE4NDE2MDYwMmI0MDc0MzQxYTEwODdiN2FmN2VkZDhhYXAxMA")

@app.get("/queue/{inp}", tags=["Root"])
async def test(inp: str):
    try:
        if inp not in kv.get("ip"):
            kv.set("ip", kv.get("ip") + ', ' + inp )
    except:
        kv.set("ip", inp)
        kv.set("started", False)
    return {"players": len((kv.get("ip")).split(",")), "started": kv.get("started"), "ips": kv.get("ip")}

@app.get("/players/")
async def players():
   return {"players": len((kv.get("ip")).split(",")), "ips": kv.get("ip")}

@app.get("/clear/")
async def clear():
    kv.delete('ip')
    kv.delete("started")
    

@app.get("/start/")
async def start():
    kv.set("started", True)
    string = ""
    for i in range(len((kv.get("ip")).split(","))):
    	string += "blank, "
    kv.set("move", string)
    kv.set("score", string)

@app.post("/main/")
async def main(base: Base):
    possibleCards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    seed = []
    if base.ip not in kv.get("ip"):
    	return {None}
    scores = kv.get("score").split(", ")
    moves = kv.get("move").split(", ")
    moves[int(base.spot)] = base.move
    scores[int(base.spot)] = base.score
    kv.set("move", ', '.join(map(str, moves)))
    kv.set("score", ', '.join(map(str, scores)))
    for i in range(20):
        seed.append(possibleCards[random.randrange(0, len(possibleCards))])
    return {"move": seed[random.randrange(3, 10)]}

    
@app.get('/request/')
async def request():
    return {"moves": kv.get("move"), "scores": kv.get("score")}
    
    
    
    
    
    
    
