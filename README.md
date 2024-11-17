# junction2024
Junction2024


## 1. Clone the GitHub Repository

Navigate to the directory where you want to clone the project:

```bash
cd /path/to/your/directory
git clone https://github.com/dnapi/junction2024
```

Navigate into the cloned repository directory:

```bash
cd  junction2024
```

## 2 Set Up and Run the FastAPI Backend
```bash
cd back
```

Create and activate a virtual environment:
```bash
python3 -m venv venv
```
For Windows use
```bash
source venv/bin/activate 
```

Install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Here, main:app refers to the file and FastAPI instance. Replace main with your specific filename if it differs.
FastAPI will be available at: http://127.0.0.1:8000

## Set Up and Run the Vite React Frontend
Open a new terminal and navigate to the frontend directory 
```bash
cd ../frontend/beamrx-frontend
```
Install the necessary dependencies:
```bash
npm install
```
Run Vite in development mode:

```bash
npm run dev
```
The frontend will be available at the URL provided by Vite, typically http://127.0.0.1:5173.




