import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from load import get_connection

MIN_PAIR = 2

with open("sql/skill_pairs.sql", encoding="utf-8") as f:
    query = f.read()

conn = get_connection()
cur = conn.cursor()
cur.execute(query)
pairs = cur.fetchall()
cur.execute("SELECT skill, COUNT(*) FROM posting_skills GROUP BY skill")
skill_counts = dict(cur.fetchall())
conn.close()

G = nx.Graph()
for s1, s2, n in pairs:
    if n >= MIN_PAIR:
        G.add_edge(s1, s2, weight=n)

sizes = [skill_counts.get(node, 1) * 150 for node in G.nodes]
widths = [G[u][v]["weight"] * 0.6 for u, v in G.edges]
pos = nx.spring_layout(G, seed=42, k=0.9)

plt.figure(figsize=(10, 8))
nx.draw_networkx_edges(G, pos, width=widths, alpha=0.5)
nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color="#4C78A8")
nx.draw_networkx_labels(G, pos, font_size=9)
plt.axis("off")
plt.tight_layout()
plt.savefig("docs/skill_network.png", dpi=150)

print("Skills in network:", G.number_of_nodes())
print("Connections:", G.number_of_edges())