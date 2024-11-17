# junction2024
Junction2024


This project is the result of the 48 hours work of the team of five
at the [Junction 2024](https://www.hackjunction.com/). We have tackled a real-world problem provided by Peikko [Peikko Group](https://www.peikko.com/). Our tool enables users to specify elements of interest and then identifies the connections required in construction. It accurately detects the number of connections and the types of materials being connected, presenting the results in an organized table format. Additionally, we developed efficient C++ code capable of filtering IFC files, extracting only relevant elements, and generating a smaller, refined IFC file as a result.
For a detailed description, ideas and further insights into our tool, check out the video here:
See https://www.youtube.com/watch?v=nMjBj4VQUX4&t=9s for the tool discribtion and ideas.


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


# Acknowledge
Huge thanks to Peikko Peikko Group Corporation for the interesting challeng and for giving us the opportunity to innovate in such an impactful field and to Markus Tuuri Sampo Pilli-Sihvola for engaging discussions.
A big shout-out to the organizers of Junction 2024 
for creating an incredible environment that fosters collaboration and creativity!




