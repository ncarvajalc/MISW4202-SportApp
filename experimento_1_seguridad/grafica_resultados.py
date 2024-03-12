import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("./ResultadosExperimentoSeguridad.csv")

df = pd.DataFrame(data, columns=["label", "responseCode"])

success_code = 200

df_filtered = df[~df["label"].str.contains("Solicitud token")]

total_counts = df_filtered["label"].value_counts()

success_counts = df_filtered[df_filtered["responseCode"] == success_code][
    "label"
].value_counts()

success_percentages = (success_counts / total_counts) * 100

plt.figure(figsize=(10, 6))
success_percentages.plot(kind="barh", color="green")
plt.xlabel("Porcentaje de éxito")
plt.ylabel("Tipo de solicitud")
plt.title("Porcentaje de éxito por cada tipo de solicitud")
plt.tight_layout()
plt.show()
