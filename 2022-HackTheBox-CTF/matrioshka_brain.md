# Matrioshka Brain

```
score: 300
solved: xx/xx
difficulty: easy
tags: heatmap, misc
```

## Problem

Given a CSV file with 5 rows, each row was 162 data points which measure
"temperature" of each dyson sphere over time.

The hint here was about "heat" in problem description.
After a loooooong time stuck, we think this may
hint use a "heatmap" graph to show the flag.

Open [jupyter](https://jupyter.org/), read in csv, import matplotlib then plot heatmap plot, got the flag.

```py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/home/hvn/Downloads/htb/heat_measurements.csv")
d2 = d2.astype(np.int32)
plt.imshow(d2.T, cmap='hot', interpolation='nearest')
```

![heatmap](./heatmap.jpeg)
