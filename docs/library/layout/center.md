---
components:
    - rx.radix.themes.Center
---

```python exec
import reflex as rx
import reflex.components.radix.themes as rdxt
```

 
# Center

`Center` is a component that centers its children within itself. It is based on the `flex` component and therefore inherits all of its props.


```python demo
rx.center(
    rx.text("Hello World!"),
    border_radius="15px",
    border_width="thick",
    width="50%",
)
```