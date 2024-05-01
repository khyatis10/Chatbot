from chatResponse import getResponse
import gradio as gr
import time

theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="fuchsia",
)


def respond(message, chat_history):
    try:
        if message.lower() == 'bye':
            bot_message = "Q&A support: bye!"
        else:
            response = getResponse([message])
            bot_message = f"{response}"
        chat_history.append((message, bot_message))
    except Exception as e:
        bot_message = "Sorry, please try another question. I haven't caught up to this topic yet."
        chat_history.append((message, bot_message))
    finally:
        time.sleep(2)  # Simulating delay for bot response
        return "", chat_history


with gr.Blocks(theme='ostris/dark_modern') as demo:
    avatar_images = [
        "https://png.pngtree.com/background/20231024/original/pngtree-nerd-university-student-laughing-innocent-intelligent-student-photo-picture-image_5711694.jpg",
        # Avatar for the user
        "https://image-cdn.flowgpt.com/image-generation/97056bc12579eb9522519963670701af.png"]

    chatbot = gr.Chatbot(value=[[None,
                                 "Hi Professor Yang and Classmate!! Please ask me question on Data Science. However, I am only 1 day old. Don't ask hard question. I will try my best!!"]],
                         avatar_images=avatar_images, bubble_full_width=False)
    msg = gr.Textbox(label="Your Question:", placeholder="Ask me an academic question on Machine Learning!",
                     container=False, scale=7)
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()