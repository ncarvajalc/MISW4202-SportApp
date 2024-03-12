import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("./ResultadosExperimentoSeguridad.csv")

df = pd.DataFrame(data, columns=["label", "responseCode"])

df = df[~df["label"].str.contains("Solicitud token")]

success_code = 200

total_counts = df["label"].value_counts()
error_counts = df[df["responseCode"] != success_code]["label"].value_counts()

error_percentages = (error_counts / total_counts) * 100

plt.figure(figsize=(10, 6))
error_percentages.plot(kind="barh", color="crimson")
plt.xlabel("Porcentaje de error")
plt.ylabel("Tipo de solicitud")
plt.title("Porcentaje de error por cada tipo de solicitud")
plt.tight_layout()
plt.show()
