
import gradio as gr
from app import demo as app
import os

_docs = {'NeoViewer': {'description': 'Creates a file component that allows uploading one or more generic files (when used as an input) or displaying generic files or URLs for download (as output).\n\n    Demo: zip_files, zip_to_json', 'members': {'__init__': {'value': {'type': 'str | list[str] | Callable | None', 'default': 'None', 'description': 'Default file(s) to display, given as a str file path or URL, or a list of str file paths / URLs. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'Timer | float | None', 'default': 'None', 'description': 'Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.'}, 'inputs': {'type': 'Component | Sequence[Component] | set[Component] | None', 'default': 'None', 'description': 'Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'height': {'type': 'int | float | None', 'default': 'None', 'description': 'The default height of the file component when no files have been uploaded, or the maximum height of the file component when files are present. Specified in pixels if a number is passed, or in CSS units if a string is passed. If more files are uploaded than can fit in the height, a scrollbar will appear.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will allow users to upload a file; if False, can only be used to display files. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'index_of_file_to_show': {'type': 'int', 'default': '0', 'description': 'int = 0, # index of file to show in case of multiple files'}, 'max_size': {'type': 'int', 'default': '5000000', 'description': 'maximum size of file to show in bytes'}, 'max_pages': {'type': 'int', 'default': '100', 'description': 'maximum number of pages of file to show'}, 'ms_files': {'type': 'bool', 'default': 'True', 'description': 'if True, will convert MS files to PDF for display, but it is a long process. Unactive if libre_office is False'}, 'libre_office': {'type': 'bool', 'default': 'True', 'description': 'if True, means that LibreOffice is installed and can be used to convert MS files to PDF'}}, 'postprocess': {'value': {'type': 'str | list[str] | None', 'description': 'Expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.'}}, 'preprocess': {'return': {'type': 'str | list[str] | None', 'description': 'Passes the file as a `str`object, or a list of `str`.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the NeoViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the NeoViewer. Uses event data gradio.SelectData to carry `value` referring to the label of the NeoViewer, and `selected` to refer to state of the NeoViewer. See EventData documentation on how to use this event data'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the NeoViewer using the clear button for the component.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the NeoViewer.'}, 'delete': {'type': None, 'default': None, 'description': 'This listener is triggered when the user deletes and item from the NeoViewer. Uses event data gradio.DeletedFileData to carry `value` referring to the file that was deleted as an instance of FileData. See EventData documentation on how to use this event data'}, 'download': {'type': None, 'default': None, 'description': 'This listener is triggered when the user downloads a file from the NeoViewer. Uses event data gradio.DownloadData to carry information about the downloaded file as a FileData object. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'NeoViewer': []}}}

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
# `gradio_neoviewer`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_neoviewer
```

## Usage

```python
import gradio as gr
from gradio_neoviewer import NeoViewer


def set_interface():
    print("Setting interface")
    view_with_ms = NeoViewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
            "./demo/data/viewer.py",
        ],
        elem_classes=["visualisation"],
        index_of_file_to_show=0,
        height=300,
        visible=True,
        ms_files=True,
    )

    view_without_ms = NeoViewer(
        value=[
            "./demo/data/Le_Petit_Chaperon_Rouge_Modifie.docx",
            "./demo/data/mermaid_graph-2.html",
            "./demo/data/graphique_couts_annuels.png",
            "./demo/data/Le_Petit_Chaperon_Rouge.zouzou",
        ],
        elem_classes=["visualisation"],
        index_of_file_to_show=1,
        height=300,
        visible=True,
        ms_files=False,
    )
    empty_view1 = view_with_ms
    empty_view2 = view_without_ms
    return view_with_ms, view_without_ms, empty_view1, empty_view2


with gr.Blocks() as demo:
    with gr.Row():
        view_with_ms = NeoViewer(visible=False)
        view_without_ms = NeoViewer(visible=False)
        empty_view1 = NeoViewer(visible=False)
        empty_view2 = NeoViewer(visible=False)
    demo.load(
        set_interface,
        outputs=[view_with_ms, view_without_ms, empty_view1, empty_view2],
    ).then(
        fn=lambda: (
            NeoViewer(visible=False, value=None, elem_id="empty1"),
            NeoViewer(visible=False, value=[], elem_id="empty2"),
        ),
        outputs=[empty_view1, empty_view2],
    )

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `NeoViewer`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["NeoViewer"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["NeoViewer"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the file as a `str`object, or a list of `str`.
- **As output:** Should return, expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.

 ```python
def predict(
    value: str | list[str] | None
) -> str | list[str] | None:
    return value
```
""", elem_classes=["md-custom", "NeoViewer-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          NeoViewer: [], };
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
