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

![heatmap](./heatmap.jpeg)

Open jupyter, read in csv, import matplotlib then plot heatmap plot, got the flag.
