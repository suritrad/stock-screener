"""Stock Screener Flask Application"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

# Import API blueprints
from src.api.screener_routes import screener_bp
from src.api.stocks_routes import stocks_bp


def create_app(config_class=None):
    """Application factory
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Flask application instance
    """
    if config_class is None:
        config_class = get_config()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(app)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(screener_bp)
    app.register_blueprint(stocks_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0-alpha',
            'environment': app.config['FLASK_ENV']
        }), 200
    
    return app


def setup_logging(app):
    """Setup logging configuration
    
    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Create logs directory
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Create file handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,
            backupCount=10
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Stock Screener startup')


def register_error_handlers(app):
    """Register error handlers
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal error occurred',
            'status': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        return jsonify({
            'error': 'Server Error',
            'message': str(error),
            'status': 500
        }), 500


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['FLASK_HOST'],
        port=app.config['FLASK_PORT'],
        debug=app.config['DEBUG']
    )
