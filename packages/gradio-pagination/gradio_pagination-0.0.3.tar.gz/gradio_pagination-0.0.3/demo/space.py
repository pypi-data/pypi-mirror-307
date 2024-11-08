
import gradio as gr
from app import demo as app
import os

_docs = {'pagination': {'description': 'Custom pagination component for Gradio that allows users to handle pagination \nlogic in a simple and interactive way.\n\nThis component is designed to allow users to specify the total number of items,\nthe current page number, and the size of each page, while providing basic input \nand output functionalities.\n\n    EVENTS (list): List of events that the component can emit.', 'members': {'__init__': {'value': {'type': 'str | Callable | None', 'default': 'None', 'description': None}, 'placeholder': {'type': 'str | None', 'default': 'None', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': None}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': None}, 'min_width': {'type': 'int', 'default': '160', 'description': None}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'rtl': {'type': 'bool', 'default': 'False', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': None}, 'total': {'type': 'int | None', 'default': '0', 'description': None}, 'page': {'type': 'int | None', 'default': '1', 'description': None}, 'page_size': {'type': 'int | None', 'default': '10', 'description': None}}, 'postprocess': {'value': {'type': 'str | None', 'description': None}}, 'preprocess': {'return': {'type': 'str | None', 'description': 'str | None: Returns a namespace object representing the pagination state'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the pagination changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'pagination': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_pagination`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_pagination/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_pagination"></a>  
</div>

pagination component
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_pagination
```

## Usage

```python
import json

import gradio as gr
from gradio_pagination import pagination

total=10000
current_page = 1
page_size = 10

def rerender_pagination_total(total_num):
    global total, page_size, current_page
    total = int(total_num)
    current_page = 1 # If the total number changes, whether to reset the current page to 1 depends on your business logic.
    print('overide total to ', total)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size)
    })

def rerender_pagination_page(page):
    global total, page_size, current_page
    current_page = int(page)
    print('overide current_page to ', current_page)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size)
    })

def rerender_pagination_size(size):
    global total, page_size, current_page
    page_size = int(size)
    print('overide page_size to ', page_size)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size)
    })

def show_page_info_into_text_box(data):
    global total, page_size, current_page
    current_page = data.page
    page_size = data.page_size
    total = data.total
    print('pagination change: ', data)
    return str(current_page), str(page_size), str(total)

with gr.Blocks() as demo:
    gr.Markdown("## Pagination Demo")
    pagination_component = pagination(total=total, page=1, page_size=10)

    with gr.Row():
        page_display = gr.Textbox(label="Current Page", value=str(current_page), interactive=True)
        size_display = gr.Textbox(label="Page Size", value=str(page_size), interactive=True)
        total_display = gr.Textbox(label="Total", value=str(total), interactive=True)

    pagination_component.change(
        fn=show_page_info_into_text_box,
        inputs=pagination_component,
        outputs=[page_display, size_display, total_display]
    )
    page_display.change(fn=rerender_pagination_page, inputs=page_display, outputs=pagination_component)
    size_display.change(fn=rerender_pagination_size, inputs=size_display, outputs=pagination_component)
    total_display.change(fn=rerender_pagination_total, inputs=total_display, outputs=pagination_component)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `pagination`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["pagination"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["pagination"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, str | None: Returns a namespace object representing the pagination state.


 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "pagination-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          pagination: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
