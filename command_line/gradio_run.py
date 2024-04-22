import gradio as gr
import steganography as steg

def encode(img, msg, key):
    img, key_res = steg.encode_img(img, msg, key)
    return img, key_res

def decode(img, key):
    return steg.decode_img(img, key)

def generate_key():
    return steg.AES_key_generate().decode("utf-8")

with gr.Blocks() as demo:   
    with gr.Tab("Encode"):
        with gr.Row():
            with gr.Column():
                im_inp = gr.Image(label="Image")
                msg = gr.Textbox(placeholder="Message",label="Input")
                key = gr.Textbox(placeholder="Key",label="Key")
                genkey_btn = gr.Button("Generate Key")
                
            out_img = gr.Image(label="Output")
        btn = gr.Button("Encode")
        btn.click(fn=encode, inputs=[im_inp,msg,key], outputs=[out_img,key])
        genkey_btn.click(fn=generate_key, outputs=[key])
    with gr.Tab("Decode"):
        im_out = gr.Image(label="Output")
        key = gr.Textbox(placeholder="Key",label="Key")
        msg_out = gr.Textbox(label="Output")
        btn = gr.Button("Decode")
        btn.click(fn=decode, inputs=[im_out,key], outputs=[msg_out])

demo.launch()
