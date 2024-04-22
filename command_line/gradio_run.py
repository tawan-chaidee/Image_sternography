import gradio as gr
import steganography as steg

def encode(img, msg, key):
    img, key_res = steg.encode_img(img, msg, key)
    return img, key_res

def decode(img, key):
    return steg.decode_img(img, key)

def generate_key():
    return steg.AES_key_generate().decode("utf-8")

def fill_key(key):
    key = list(key)
    key_length = 44
    
    # Fill the key with "-"
    if len(key) < key_length:
        key += "-"*(key_length-len(key))
    else:
        key = key[:key_length]
        
    # Replace the last character with "="
    key[-1] = "="
    
    # Replace all spaces with "_"
    for i in range(len(key)):
        if key[i] == " ":
            key[i] = "_"
    
    return "".join(key)

with gr.Blocks() as demo:   
    with gr.Tab("Encode"):
        with gr.Row():
            with gr.Column():
                im_inp = gr.Image(label="Image")
                msg = gr.Textbox(placeholder="Message",label="Input")
                key = gr.Textbox(placeholder="Key",label="Key")
                with gr.Row():
                    genkey_btn = gr.Button("Generate Key")
                    fill_btn = gr.Button("Fill Key")
                
            out_img = gr.Image(label="Output")
        btn = gr.Button("Encode")
        btn.click(fn=encode, inputs=[im_inp,msg,key], outputs=[out_img,key])
        
        genkey_btn.click(fn=generate_key, outputs=[key])
        fill_btn.click(fn=fill_key, inputs=[key], outputs=[key])
    with gr.Tab("Decode"):
        im_out = gr.Image(label="Output")
        with gr.Blocks():
            with gr.Row(variant="default"):
                key = gr.Textbox(placeholder="Key",label="Key")
                fill_btn = gr.Button("Fill Key")
            msg_out = gr.Textbox(label="Output")
        btn = gr.Button("Decode")
        btn.click(fn=decode, inputs=[im_out,key], outputs=[msg_out])
        fill_btn.click(fn=fill_key, inputs=[key], outputs=[key])

demo.launch()
