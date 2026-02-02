import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation(df):
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Strategy Correlation")
    return fig
