import os
from flask import Flask, render_template, request, redirect
from google import genai
from google.genai import types

app = Flask(__name__)

PROJECT_ID = "ai-note-summarizer-491416"

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location = "us-central1" 
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def generate(text, model, additional_prompt):

    if not additional_prompt:
        additional_prompt = "Summarize the following notes clearly."

    contents = [
        types.Part.from_text(
            text=f"{additional_prompt}\n{text}"
        )
    ]

    response = client.models.generate_content(
        model=model,
        contents=contents,
    )

    return response.text



@app.route('/summarize', methods=['GET', 'POST'])
def summarize():

    if request.method == 'POST':
        text = request.form['text']
        model = request.form['model']
        additional_prompt = request.form['additional_prompt']

        try:
            summary = generate(text, model, additional_prompt)


            return render_template('index.html', result=summary)

        except ValueError as e:
            return str(e)

    else:
        return redirect('/')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
