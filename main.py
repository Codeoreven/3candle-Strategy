import threading
from rich.console import Console
from websocket_client import WebSocketClient
from candle_manager import CandleManager
from strategy import Strategy
from trade_simulator import TradeSimulator

console = Console()

def main():
    # Prompt for access token
    access_token = console.input("[bold green]Enter your Fyers access token: [/bold green]")

    # Initialize components
    candle_manager = CandleManager()
    strategy = Strategy()
    trade_simulator = TradeSimulator(console)
    websocket_client = WebSocketClient(access_token, candle_manager, console)

    # WebSocket Thread
    def websocket_thread():
        websocket_client.connect()

    # Strategy Thread
    def strategy_thread():
        while True:
            candles = candle_manager.get_candles()
            signal = strategy.check_reversal_signals(candles)
            if signal:
                trade_simulator.execute_trade(signal, candles[-2])

    # PnL Thread
    def pnl_thread():
        while True:
            trade_simulator.check_pnl()

    # Start Threads
    console.log("[cyan]Starting WebSocket, Strategy, and PnL threads...[/cyan]")
    threading.Thread(target=websocket_thread, daemon=True).start()
    threading.Thread(target=strategy_thread, daemon=True).start()
    threading.Thread(target=pnl_thread, daemon=True).start()

    # Keep the main thread running
    while True:
        pass

if __name__ == "__main__":
    main()
