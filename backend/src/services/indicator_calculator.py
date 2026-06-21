"""Technical Indicator Calculator"""
from typing import List, Dict, Optional
from decimal import Decimal
import numpy as np


class IndicatorCalculator:
    """Calculate technical indicators"""
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average
        
        Args:
            prices: List of prices in ascending order (oldest first)
            period: EMA period
        
        Returns:
            EMA value or None if not enough data
        """
        if len(prices) < period:
            return None
        
        prices = np.array(prices, dtype=float)
        ema = prices[-period:].mean()  # Start with SMA
        
        multiplier = 2 / (period + 1)
        
        # Calculate EMA from period point onwards
        for i in range(len(prices) - period + 1, len(prices)):
            ema = (prices[i] - ema) * multiplier + ema
        
        return round(float(ema), 4)
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index
        
        Args:
            prices: List of prices in ascending order
            period: RSI period
        
        Returns:
            RSI value (0-100) or None if not enough data
        """
        if len(prices) < period + 1:
            return None
        
        prices = np.array(prices, dtype=float)
        deltas = np.diff(prices)
        
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        
        # Smooth remaining values
        for d in deltas[period+1:]:
            if d > 0:
                up = (up * (period - 1) + d) / period
                down = down * (period - 1) / period
            else:
                up = up * (period - 1) / period
                down = (down * (period - 1) - d) / period
            
            rs = up / down if down != 0 else 0
            rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    @staticmethod
    def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[Dict[str, float]]:
        """Calculate MACD indicator
        
        Args:
            prices: List of prices in ascending order
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        
        Returns:
            Dict with macd, signal, histogram or None if not enough data
        """
        if len(prices) < slow:
            return None
        
        ema_fast = IndicatorCalculator.calculate_ema(prices, fast)
        ema_slow = IndicatorCalculator.calculate_ema(prices, slow)
        
        if ema_fast is None or ema_slow is None:
            return None
        
        macd = ema_fast - ema_slow
        
        # For signal line, we'd need all MACD values
        # Simplified: use current MACD as estimate
        signal_line = macd  # Placeholder
        histogram = macd - signal_line
        
        return {
            'macd': round(macd, 4),
            'signal': round(signal_line, 4),
            'histogram': round(histogram, 4)
        }
    
    @staticmethod
    def calculate_atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> Optional[float]:
        """Calculate Average True Range
        
        Args:
            high: List of highs
            low: List of lows
            close: List of closes
            period: ATR period
        
        Returns:
            ATR value or None if not enough data
        """
        if len(high) < period or len(low) < period or len(close) < period:
            return None
        
        high = np.array(high, dtype=float)
        low = np.array(low, dtype=float)
        close = np.array(close, dtype=float)
        
        tr1 = high - low
        tr2 = np.abs(high - np.roll(close, 1))
        tr3 = np.abs(low - np.roll(close, 1))
        
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        atr = np.mean(tr[-period:])
        
        return round(float(atr), 4)
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2) -> Optional[Dict[str, float]]:
        """Calculate Bollinger Bands
        
        Args:
            prices: List of prices
            period: Moving average period
            std_dev: Number of standard deviations
        
        Returns:
            Dict with upper, middle, lower bands or None
        """
        if len(prices) < period:
            return None
        
        prices = np.array(prices[-period:], dtype=float)
        middle = np.mean(prices)
        std = np.std(prices)
        
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return {
            'upper': round(upper, 4),
            'middle': round(middle, 4),
            'lower': round(lower, 4)
        }
    
    @staticmethod
    def calculate_relative_volume(volume: float, avg_volume_20: float) -> Optional[float]:
        """Calculate relative volume
        
        Args:
            volume: Current day volume
            avg_volume_20: Average volume last 20 days
        
        Returns:
            Relative volume ratio
        """
        if avg_volume_20 == 0:
            return None
        
        return round(volume / avg_volume_20, 2)
