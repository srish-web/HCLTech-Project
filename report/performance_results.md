## Performance Benchmark Results

**Dataset size:** 500 trip records  
**Benchmark procedure:** One warm-up run followed by seven measured runs per operation.  
**Summary statistic:** Median execution time.

| Operation | Median (s) | Minimum (s) | Maximum (s) |
|---|---:|---:|---:|
| Data validation | 0.0036 | 0.0025 | 0.0153 |
| Statistical fuel analysis | 0.0087 | 0.0063 | 0.0186 |
| Isolation Forest | 0.3891 | 0.3456 | 0.4257 |
| Delivery analytics | 0.0016 | 0.0013 | 0.0042 |
| Route analysis | 0.0183 | 0.0169 | 0.0238 |

### Interpretation

All five operations completed successfully during the benchmark. Isolation Forest had the highest median execution time, at 0.3891 seconds. Delivery analytics had the lowest median execution time, at 0.0016 seconds.

The measurements indicate that the analytical functions execute quickly on the current 500-record dataset. The difference between minimum and maximum timings also demonstrates that execution time varies between runs.

These measurements represent function execution time only. They do not include full dashboard startup, browser rendering, API latency, or concurrent users. Further testing is required to assess scalability.

### Reproducibility

The benchmark used `time.perf_counter()`, a warm-up execution, and seven measured executions per operation. The median was used as the primary summary statistic. Results may vary with hardware, operating-system activity, Python version, and installed package versions.
