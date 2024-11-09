# Textual Router

A view router for [Textual](https://textual.textualize.io/) inspired by [Solid-Router](https://docs.solidjs.com/solid-router).

## Usage
Create _Views_ from _Static_ widgets.

Use the Router object in your App's compose() and provide links and their _Views_:

```python
    yield Router(
        {
            "link_to_component_a": ComponentA,
            "link_to_component_a": ComponentB,
        }
    )
```

Within in your _View_, user RouterLinks to navigate to other views.

```python
    yield RouterLink(page="link_to_component_b",label="ComponentB")
```



## Full Example
```python
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from textual_router import Router, RouterLink

class Home(Static):

    def compose(self):

        yield RouterLink(page="about", label="About")


class About(Static):
    
    def compose(self):

        yield RouterLink(page="home", label="Home")

class BasicApp(App):
    TITLE = "Basic app"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Router(
            {
                "home": Home(),
                "about": About(),
            }
        )
        yield Footer()

```