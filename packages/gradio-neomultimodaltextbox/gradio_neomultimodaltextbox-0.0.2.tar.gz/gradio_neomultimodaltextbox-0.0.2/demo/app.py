import gradio as gr
from gradio_neomultimodaltextbox import NeoMultimodalTextbox


example = NeoMultimodalTextbox().example_value()


def identity(i):
    return i


with gr.Blocks() as demo:
    box1 = NeoMultimodalTextbox(
        file_count="multiple",
        value={"text": "zouzou", "files": []},
        interactive=False,
    )  # interactive version of your component
    box2 = NeoMultimodalTextbox(
        upload_btn=False, interactive=False, stop_btn=True
    )  # static version of your component
    box1.submit(fn=identity, inputs=box1, outputs=box2)

if __name__ == "__main__":
    demo.launch()
