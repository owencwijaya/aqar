# aqar

Repository for our project Automated QA Runner (AQAR) for Korika Student Mentorship programme, Spring 2024.

## How to Install

1. Clone this repository to your computer
2. Create a virtual environment
3. Activate the virtual environment and install the requirements (`pip install -r requirements.txt`)
4. Open the `gpt/app` folder, update the environment variable `GROQ_API_KEY` with your own Groq API key

## How to Run

1. Ensure you have BlueStacks and PUBG MOBILE installed in your computer
2. Open the PUBG MOBILE game, ensure it's running in the window titled "BlueStacks App Player"
3. Once you get inside the lobby, select the option "Training Ground"
4. Once you're inside the training ground, run the backend server by running:

   ```
   cd gpt/app
   python server.py // ensure venv is activated
   ```
5. Run the main script with the command `python main.py`
