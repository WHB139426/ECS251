import pandas as pd
import matplotlib.pyplot as plt
import os

# 创建图表保存目录
if not os.path.exists("logs/plots"):
    os.makedirs("logs/plots")

print("📊 Loading experiment_results.csv...")
df = pd.read_csv("experiment_results.csv")

# 过滤掉 sync 模型在不同 worker 下的重复数据（因为它只用单线程）
df = df[~((df['Mode'] == 'sync') & (df['Workers'] > 1))]

# 颜色映射，保证图表统一
colors = {'sync': 'gray', 'thread': 'blue', 'process': 'red', 'async': 'green'}

# ==========================================
# 图表 1: 吞吐量 vs CPU 负载强度 (Crossover Point)
# 我们固定 8 个 Workers，看不同负载下谁更强
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
# 图表 2: 上下文切换代价分析 (Context Switches)
# ==========================================
if 'Context_Switches' in df.columns:
    plt.figure(figsize=(8, 5))
    df_io = df[df['Matrix_Size'] == 0] # 选纯IO场景
    
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
# 图表 3: 内存开销分析 (Peak Memory)
# ==========================================
if 'Peak_Memory_MB' in df.columns:
    plt.figure(figsize=(8, 5))
    df_mem = df[df['Matrix_Size'] == 500] # 选高负载场景看内存分配
    
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