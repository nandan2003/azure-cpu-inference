# Automated Benchmark Report
## Execution Environment: Azure Standard_D4s_v3 (4 vCPU)
```
Model                  | Threads  | Speed (t/s)  | RAM (GB)  
-----------------------------------------------------------------
Mistral-7B (Baseline)  | 2        | 2.64         | 7.51      
Mistral-7B (Baseline)  | 4        | 2.99         | 7.53      
Phi-3-Mini (Optimized) | 4        | 8.11         | 5.03      
-----------------------------------------------------------------
```

## System Latency (Cold vs Warm Start)
```
--- STARTING KERNEL MEMORY LATENCY TEST ---
 [System] Clearing OS Page Cache...
 COLD START (Disk Read) Load Time: 12.2544 seconds
 WARM START (RAM Cache) Load Time: 2.1095 seconds
---------------------------------------
```
