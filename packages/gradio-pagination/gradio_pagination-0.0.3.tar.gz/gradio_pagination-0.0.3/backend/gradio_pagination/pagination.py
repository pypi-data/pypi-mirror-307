from __future__ import annotations

import json
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Callable, Sequence

from gradio.components.base import Component, FormComponent
from gradio.events import Events

if TYPE_CHECKING:
    from gradio.components import Timer


class pagination(FormComponent):
    """
    Custom pagination component for Gradio that allows users to handle pagination 
    logic in a simple and interactive way.

    This component is designed to allow users to specify the total number of items,
    the current page number, and the size of each page, while providing basic input 
    and output functionalities.

    Attributes:
        EVENTS (list): List of events that the component can emit.
    """

    EVENTS = [
        Events.change,
    ]

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        placeholder: str | None = None,
        label: str | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        rtl: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        total: int | None = 0,
        page: int | None = 1,
        page_size: int | None = 10,
    ):
        """
        Initializes the pagination component.

        Parameters:
            total (int | None): Total number of items for pagination.
            page (int | None): Current page number.
            page_size (int | None): Number of items per page.
        """
        self.placeholder = placeholder
        self.rtl = rtl
        
        # Serialize pagination info to JSON format for initial value
        value_json = json.dumps({
            "total": int(total),
            "page": int(page),
            "page_size": int(page_size)
        })
        
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value or value_json,
            render=render,
            key=key,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """
        Preprocesses the input received from the component.

        This method converts the JSON string input into a Python object.

        Parameters:
            payload (str | None): The input JSON string from the component.

        Returns:
            str | None: Returns a namespace object representing the pagination state 
            or None if the input is invalid.
        """
        try:
            if payload is not None:
                # Convert the JSON payload to a namespace object for easy attribute access
                page_obj = json.loads(payload, object_hook=lambda d: SimpleNamespace(**d))
                return page_obj
        except TypeError as e:
            print(f"something goes wrong: {e}")
        return None

    def postprocess(self, value: str | None) -> str | None:
        """
        Postprocesses the output to be displayed in the component.

        Converts the output value to a string format.

        Parameters:
            value (str | None): The output value returned from the processing function.

        Returns:
            str | None: The string representation of the output value to be displayed 
            in the component or None if the value is None.
        """
        return None if value is None else str(value)

    def api_info(self) -> dict[str, Any]:
        """
        Provides API information about the component.

        Returns:
            dict[str, Any]: A dictionary containing information about the component's type.
        """
        return {"type": "string"}

    def example_payload(self) -> Any:
        """
        Provides an example payload for the component.

        Returns:
            Any: An example string that represents a typical payload.
        """
        return "Hello!!"

    def example_value(self) -> Any:
        """
        Provides an example value to be displayed in the component.

        Returns:
            Any: An example string that represents a typical value.
        """
        return "Hello!!"
