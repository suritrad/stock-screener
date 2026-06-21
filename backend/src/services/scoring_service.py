"""AI Scoring Service for calculating stock scores"""
from typing import Dict, Optional, Tuple
from decimal import Decimal
from .config_service import ConfigService


class ScoringService:
    """Service for calculating AI scores based on indicators"""
    
    def __init__(self, config_service: ConfigService):
        """Initialize scoring service
        
        Args:
            config_service: ConfigService instance
        """
        self.config = config_service
    
    def calculate_score(self, indicator_data: Dict, market_regime: str = None) -> Tuple[float, Dict[str, float]]:
        """Calculate overall AI score for a stock
        
        Args:
            indicator_data: Dict containing indicator values
            market_regime: Market regime (bull/sideway/bear). If None, uses config default
        
        Returns:
            Tuple of (total_score, score_breakdown)
        """
        if market_regime is None:
            market_regime = self.config.get_market_regime()
        
        # Get adjusted weights based on market regime
        weights = self.config.get_adjusted_weights(market_regime)
        
        # Calculate individual indicator scores
        scores = {
            'ema_alignment': self._score_ema_alignment(indicator_data),
            'rsi': self._score_rsi(indicator_data),
            'macd': self._score_macd(indicator_data),
            'relative_volume': self._score_relative_volume(indicator_data),
            'breakout': self._score_breakout(indicator_data),
            'adx': self._score_adx(indicator_data),
            'market_cap': self._score_market_cap(indicator_data),
            'risk_reward': self._score_risk_reward(indicator_data)
        }
        
        # Calculate weighted score
        total_score = sum(scores[k] * weights[k] / 100 for k in scores.keys())
        
        # Round to 2 decimal places
        total_score = round(total_score, 2)
        
        return total_score, scores
    
    def _score_ema_alignment(self, data: Dict) -> float:
        """Score EMA alignment (Price > EMA5 > EMA10 > EMA25)
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-20
        """
        max_score = 20
        price = float(data.get('close_price', 0))
        ema5 = float(data.get('ema5', 0))
        ema10 = float(data.get('ema10', 0))
        ema25 = float(data.get('ema25', 0))
        
        conditions_met = 0
        total_conditions = 3
        
        if price > ema5:
            conditions_met += 1
        if ema5 > ema10:
            conditions_met += 1
        if ema10 > ema25:
            conditions_met += 1
        
        # Award score proportionally
        score = (conditions_met / total_conditions) * max_score
        return round(score, 2)
    
    def _score_rsi(self, data: Dict) -> float:
        """Score RSI indicator
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-15
        """
        rsi = float(data.get('rsi14', 0))
        
        if 55 <= rsi <= 70:
            return 15.0
        elif 50 <= rsi < 55:
            return 8.0
        elif 70 < rsi <= 75:
            return 5.0
        else:
            return 0.0
    
    def _score_macd(self, data: Dict) -> float:
        """Score MACD indicator
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-15
        """
        macd = float(data.get('macd', 0))
        signal = float(data.get('macd_signal', 0))
        
        # Check if MACD > Signal and MACD > 0
        if macd > signal and macd > 0:
            return 15.0
        else:
            return 0.0
    
    def _score_relative_volume(self, data: Dict) -> float:
        """Score relative volume
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-20
        """
        rvol = float(data.get('relative_volume', 0))
        
        if rvol >= 2.0:
            return 20.0
        elif 1.5 <= rvol < 2.0:
            return 15.0
        elif 1.2 <= rvol < 1.5:
            return 10.0
        else:
            return 0.0
    
    def _score_breakout(self, data: Dict) -> float:
        """Score breakout condition
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-10
        """
        close = float(data.get('close_price', 0))
        high_20 = float(data.get('high_20', 0))
        volume = float(data.get('volume', 0))
        avg_volume_20 = float(data.get('avg_volume_20', 0))
        
        # Check breakout condition
        if close > high_20 and volume > avg_volume_20:
            return 10.0
        else:
            return 0.0
    
    def _score_adx(self, data: Dict) -> float:
        """Score ADX (trend strength)
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-10
        """
        adx = float(data.get('adx', 0))
        
        if adx >= 25:
            return 10.0
        elif 20 <= adx < 25:
            return 5.0
        else:
            return 0.0
    
    def _score_market_cap(self, data: Dict) -> float:
        """Score market cap
        
        Args:
            data: Indicator data dict (should include market_cap in baht)
        
        Returns:
            Score 0-5
        """
        market_cap = float(data.get('market_cap', 0))
        
        # Convert to millions
        market_cap_m = market_cap / 1_000_000
        
        if market_cap_m >= 5000:
            return 5.0
        elif 3000 <= market_cap_m < 5000:
            return 3.0
        else:
            return 0.0
    
    def _score_risk_reward(self, data: Dict) -> float:
        """Score risk/reward ratio
        
        Args:
            data: Indicator data dict
        
        Returns:
            Score 0-5
        """
        # This would need support/resistance/target calculations
        # Placeholder implementation
        ratio = float(data.get('risk_reward_ratio', 0))
        
        if ratio >= 1.5:
            return 5.0
        elif ratio >= 1.2:
            return 3.0
        else:
            return 0.0
