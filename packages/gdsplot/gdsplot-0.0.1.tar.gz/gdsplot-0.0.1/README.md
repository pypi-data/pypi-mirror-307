# gdsplot
Turn a GDS or OAS file into a Plotly figure.

![image](https://github.com/user-attachments/assets/08d173c3-93c1-4b93-bbfb-0645147982cf)

Click a layer in the legend to hide, or double click a layer to hide all others.

## installation
```
pip install gdsplot
```

## usage
```python
from gdsplot import create_gdsplot

fig = create_gdsplot(
    file_path=file_path,
    show_layers=True,
)
```

## supported file types
- .oas
- .gds
- .gds2

## example gds files
https://www.yzuda.org/download/_GDSII_examples.html

## requires
- plotly>=5.24.1
- gdstk>=0.9.55
- distinctipy>=1.3.4
- shapely>=2.0.0
- nbformat>=4.2.0

