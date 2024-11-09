# Viriback to MISP

This project aims to get the detection generated for the project [C2 Tracker](https://tracker.viriback.com/), and create events in MISP. 

The events will be distributed by month/year and malware family, like the example below. In each event will be created objects for each IOC detected in the C2 Tracker.


|![](https://github.com/santiag02/viriback2misp/blob/main/media/misp.png)|
|:---:|
|MISP Events|

## How install

```bash
pip install viriback2misp
```