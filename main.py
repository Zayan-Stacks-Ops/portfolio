from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio, random, datetime

app = FastAPI(title="PSX Trader Backend - Starter")

class Order(BaseModel):
    symbol: str
    side: str
    qty: float
    price: float = None

@app.get('/health')
async def health():
    return {'status':'ok','time': datetime.datetime.utcnow().isoformat()}

@app.get('/api/sample-ticks')
async def sample_ticks():
    # return simulated recent ticks for a sample symbol
    now = datetime.datetime.utcnow()
    ticks = []
    price = 100.0
    for i in range(60):
        price += random.uniform(-0.8,0.8)
        ticks.append({'ts': (now - datetime.timedelta(seconds=60-i)).isoformat(), 'price': round(price,2)})
    return JSONResponse(content={'symbol':'SAMPLE','ticks':ticks})

@app.post('/api/place-order')
async def place_order(order: Order):
    # This is a stub: in production integrate with broker API
    trade_id = f"TR-{int(datetime.datetime.utcnow().timestamp())}-{random.randint(100,999)}"
    return {'status':'accepted','trade_id': trade_id, 'order': order.dict()}

@app.post('/api/backtest')
async def backtest(strategy: dict):
    # Very simple mock backtest: returns random performance stats
    total_trades = random.randint(10,100)
    wins = int(total_trades * random.uniform(0.45,0.7))
    losses = total_trades - wins
    pnl = round(random.uniform(-0.05, 0.25) * 100000,2)
    return {'strategy': strategy, 'trades': total_trades, 'wins': wins, 'losses': losses, 'pnl': pnl}

# WebSocket simulated feed for price ticks
@app.websocket('/ws/ticks/{symbol}')
async def ws_ticks(ws: WebSocket, symbol: str):
    await ws.accept()
    price = 100.0
    try:
        while True:
            # simulate a tick
            price += random.uniform(-0.6,0.6)
            tick = {'symbol': symbol.upper(), 'ts': datetime.datetime.utcnow().isoformat(), 'price': round(price,2)}
            await ws.send_json(tick)
            await asyncio.sleep(1.0)
    except Exception:
        await ws.close()
