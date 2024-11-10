# FuckExcel

- Easier to operate excel.

## Install

```shell
pip3 install git+https://github.com/Rhythmicc/FuckExcel.git -U
```

## DEMO
### demo - 1

```python
from FuckExcel import FuckExcel

fuck_excel = FuckExcel('./A.xlsx')
fuck_excel[5:10, 5:10] = 'init' # or ['init', 'init', 'init', 'init', 'init']
fuck_excel.save()
```

- Demo will create `A.xlsx` and set init value.

![demo](demo.png)

### demo - 2

```python
from FuckExcel import FuckExcel

fuck_excel = FuckExcel('./A.xlsx') # default with_numba is False
fuck_excel[5:, 1] = [1, 2, 3, 4, 5]  # set [5][1]~[10][1] = [1, 2, 3, 4, 5]
fuck_excel.save()
```

