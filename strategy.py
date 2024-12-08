class Strategy:
    def check_reversal_signals(self, candles):
        if len(candles) < 3:
            return None

        first, second, third = candles[-3], candles[-2], candles[-1]

        # Bearish Reversal (Short Signal)
        if (first["close"] > first["open"] and second["close"] < second["open"]
                and second["high"] - second["low"] > 2 * abs(second["open"] - second["close"])
                and third["close"] < second["low"]):
            return "SHORT"

        # Bullish Reversal (Long Signal)
        if (first["close"] < first["open"] and second["close"] > second["open"]
                and second["high"] - second["low"] > 2 * abs(second["open"] - second["close"])
                and third["close"] > second["high"]):
            return "LONG"

        return None
