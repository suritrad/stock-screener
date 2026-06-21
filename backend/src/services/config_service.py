"""Configuration Service for managing system settings and scoring weights"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from decimal import Decimal


class ConfigService:
    """Service for managing configuration and system settings"""
    
    def __init__(self, config_path: str = None):
        """Initialize config service
        
        Args:
            config_path: Path to scoring_config.json file
        """
        self.config_path = config_path or Path(__file__).parent / 'scoring_config.json'
        self.config = self._load_config()
        self.db_settings = {}
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {self.config_path}")
    
    def reload_config(self):
        """Reload configuration from file"""
        self.config = self._load_config()
    
    def get_default_weights(self) -> Dict[str, float]:
        """Get default scoring weights"""
        return self.config['scoring']['default_weights']
    
    def get_market_regime_weights(self, market_regime: str) -> Dict[str, float]:
        """Get weight multipliers for a specific market regime
        
        Args:
            market_regime: 'bull', 'sideway', or 'bear'
        
        Returns:
            Dict of weight multipliers
        """
        regimes = self.config['scoring']['market_regimes']
        if market_regime not in regimes:
            raise ValueError(f"Unknown market regime: {market_regime}")
        
        return regimes[market_regime]['weight_multipliers']
    
    def get_adjusted_weights(self, market_regime: str) -> Dict[str, float]:
        """Get adjusted weights based on market regime
        
        Args:
            market_regime: 'bull', 'sideway', or 'bear'
        
        Returns:
            Dict of adjusted weights
        """
        default_weights = self.get_default_weights()
        multipliers = self.get_market_regime_weights(market_regime)
        
        adjusted = {}
        for indicator, weight in default_weights.items():
            multiplier = multipliers.get(indicator, 1.0)
            adjusted[indicator] = weight * multiplier
        
        # Normalize to sum to 100
        total = sum(adjusted.values())
        adjusted = {k: (v / total) * 100 for k, v in adjusted.items()}
        
        return adjusted
    
    def get_indicator_thresholds(self, indicator: str) -> Dict[str, Any]:
        """Get thresholds for an indicator
        
        Args:
            indicator: Indicator name
        
        Returns:
            Dict of threshold values
        """
        return self.config['indicator_thresholds'].get(indicator, {})
    
    def get_screening_filters(self) -> Dict[str, Any]:
        """Get screening filter thresholds"""
        return self.config['screening_filters']
    
    def get_recommendation_levels(self) -> Dict[str, Dict[str, Any]]:
        """Get recommendation levels and their score thresholds"""
        return self.config['scoring']['recommendation_levels']
    
    def get_recommendation_by_score(self, score: float) -> str:
        """Get recommendation level based on score
        
        Args:
            score: AI score (0-100)
        
        Returns:
            Recommendation level
        """
        levels = self.get_recommendation_levels()
        
        if score >= levels['strong_buy']['min_score']:
            return 'Strong Buy'
        elif score >= levels['buy']['min_score']:
            return 'Buy'
        elif score >= levels['watch']['min_score']:
            return 'Watch'
        else:
            return 'Ignore'
    
    def set_db_settings(self, settings: Dict[str, str]):
        """Set settings loaded from database
        
        Args:
            settings: Dict of setting_key -> setting_value
        """
        self.db_settings = settings
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting from database or config
        
        Args:
            key: Setting key
            default: Default value if not found
        
        Returns:
            Setting value
        """
        if key in self.db_settings:
            return self.db_settings[key]
        return default
    
    def get_market_regime(self) -> str:
        """Get current market regime from settings"""
        regime = self.get_setting('market_regime', 'bull')
        if regime not in ['bull', 'sideway', 'bear']:
            regime = 'bull'
        return regime
