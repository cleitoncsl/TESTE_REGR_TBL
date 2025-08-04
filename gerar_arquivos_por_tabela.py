import os
import pandas as pd
from prophet import Prophet
from etl.extract_data import carregar_dados

def gerar_previsao(df, coluna_valor, nome_coluna_resultado):
    if df[coluna_valor].nunique() < 2:
        print(f"⚠️  Dados insuficientes para previsão de '{coluna_valor}'. Gerando valores constantes.")
        ultimo_valor = df[coluna_valor].iloc[-1]
        futuro = pd.date_range(start=df["DataHoraColeta"].max(), periods=14, freq='MS')
        previsao = pd.DataFrame({
            'ano_mes': futuro.strftime('%Y-%m'),
            nome_coluna_resultado: [ultimo_valor] * len(futuro)
        })
    else:
        df_prophet = df[["DataHoraColeta", coluna_valor]].rename(columns={"DataHoraColeta": "ds", coluna_valor: "y"})
        modelo = Prophet()
        modelo.fit(df_prophet)

        futuro = modelo.make_future_dataframe(periods=14, freq='MS')
        forecast = modelo.predict(futuro)
        forecast["ano_mes"] = forecast["ds"].dt.strftime("%Y-%m")
        previsao = forecast[["ano_mes", "yhat"]].rename(columns={"yhat": nome_coluna_resultado})

    return previsao

def gerar_arquivos_por_tabela():
    df = carregar_dados()
    tabelas = df["TableName"].unique()

    os.makedirs("data/tabelas", exist_ok=True)

    for tabela in tabelas:
        df_tabela = df[df["TableName"] == tabela].copy()
        df_tabela = df_tabela.sort_values("DataHoraColeta")

        resumo = df_tabela[["TableName", "DataHoraColeta", "RowCounts", "TotalSizeMB"]].copy()
        resumo["TotalSizeGB"] = resumo["TotalSizeMB"] / 1024

        previsao_row = gerar_previsao(df_tabela, "RowCounts", "Previsao_RowCounts_Mensal")
        previsao_size = gerar_previsao(df_tabela, "TotalSizeMB", "Previsao_TotalSizeMB_Mensal")
        previsao_size["Previsao_TotalSizeGB_Mensal"] = previsao_size["Previsao_TotalSizeMB_Mensal"] / 1024

        caminho_saida = f"data/tabelas/{tabela}.xlsx"
        with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
            resumo.to_excel(writer, sheet_name="Resumo", index=False)
            previsao_row.to_excel(writer, sheet_name="Previsao_RowCounts", index=False)
            previsao_size.to_excel(writer, sheet_name="Previsao_TotalSizeMB", index=False)

        print(f"✅ Arquivo gerado para a tabela '{tabela}': {caminho_saida}")
