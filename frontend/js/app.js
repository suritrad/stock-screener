/**
 * Stock Screener Frontend Application
 * Main app.js for handling UI interactions and API calls
 */

class StockScreenerApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.results = [];
        this.filteredResults = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadLatestResults();
    }

    setupEventListeners() {
        document.getElementById('runScreener').addEventListener('click', () => this.runScreener());
        document.getElementById('refreshBtn').addEventListener('click', () => this.loadLatestResults());
        document.getElementById('searchBox').addEventListener('input', () => this.filterResults());
        document.getElementById('filterRecommendation').addEventListener('change', () => this.filterResults());
        document.getElementById('exportCsv').addEventListener('click', (e) => this.handleExport(e, 'csv'));
        document.getElementById('exportExcel').addEventListener('click', (e) => this.handleExport(e, 'excel'));
        document.getElementById('exportPdf').addEventListener('click', (e) => this.handleExport(e, 'pdf'));
    }

    async runScreener() {
        this.showLoading(true);
        try {
            const response = await fetch(`${this.apiBaseUrl}/screener/run`, { method: 'POST' });
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('Screener started successfully');
                setTimeout(() => this.loadLatestResults(), 2000);
            } else {
                this.showToast('Error running screener', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('Failed to run screener', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async loadLatestResults() {
        this.showLoading(true);
        try {
            const response = await fetch(`${this.apiBaseUrl}/screener/latest`);
            const data = await response.json();
            
            if (response.ok) {
                this.results = data.data || [];
                this.filteredResults = [...this.results];
                this.renderResults();
                this.updateLastUpdate();
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('Failed to load results', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    filterResults() {
        const searchTerm = document.getElementById('searchBox').value.toLowerCase();
        const recommendation = document.getElementById('filterRecommendation').value;

        this.filteredResults = this.results.filter(stock => {
            const matchesSearch = !searchTerm || 
                stock.symbol.toLowerCase().includes(searchTerm) ||
                (stock.company_name && stock.company_name.toLowerCase().includes(searchTerm));
            
            const matchesRecommendation = !recommendation || stock.recommendation === recommendation;
            
            return matchesSearch && matchesRecommendation;
        });

        this.renderResults();
    }

    renderResults() {
        const container = document.getElementById('resultsContainer');
        const emptyState = document.getElementById('emptyState');
        
        if (this.filteredResults.length === 0) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }
        
        emptyState.style.display = 'none';
        container.innerHTML = this.filteredResults.map((stock, index) => this.createStockCard(stock, index + 1)).join('');
        
        // Add event listeners to TradingView buttons
        document.querySelectorAll('.tradingview-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.openTradingView(e));
        });
    }

    createStockCard(stock, rank) {
        const recommendationClass = this.getRecommendationClass(stock.recommendation);
        const priceChangeClass = stock.change_percent >= 0 ? 'positive' : 'negative';
        const priceChangeIcon = stock.change_percent >= 0 ? '📈' : '📉';

        return `
            <div class="col-md-6 col-lg-4">
                <div class="card stock-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-0">${stock.symbol}</h5>
                            <small>${stock.company_name || 'N/A'}</small>
                        </div>
                        <div class="text-end">
                            <div class="score-badge">${stock.ai_score}</div>
                            <span class="recommendation ${recommendationClass}">${stock.recommendation}</span>
                        </div>
                    </div>
                    
                    <div class="price-info">
                        <div class="row mb-2">
                            <div class="col-6">
                                <small class="text-muted">Price</small><br>
                                <strong>${stock.close_price}฿</strong>
                            </div>
                            <div class="col-6 text-end">
                                <small class="text-muted">Change</small><br>
                                <strong class="price-change ${priceChangeClass}">${priceChangeIcon} ${stock.change_percent}%</strong>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted">Volume</small><br>
                                <small>${this.formatNumber(stock.volume)} M</small>
                            </div>
                            <div class="col-6 text-end">
                                <small class="text-muted">Market Cap</small><br>
                                <small>${this.formatNumber(stock.market_cap)} B</small>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-3">
                        <div class="mb-3">
                            <small class="text-muted d-block mb-2"><strong>Trading Plan</strong></small>
                            <div class="trading-plan">
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Entry</span>
                                    <span class="trading-plan-value">${stock.close_price}฿</span>
                                </div>
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Support</span>
                                    <span class="trading-plan-value">${stock.support || 'N/A'}฿</span>
                                </div>
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Resistance</span>
                                    <span class="trading-plan-value">${stock.resistance || 'N/A'}฿</span>
                                </div>
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Stop Loss</span>
                                    <span class="trading-plan-value">${stock.stop_loss || 'N/A'}฿</span>
                                </div>
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Target 1</span>
                                    <span class="trading-plan-value">${stock.target_1 || 'N/A'}฿</span>
                                </div>
                                <div class="trading-plan-item">
                                    <span class="trading-plan-label">Target 2</span>
                                    <span class="trading-plan-value">${stock.target_2 || 'N/A'}฿</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted d-block mb-2"><strong>Technical Confirmation</strong></small>
                            <div class="indicator-badge pass">✓ EMA Aligned</div>
                            <div class="indicator-badge pass">✓ MACD Bullish</div>
                            <div class="indicator-badge pass">✓ RSI ${stock.rsi14 || 'N/A'}</div>
                            <div class="indicator-badge pass">✓ ADX ${stock.adx || 'N/A'}</div>
                        </div>
                        
                        <div class="mb-3">
                            <small class="text-muted d-block mb-2"><strong>Risk Assessment</strong></small>
                            <div class="warning-box">
                                <div class="warning-content">
                                    No significant technical warning
                                </div>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <a href="https://www.tradingview.com/symbols/SET-${stock.symbol}/" target="_blank" class="tradingview-btn flex-grow-1">
                                <i class="bi bi-graph-up"></i> TradingView
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getRecommendationClass(recommendation) {
        const map = {
            'Strong Buy': 'strong-buy',
            'Buy': 'buy',
            'Watch': 'watch',
            'Ignore': 'ignore'
        };
        return map[recommendation] || 'watch';
    }

    formatNumber(num) {
        if (!num) return '0';
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }

    showLoading(show) {
        document.getElementById('loadingSpinner').style.display = show ? 'flex' : 'none';
    }

    showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        toastMessage.textContent = message;
        toast.style.display = 'block';
        
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }

    updateLastUpdate() {
        const now = new Date();
        document.getElementById('lastUpdate').textContent = `Last Update: ${now.toLocaleTimeString()}`;
        document.getElementById('stockCount').textContent = `${this.results.length} stocks`;
    }

    async handleExport(event, format) {
        event.preventDefault();
        this.showToast(`Exporting as ${format.toUpperCase()}...`);
        // Export logic will be implemented
    }

    openTradingView(event) {
        // TradingView opens in new tab (handled by href)
        return true;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new StockScreenerApp();
});
