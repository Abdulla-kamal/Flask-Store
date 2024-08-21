
### Steps to Run the Flask Project Without Installing Flask Globally In Your Device:

1. **Navigate to Your Project Directory**:
   ```bash
   cd /path/to/your/flask/project
   ```

2. **Create a Virtual Environment**:
   This step ensures that all dependencies, including Flask, are installed locally within the project and not system-wide.
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Flask Locally**:
   If Flask is not already listed in your `requirements.txt`, you can install it in the virtual environment:
   ```bash
   pip install flask
   ```
   Or, if you have a `requirements.txt` file, you can install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set the `FLASK_APP` Environment Variable**:
   - On **Windows** (Command Prompt):
     ```bash
     set FLASK_APP=app.py
     ```
   - On **Windows** (PowerShell):
     ```bash
     $env:FLASK_APP="app.py"
     ```
   - On **macOS/Linux**:
     ```bash
     export FLASK_APP=app.py
     ```

6. **Run Your Flask Project**:
   Once Flask is installed in the virtual environment and the environment variable is set, you can start the Flask server:
   ```bash
   flask run
   ```

This will launch the Flask application locally, accessible via `http://127.0.0.1:5000/`.
