import pandas as pd
from config.database import SQLServerConnector

def carregar_dados():
    conn = SQLServerConnector().get_connection()
    query = "SELECT * FROM HIST_CRESC_TABELAS"
    df = pd.read_sql(query, conn)
    conn.close()

    # Conversões de tipo
    df["DataHoraColeta"] = pd.to_datetime(df["DataHoraColeta"])
    df["RowCounts"] = pd.to_numeric(df["RowCounts"], errors='coerce')
    df["TotalSizeMB"] = pd.to_numeric(df["TotalSizeMB"], errors='coerce')
    df["AvgSizePerRowKB"] = pd.to_numeric(df["AvgSizePerRowKB"], errors='coerce')

    # Mostrar resumo por tabela (último snapshot)
    print("\n📋 Resumo das tabelas no último snapshot:\n")
    ultima_data = df["DataHoraColeta"].max()
    df_ult = df[df["DataHoraColeta"] == ultima_data]

    resumo = df_ult[["TableName", "RowCounts", "TotalSizeMB"]].sort_values("TotalSizeMB", ascending=False)

    for _, row in resumo.iterrows():
        nome_tabela = str(row['TableName'])
        linhas = int(row['RowCounts']) if pd.notnull(row['RowCounts']) else 0
        tamanho_mb = float(row['TotalSizeMB']) if pd.notnull(row['TotalSizeMB']) else 0.0

        print(f"📦 {nome_tabela:<35} | 📈 {linhas:>12,} linhas | 💾 {tamanho_mb:>10.2f} MB")

    return df
