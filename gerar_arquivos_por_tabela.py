import os
import pandas as pd
from prophet import Prophet
from config.database import SQLServerConnector
from etl.extract_data import carregar_dados
from pathlib import Path

def preparar_previsao(df_tabela, coluna_valor):
    df = df_tabela[["DataHoraColeta", coluna_valor]].copy()
    df["DataHoraColeta"] = pd.to_datetime(df["DataHoraColeta"])
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors="coerce")
    df = df.dropna()

    # Agrupar por mês
    df = df.groupby(pd.Grouper(key="DataHoraColeta", freq="MS"))[coluna_valor].sum().reset_index()
    df.columns = ["ds", "y"]

    if len(df) < 3 or df["y"].sum() == 0:
        return None

    modelo = Prophet()
    modelo.fit(df)

    futuro = modelo.make_future_dataframe(periods=6, freq="MS")
    forecast = modelo.predict(futuro)

    forecast_resultado = forecast[["ds", "yhat"]].copy()
    forecast_resultado.columns = ["ds", f"{coluna_valor}_previsto"]

    return forecast_resultado

def gerar_arquivos_por_tabela():
    df = carregar_dados()

    df["DataHoraColeta"] = pd.to_datetime(df["DataHoraColeta"])
    df["RowCounts"] = pd.to_numeric(df["RowCounts"], errors="coerce")
    df["TotalSizeMB"] = pd.to_numeric(df["TotalSizeMB"], errors="coerce")

    output_dir = Path("data/tabelas")
    output_dir.mkdir(parents=True, exist_ok=True)

    tabelas = df["TableName"].unique()

    for tabela in tabelas:
        df_tabela = df[df["TableName"] == tabela].copy()

        previsao_linhas = preparar_previsao(df_tabela, "RowCounts")
        previsao_tamanho = preparar_previsao(df_tabela, "TotalSizeMB")

        # Verificação de dados insuficientes
        if previsao_linhas is None or previsao_tamanho is None:
            print(f"⚠️ Tabela '{tabela}' ignorada por falta de dados suficientes.")
            continue

        df_final = pd.merge(previsao_linhas, previsao_tamanho, on="ds", how="outer")
        df_final["TotalSizeGB_previsto"] = df_final["TotalSizeMB_previsto"] / 1024
        df_final = df_final.sort_values("ds")

        caminho_saida = output_dir / f"TABELA_{tabela}.xlsx"
        with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
            df_final.to_excel(writer, sheet_name="Previsao_Mensal", index=False)

        print(f"✅ Previsão gerada para: {tabela}")

if __name__ == "__main__":
    gerar_arquivos_por_tabela()
