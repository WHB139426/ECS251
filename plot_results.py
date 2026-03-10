import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists("logs/plots"):
    os.makedirs("logs/plots")

print("📊 Loading experiment_results.csv...")
df = pd.read_csv("experiment_results.csv")

# filter sync under different worker number
df = df[~((df['Mode'] == 'sync') & (df['Workers'] > 1))]

# 颜色映射，保证图表统一
colors = {'sync': 'gray', 'thread': 'blue', 'process': 'red', 'async': 'green'}

# ==========================================
# Figure 1: Throughput vs CPU Load Intensity (Crossover Point)
# Fix 8 Workers
# ==========================================
plt.figure(figsize=(8, 5))
df_8w = df[(df['Workers'] == 8) | (df['Mode'] == 'sync')]
for mode in df_8w['Mode'].unique():
    subset = df_8w[df_8w['Mode'] == mode]
    plt.plot(subset['Matrix_Size'], subset['Throughput'], marker='o', label=mode.upper(), color=colors.get(mode))

plt.title('Throughput vs CPU Load Intensity (Workers=8)')
plt.xlabel('CPU Load (Matrix Size N x N)')
plt.ylabel('Throughput (Files / Sec)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("logs/plots/throughput_vs_cpuload.png", dpi=300)
print("Saved logs/plots/throughput_vs_cpuload.png")

# ==========================================
# Figure 2: OS Context Switches Overhead
# ==========================================
if 'Context_Switches' in df.columns:
    plt.figure(figsize=(8, 5))
    df_io = df[df['Matrix_Size'] == 0] # Pure I/O
    
    for mode in df_io['Mode'].unique():
        subset = df_io[df_io['Mode'] == mode]
        plt.plot(subset['Workers'], subset['Context_Switches'], marker='s', label=mode.upper(), color=colors.get(mode))

    plt.title('OS Context Switches Overhead (Pure I/O)')
    plt.xlabel('Number of Workers')
    plt.ylabel('Total Context Switches')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("logs/plots/context_switches_overhead.png", dpi=300)
    print("Saved logs/plots/context_switches_overhead.png")

# ==========================================
# Figure 3: Peak Memory Consumption
# ==========================================
if 'Peak_Memory_MB' in df.columns:
    plt.figure(figsize=(8, 5))
    df_mem = df[df['Matrix_Size'] == 500]
    
    for mode in df_mem['Mode'].unique():
        subset = df_mem[df_mem['Mode'] == mode]
        plt.plot(subset['Workers'], subset['Peak_Memory_MB'], marker='^', label=mode.upper(), color=colors.get(mode))

    plt.title('Peak Memory Consumption (High CPU Load)')
    plt.xlabel('Number of Workers')
    plt.ylabel('Peak Memory (MB)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("logs/plots/peak_memory_overhead.png", dpi=300)
    print("Saved logs/plots/peak_memory_overhead.png")
    
print("✅ Plotting complete!")