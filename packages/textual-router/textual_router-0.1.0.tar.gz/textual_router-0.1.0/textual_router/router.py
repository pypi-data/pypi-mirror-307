"""A view router for Textual"""

from typing import TypeAlias, cast

from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Static


class RouterLink(Button):
    """Component that navigates to the provided path"""

    page: str

    def __init__(self, page: str, **kargs):
        super().__init__(**kargs)
        self.page = page

    class Clicked(Message):
        """Message carrier for link clicks"""

        page: str

        def __init__(self, page: str) -> None:
            self.page = page
            super().__init__()

    async def on_button_pressed(self) -> None:
        """Notifies the Router component that link was clicked"""

        self.post_message(self.Clicked(self.page))


# The dict used when defining the routes of an application.
Routes: TypeAlias = dict[str, Static]


def Router(routes: Routes):
    """The top level component that manages the routing of your application"""

    class Router(Static):
        """The routing class"""

        link = reactive(next(iter(routes)))

        def watch_link(self, old_link: str, new_link: str) -> None:
            """Reactive response to the link change"""

            if old_link != new_link:
                route_name = f"{type(routes[old_link]).__name__}"
                self.query_one(route_name).remove()

            self.mount(cast(Widget, routes[new_link]))

        def on_router_link_clicked(self, message: RouterLink.Clicked) -> None:
            """Updates the current link of the Router"""
            self.link = message.page

    return Router()
