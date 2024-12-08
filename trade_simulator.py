import time

class TradeSimulator:
    def __init__(self, console):
        self.console = console
        self.positions = []
        self.closed_trades = []
        self.balance = 0

    def execute_trade(self, signal, second_candle):
        entry_price = second_candle["close"]
        sl = second_candle["low"] - 5 if signal == "LONG" else second_candle["high"] + 5
        target = entry_price + (entry_price - sl) * 2 if signal == "LONG" else entry_price - (sl - entry_price) * 2

        position = {
            "signal": signal,
            "entry_price": entry_price,
            "sl": sl,
            "target": target,
            "quantity": 15,
            "open_time": second_candle["time"],
            "open": True,
        }
        self.positions.append(position)
        self.console.log(f"[blue]Opened {signal} trade:[/blue] {position}")
        self.log_trade(position, "OPEN")

    def check_pnl(self):
        for position in self.positions:
            if not position["open"]:
                continue

            # Simulate the current market price (LTP)
            ltp = self.get_mock_ltp(position)

            # Check for stop-loss or target hit
            if position["signal"] == "LONG":
                if ltp >= position["target"]:
                    self.close_trade(position, "TARGET HIT", ltp)
                elif ltp <= position["sl"]:
                    self.close_trade(position, "STOP LOSS HIT", ltp)
            elif position["signal"] == "SHORT":
                if ltp <= position["target"]:
                    self.close_trade(position, "TARGET HIT", ltp)
                elif ltp >= position["sl"]:
                    self.close_trade(position, "STOP LOSS HIT", ltp)

            time.sleep(1)  # To avoid excessive looping

    def close_trade(self, position, reason, ltp):
        position["close_price"] = ltp
        position["close_time"] = time.time()
        position["pnl"] = (
            (ltp - position["entry_price"]) * position["quantity"]
            if position["signal"] == "LONG"
            else (position["entry_price"] - ltp) * position["quantity"]
        )
        position["reason"] = reason
        position["open"] = False
        self.closed_trades.append(position)
        self.balance += position["pnl"]
        self.console.log(f"[green]Closed trade:[/green] {position}")
        self.log_trade(position, "CLOSE")

    def log_trade(self, trade, action):
        with open("trades.log", "a") as log_file:
            log_file.write(f"{action}: {trade}\n")

    def get_mock_ltp(self, position):
        """
        Simulate the LTP movement for paper trading.
        This is a simple approximation and can be replaced with real data.
        """
        if position["signal"] == "LONG":
            return position["entry_price"] + 5  # Increment for mock LTP
        elif position["signal"] == "SHORT":
            return position["entry_price"] - 5  # Decrement for mock LTP
