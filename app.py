from flask import Flask, request, jsonify
from datetime import datetime
from portfolio import Portfolio
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

portfolio = Portfolio()

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    try:
        ticker = data['ticker']
        shares = float(data['shares'])
        portfolio.add_stock(ticker, shares)
        return jsonify({
            "status": "success",
            "message": f"Added {shares} shares of {ticker} to portfolio"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/calculate_profit', methods=['POST'])
def calculate_profit():
    data = request.get_json()
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        annualized = data.get('annualized', False)
        
        portfolio.load_data(start_date, end_date)
        
        profit = portfolio.profit(start_date, end_date, annualized)
        
        return jsonify({
            "status": "success",
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "annualized": annualized,
            "profit": profit if not annualized else profit * 100,
            "unit": "USD" if not annualized else "%"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/portfolio_plot', methods=['POST'])
def get_portfolio_plot():
    data = request.get_json()
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        
        portfolio.load_data(start_date, end_date)
        
        plt.figure(figsize=(12, 6))
        date_range = pd.date_range(start=start_date, end=end_date)
        portfolio_values = []
        
        for date in date_range:
            total_value = sum(
                stock_info['stock'].price(date) * stock_info['shares']
                for stock_info in portfolio.stocks.values()
            )
            portfolio_values.append(total_value)
        
        plt.plot(date_range, portfolio_values, label='Portfolio Value')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value (USD)')
        plt.title('Portfolio Value Over Time')
        plt.legend()
        plt.grid(True)
        
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png')
        img_bytes.seek(0)
        plt.close()
        
        return jsonify({
            "status": "success",
            "plot": base64.b64encode(img_bytes.getvalue()).decode()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
