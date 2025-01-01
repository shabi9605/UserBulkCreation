# **Project Setup**

## **Prerequisites**

### **Docker Setup**
1. Ensure Docker is installed on your system.
2. Clone this project and navigate to the location of the `manage.py` file.


### **Without Docker**
1. Ensure Python version **3.12** is installed on your system.
2. Install `pipenv` by running:
   ```bash
   pip install pipenv
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
4. Install project dependencies:
   ```bash
   pipenv install
   ```

### **Additional Requirements**
- **Redis**: Required for Celery.
  - Redis can be installed using WSL (Windows Subsystem for Linux) or Ubuntu.
- **Celery**: Used for asynchronous task processing.

## **Running the Project**

### **Using Docker**
1. Build and start the Docker containers:
   ```bash
   docker compose up --build -d
   ```
2. Apply database migrations:
   ```bash
   docker compose exec server python manage.py migrate
   ```
3. Access the application at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **Without Docker**
1. Start Redis:
   - On WSL/Ubuntu, ensure Redis is running.
2. Start Celery:
   ```bash
   celery -A proj worker -l INFO
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

## **Accessing the Application**
- Default URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

Feel free to customize the `.env` file and database configurations as per your requirements.
