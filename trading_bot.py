from datetime import datetime

import alpaca_trade_api as tradeapi
import pandas as pd
import time



API_KEY = "YOUR OWN API"
SECRET_KEY = "YOUR KEY"
BASE_URL = "https://paper-api.alpaca.markets"



api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')


# # TEST BUY – runs once
# api.submit_order(
#     symbol="AAPL",
#     qty=22,
#     side="buy",
#     type="market",
#     time_in_force="gtc"
# )
#
# print("Test order sent")




def market_open():
    clock = api.get_clock()
    return clock.is_open

def get_signal(symbol):
    bars = api.get_bars(
        symbol,
        tradeapi.TimeFrame.Minute,
        limit=100,
        feed="iex"
    ).df

    if bars.empty or len(bars) < 50:
        return "WAIT"

    bars["SMA_fast"] = bars["close"].rolling(20).mean()
    bars["SMA_slow"] = bars["close"].rolling(50).mean()

    bars = bars.dropna()
    if len(bars) < 2:
        return "WAIT"

    prev = bars.iloc[-2]
    last = bars.iloc[-1]

    print(
        f"{symbol} | {last.name} | "
        f"Price: {last.close:.2f} | "
        f"Fast: {last.SMA_fast:.2f} | "
        f"Slow: {last.SMA_slow:.2f}"
    )

    if prev.SMA_fast < prev.SMA_slow and last.SMA_fast > last.SMA_slow:
        return "BUY"
    if prev.SMA_fast > prev.SMA_slow and last.SMA_fast < last.SMA_slow:
        return "SELL"

    return "HOLD"

def trade_logic(symbol, signal):
    try:
        position = api.get_position(symbol)
        qty_owned = int(position.qty)
    except:
        qty_owned = 0

    if signal == "BUY" and qty_owned == 0:
        api.submit_order(
            symbol=symbol,
            qty=1,
            side="buy",
            type="market",
            time_in_force="gtc"
        )
        print(f"ORDER FILLED: BUY {symbol}")

    elif signal == "SELL" and qty_owned > 0:
        api.submit_order(
            symbol=symbol,
            qty=qty_owned,
            side="sell",
            type="market",
            time_in_force="gtc"
        )
        print(f"ORDER FILLED: SELL {symbol}")

print("Bot running for AAPL")

last_minute = None

while True:
    if not market_open():
        print("Market closed")
        time.sleep(300)
        continue

    current_minute = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    if current_minute != last_minute:
        signal = get_signal("AAPL")
        trade_logic("AAPL", signal)
        last_minute = current_minute

    time.sleep(5)





# if __name__ == "__main__":
#     check_account()
#     main()



























































# def get_signal(symbol):
#     try:
#         bars = api.get_bars(symbol, tradeapi.TimeFrame.Minute, limit=100, feed='iex').df
#         if bars.empty:
#             print(f"[{symbol}] No data found. Market might be closed.")
#             return "WAITING"
#
#         bars['SMA_fast'] = bars['close'].rolling(window=20).mean()
#         bars['SMA_slow'] = bars['close'].rolling(window=50).mean()
#
#         last_row = bars.iloc[-1]
#         prev_row = bars.iloc[-2]
#
#         print(
#             f"{symbol} | Price: ${last_row['close']:.2f} | Fast: {last_row['SMA_fast']:.2f} | Slow: {last_row['SMA_slow']:.2f}")
#
#         if prev_row['SMA_fast'] < prev_row['SMA_slow'] and last_row['SMA_fast'] > last_row['SMA_slow']:
#             return "BUY"
#         elif prev_row['SMA_fast'] > prev_row['SMA_slow'] and last_row['SMA_fast'] < last_row['SMA_slow']:
#             return "SELL"
#         return "HOLD"
#     except Exception as e:
#         print(f"Signal Error: {e}")
#         return "ERROR"
#
#
# def trade_logic(symbol, signal):
#     try:
#         # Check current position
#         try:
#             position = api.get_position(symbol)
#             qty_owned = int(position.qty)
#         except:
#             qty_owned = 0
#
#         if signal == "BUY" and qty_owned == 0:
#             print(f">>> {symbol} SIGNAL: BUY. Executing market order...")
#             api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='gtc')
#
#         elif signal == "SELL" and qty_owned > 0:
#             print(f">>> {symbol} SIGNAL: SELL. Closing position...")
#             api.submit_order(symbol=symbol, qty=qty_owned, side='sell', type='market', time_in_force='gtc')
#
#     except Exception as e:
#         print(f"Execution Error: {e}")
#
#
# # --- MAIN LOOP ---
# print("Stock Bot Active. Trading AAPL...")
# while True:
#     stock_symbol = "AAPL"
#     current_signal = get_signal(stock_symbol)
#     trade_logic(stock_symbol, current_signal)
#     time.sleep(60)


# Example usage:
# signal = get_signal("AAPL")
# print(f"Current Signal for AAPL: {signal}")







