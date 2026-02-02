import numpy as np
from scipy import stats

def sharpe_ratio(returns, risk_free_rate=0.0):
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def sharpe_significance(returns):
    sharpe = sharpe_ratio(returns)
    n = len(returns)
    standard_error = np.sqrt((1 + 0.5 * sharpe**2) / n)
    z_score = sharpe / standard_error
    p_value = 1 - stats.norm.cdf(z_score)
    return sharpe, p_value

def drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    return (cumulative - peak) / peak
# python -m streamlit run app.py
 
