from fastapi import FastAPI
from upstash_redis import Redis
import random
import time

app = FastAPI()
kv = Redis(url="https://full-walrus-28914.upstash.io", token="AXDyAAIjcDE4NDE2MDYwMmI0MDc0MzQxYTEwODdiN2FmN2VkZDhhYXAxMA")
@app.get("/queue/{inp}", tags=["Root"])
async def test(inp: str):
    kv.set('p1move', 'true')
    kv.set('p2move', 'true')
    kv.set("p1score", '0')
    kv.set("p2score", '0')
    print(type(inp))
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

@app.get("/main/{spot}/{move}/{score}")
async def main(spot: str, move: str, score: str):
    possibleCards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    seed = []
    print(spot, type(spot))
    if spot == '1':
    	kv.set('p1move', move)
    	kv.set('p1score', score)
    else:
    	kv.set('p2score', score)
    	kv.set('p2move', move)

    for i in range(20):
        seed.append(possibleCards[random.randrange(0, len(possibleCards))])
    return {"p1move": seed[random.randrange(3, 10)], "p2move": seed[random.randrange(3, 10)], "p1score": kv.get("p1move")}

    
@app.get('/request')
async def request():
    return {"p1move": kv.get("p1move"), "p2move": kv.get('p2move'), "p1score": kv.get("p1score"), "p2score": kv.get("p2score")}
    
    
    
    
    
    
    
    
    
