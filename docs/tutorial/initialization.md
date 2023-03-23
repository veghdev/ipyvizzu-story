# Initialization

## Import

From `ipyvizzu` import `Data`, `Config` and `Style` and from `ipyvizzu-story`
import `Story`, `Slide` and `Step`:

```python
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
```

## Constructor

You need to put the `Data` object (described in the [Data](./data.md) chapter)
into the `Story` constructor. You can not alter the data later but the data
being shown can be filtered at each step.

```python
story = Story(data=data)
```

You can set the style used initally for the story as you can see in this
[example](../examples/usbudget.ipynb), and you can alter the style at each step
within the story.

```python
story = Story(data=data, style=Style({"title": {"fontSize": 50}}))
```

!!! tip
    Check
    [ipyvizzu - Color palette & fonts chapter](https://ipyvizzu.vizzuhq.com/latest/tutorial/color_palette_fonts/)
    and
    [ipyvizzu - Chart layout chapter](https://ipyvizzu.vizzuhq.com/latest/tutorial/chart_layout/)
    for more details on the available styling options.
