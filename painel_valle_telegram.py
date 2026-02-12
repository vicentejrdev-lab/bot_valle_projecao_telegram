import requests
import psycopg2
import os

# ========================
# VARIÁVEIS DO GITHUB
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# =====================================================
# MENSAGEM 3 — RESUMO GERAL
# =====================================================

cursor.execute("SELECT * FROM vw_valle_projecao_geral_telegram;")
g = cursor.fetchone()

mensagem_geral = f"""
📊 *VALLE — RESUMO DO MÊS*

🎯 Meta: {g[0]}
🧾 Total de placas: {g[1]}
📉 GAP: {g[2]}

⚙ Ritmo atual: {g[5]}
📈 Ritmo exigido: {g[6]}

🔮 Projeção: {int(g[7])}
📊 Probabilidade de bater meta: {g[8]}%

⏳ Dias úteis restantes: {g[4]}
"""

requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem_geral, "parse_mode":"Markdown"})

# =====================================================
# MENSAGEM 1 — COOPERATIVAS
# =====================================================

cursor.execute("SELECT * FROM vw_valle_projecao_cooperativa_telegram;")
coops = cursor.fetchall()

mensagem_coop = "🏢 *VALLE — COOPERATIVAS*\n\n"

for c in coops:
    mensagem_coop += (
        f"*{c[0]}*\n"
        f"Placas: {c[2]} | Ritmo: {c[6]} | Exigido: {c[7]}\n"
        f"Projeção: {int(c[8])} | Prob: {c[9]}%\n\n"
    )

requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem_coop, "parse_mode":"Markdown"})

# =====================================================
# MENSAGEM 2 — TOP 10 CONSULTORES
# =====================================================

cursor.execute("""
SELECT *
FROM vw_valle_projecao_consultor_telegram
ORDER BY vendas DESC
LIMIT 10;
""")
consultores = cursor.fetchall()

mensagem_consultor = "👤 *VALLE — TOP 10 CONSULTORES*\n\n"

for c in consultores:
    mensagem_consultor += (
        f"{c[0]}\n"
        f"Placas: {c[1]} | Ritmo: {c[2]} | Projeção: {int(c[3])}\n\n"
    )


requests.post(url, data={"chat_id": CHAT_ID, "text": mensagem_consultor, "parse_mode":"Markdown"})

print("Painel completo enviado!")
