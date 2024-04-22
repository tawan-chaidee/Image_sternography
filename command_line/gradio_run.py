import gradio as gr

def update(name):
    return f"Welcome to Gradio, {name}!"

with gr.Blocks() as demo:
    gr.Markdown("Start typing below and then click **Run** to see the output.")
    with gr.Row():
        mode = gr.Radio(["Encode", "Decode"], label="Mode")
        inp = gr.Textbox(placeholder="Message")
        out = gr.Textbox()
        inp2 = gr.Textbox()
        im = gr.File(label="Image")
    btn = gr.Button("Run")
    btn.click(fn=update, inputs=inp, outputs=out)

demo.launch()
