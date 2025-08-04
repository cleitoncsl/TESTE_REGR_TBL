import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analisar_tendencias(df: pd.DataFrame):
    top_tabelas = df["TableName"].value_counts().head(3).index

    for tabela in top_tabelas:
        df_tabela = df[df["TableName"] == tabela].sort_values("DataHoraColeta")

        plt.figure()
        sns.lineplot(data=df_tabela, x="DataHoraColeta", y="RowCounts")
        plt.title(f"Crescimento de registros: {tabela}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
