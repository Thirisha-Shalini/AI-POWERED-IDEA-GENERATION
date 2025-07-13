# ✍️ InspireWrite - AI-Powered Creative Writing Generator

Welcome to **InspireWrite**, an AI-enhanced creative writing tool that helps users unleash their imagination through stories, poems, and dialogues — all generated from a single prompt.

## 🌟 Features

- 🔮 Generate **Stories**, **Poems**, or **Dialogues** from your prompt
- 🧠 Uses HuggingFace API or fallback template-based generation
- 💡 Suggested creative prompts for quick inspiration
- ✨ Beautiful, responsive UI with animations
- 📋 Copy generated content with one click
- 🔄 Real-time status check of the backend

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/inspirewrite.git
cd inspirewrite
2. Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
3. Install dependencies

pip install -r requirements.txt
4. Set up HuggingFace API token (optional)
Create a .env file in the root directory:


HF_TOKEN=your_huggingface_api_token
Or set it via terminal before running the app:


export HF_TOKEN=your_huggingface_api_token
5. Run the application

python app.py
Then open your browser at:
🌐 http://127.0.0.1:5000

🧠 API Endpoints
Method	Endpoint	Description
GET	/	Loads the creative writing interface
GET	/health	Server health/status check
POST	/generate	JSON input → creative text output

Sample POST payload:

{
  "prompt": "A library where books rewrite themselves",
  "category": "story"
}
📁 Project Structure

inspirewrite/
├── app.py                # Flask app
├── templates/
│   └── index.html        # Main HTML file
├── static/               # CSS/JS (optional)
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── .env                  # Optional token config
💡 Example Prompts
A library where books rewrite themselves

The last person on Earth finds a radio signal

Colors that exist only in dreams

A conversation with your future self

The sound of forgotten memories

📜 License
This project is licensed under the MIT License.

🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/YourFeature)

Commit your changes (git commit -m 'Add new feature')

Push to the branch (git push origin feature/YourFeature)

Open a Pull Request

Made with ❤️ to help you imagine more.

yaml
Copy
Edit

---

Let me know if you want a `requirements.txt`, `.gitignore`, or GitHub Actions CI workflow file to go with it!






