import anthropic
import mss
import speech_recognition as sr
from PIL import Image
import io
import base64
import time
import sys
import os
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

ASSISTANT_NAME = "alex"

# Load environment variables from a .env file
load_dotenv()

# Set up Anthropic API key from environment variable
anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')
if not anthropic.api_key:
    print("[bold red]Error: ANTHROPIC_API_KEY environment variable not set.[/bold red]")
    sys.exit(1)

claude = anthropic.Anthropic(api_key=anthropic.api_key)

# Set up speech recognition
recognizer = sr.Recognizer()

def listen():
    """
    Listens to the user's speech and converts it to text using Google Speech Recognition API.

    Returns:
        str: The recognized text if successful, otherwise None.
    """
    with sr.Microphone() as source:
        print("[bold green]Alex is ready to help...[/bold green]")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"[bold blue]User said:[/bold blue] {command}")
        return command
    except sr.UnknownValueError:
        print("[bold red]Sorry, I did not understand that.[/bold red]")
        return None

def capture_screen():
    """
    Captures the current screen and returns the image bytes.

    Returns:
        BytesIO: A BytesIO object containing the screenshot in PNG format.
    """
    print("[bold magenta]Capturing Screen[/bold magenta]")
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

def analyze_screen(image_bytes):
    """
    Converts the image bytes to a base64 encoded string.

    Args:
        image_bytes (BytesIO): The image bytes.

    Returns:
        str: The base64 encoded string of the image.
    """
    print("[bold magenta]Analyzing Image[/bold magenta]")
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
    return image_base64

def load_context(file_path):
    """
    Loads the context from a file.

    Args:
        file_path (str): The path to the context file.

    Returns:
        str: The content of the context file.
    """
    with open(file_path, 'r') as file:
        context = file.read()
    return context

def query_anthropic(prompt, image_base64, 
                    model="claude-3-haiku-20240307", 
                    image_media_type="image/png", 
                    max_tokens=200,
                    temperature=0):
    """
    Queries the Anthropic API with a prompt and an image.

    Args:
        prompt (str): The text prompt to send to the API.
        image_base64 (str): The base64 encoded image string.
        model (str): The model to use for the query.
        image_media_type (str): The media type of the image.
        max_tokens (int): The maximum number of tokens in the response from the model.
        temperature (float): The temperature of the response from the model.

    Returns:
        str: The response from the API.
    """
    print(f"[bold cyan]Querying {model}[/bold cyan]")

    console = Console()
    response = ""

    with claude.messages.stream(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system="You are a helpful assistant AI, with the goal to help the user become a world class academic grant writer",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    ) as stream:
        for i, text in enumerate(stream.text_stream):
            response += text
            markdown = Markdown(response)
            console.clear()
            console.print(markdown)

    return response

def main():
    """
    Main function to execute the screen capture, speech recognition, and AI querying process.
    """
    context = load_context('./context/cssi.txt')
    while True:
        command = listen()
        if command:
            if ASSISTANT_NAME in command.lower():
                image_bytes = capture_screen()
                image_base64 = analyze_screen(image_bytes)
                prompt = f"""
                    User is working on a scientific proposal for the National Science Foundation 
                    on topics of search and discovery of distributed scientific research data.
                    The context of the grant is as follows in what is defined as the program solicitation 
                    or sometimes referred to as a call:
                    <program solicitation>
                    <call>
                    {context}
                    </call>
                    </program solicitation>
                    As an expert, provide feedback on the text, and propose text changes or ways 
                    to strengthen the proposal. If the user has specific questions about the call, 
                    answer based on the context provided in <call> above. Be succinct and helpful.

                    Your response should be in markdown if formatting would help your reply. 

                    The user's question is: {command}
                """

                ai_response = query_anthropic(prompt, image_base64)
                time.sleep(2)

if __name__ == "__main__":
    main()
