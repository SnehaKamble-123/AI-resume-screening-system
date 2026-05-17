from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['resume']

    if file.filename == '':
        return "No file selected"

    if not file.filename.endswith('.pdf'):
        return "Please upload PDF file only"

    try:
        pdf_reader = PyPDF2.PdfReader(file)

        text = ""

        for page in pdf_reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

        skills_list = [
            'Python',
            'Java',
            'C++',
            'HTML',
            'CSS',
            'JavaScript',
            'React.js',
            'MySQL',
            'Django',
            'Flask'
        ]

        found_skills = []

        for skill in skills_list:
            if skill.lower() in text.lower():
                found_skills.append(skill)

        score = len(found_skills) * 10

        email = re.findall(r'[\w\.-]+@[\w\.-]+', text)

        phone = re.findall(r'\d{10}', text)

        return f"""
        <h1>AI Resume Screening Result</h1>

        <h3>Email:</h3>
        {email}

        <h3>Phone:</h3>
        {phone}

        <h3>Skills Found:</h3>
        {found_skills}

        <h3>Resume Score:</h3>
        {score}
        """

    except:
        return "Error reading PDF. Please upload valid PDF resume."


if __name__ == '__main__':
    app.run(debug=True)