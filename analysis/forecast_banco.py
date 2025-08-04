from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import os
from openpyxl.styles import numbers

def prever_crescimento_total(df: pd.DataFrame, tipo: str = "TotalSizeMB", salvar_excel=True):
    if tipo not in ["TotalSizeMB", "RowCounts"]:
        raise ValueError("tipo deve ser 'TotalSizeMB' ou 'RowCounts'.")

    df_agg = df.groupby("DataHoraColeta").agg({tipo: "sum"}).reset_index()
    df_agg = df_agg.rename(columns={"DataHoraColeta": "ds", tipo: "y"}).dropna()

    modelo = Prophet()
    modelo.fit(df_agg)

    futuro = modelo.make_future_dataframe(periods=365)
    previsao = modelo.predict(futuro)

    modelo.plot(previsao)
    plt.title(f"Previsão de crescimento total ({tipo})")
    plt.tight_layout()
    plt.show()

    previsao["ds"] = pd.to_datetime(previsao["ds"])
    previsao["ano_mes"] = previsao["ds"].dt.to_period("M")
    previsao_mensal = (
        previsao.groupby("ano_mes")["yhat"]
        .sum()
        .reset_index()
        .rename(columns={"yhat": f"Previsao_{tipo}_Mensal"})
    )

    if salvar_excel:
        os.makedirs("data", exist_ok=True)
        caminho_saida = os.path.join("data", f"previsao_{tipo.lower()}_mensal.xlsx")

        with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
            previsao_mensal.to_excel(writer, index=False, sheet_name="Previsao")
            worksheet = writer.sheets["Previsao"]
            for cell in worksheet["B"]:
                cell.number_format = "#,##0"

        print(f"📁 Previsão mensal exportada para: {caminho_saida}")

    return previsao_mensal
