"""A view router for Textual"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeAlias, cast

from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Static


class RouterLink(Button):
    """Class that navigates to the provided path"""

    path: str

    def __init__(self, path: str, **kargs):
        super().__init__(**kargs)
        self.path = path

    class Clicked(Message):
        """Message carrier for link clicks"""

        path: str

        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    async def on_button_pressed(self) -> None:
        """Notifies the Router class that link was clicked"""

        self.post_message(self.Clicked(self.path))


@dataclass
class Route:
    """The class used when defining the routes of an application."""

    path: str
    view: Static


Routes: TypeAlias = list[Route]


class RouterType(ABC):
    """For typing hinting Router class"""

    @abstractmethod
    def route_to(self, path: str):
        """Route to path"""

        pass


def Router(routes: Routes, identifier: str = "router") -> Static:
    """The top level class that manages the routing of your application"""

    class __Router(Static):
        """The routing class"""

        internal_routes = {x.path: x.view for x in routes}
        link = reactive(next(iter(internal_routes)))
        id = identifier

        def watch_link(self, old_link: str, new_link: str) -> None:
            """Reactive response to the link change"""

            if old_link != new_link:
                prev_view = type(self.internal_routes[old_link]).__name__
                self.query_one(prev_view).remove()

            self.mount(cast(Widget, self.internal_routes[new_link]))

        def on_router_link_clicked(self, message: RouterLink.Clicked) -> None:
            """Updates the current link of the Router"""

            self.link = message.path

        def route_to(self, path: str):
            """Route to path"""

            self.link = path

    return __Router()
