# Textual Router

A view router for [Textual](https://textual.textualize.io/) inspired by [Solid-Router](https://docs.solidjs.com/solid-router).

## Usage
Create _Views_ from _Static_ widgets.

Use the Router object in your App's compose() and provide links and their _Views_:

```python
    yield Router(
        [
            Route(path="link_to_view_a", view=ViewA()),
            Route(path="link_to_view_b", view=ViewB()),
        ]
    )
```

Within in your _View_, use RouterLinks to navigate to other views.

```python
    yield RouterLink(path="link_to_view_b",label="ViewB")
```



## Full Example
```python
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from textual_router import Route, Router, RouterLink

class Home(Static):

    def compose(self):
        yield RouterLink(path="about", label="About")


class About(Static):
    
    def compose(self):
        yield RouterLink(path="home", label="Home")

class BasicApp(App):
    TITLE = "Basic app"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Router(
            [
                Route(path="home", view=Home()),
                Route(path="about", view=About()),
            ]
        )
        yield Footer()

```