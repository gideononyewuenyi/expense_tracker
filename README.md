# expense_tracker

Personal Expense Tracker
This is a Django-based Personal Expense Tracker API, which allows users to manage their income and expenditures. The API uses Django Rest Framework for handling requests, and includes features such as user authentication, income and expenditure tracking.

Prerequisites
Before you start, you need to have the following installed:

Python 3.8+: 
pip: Python package installer (comes with Python)
PostgreSQL (or another database of choice) – make sure it's running if you're using it.
Virtual Environment (optional but recommended): 

Setup Instructions

1. Clone the Repository
First, clone the repository to your local machine:

git clone https://github.com/gideononyewuenyi/expense_tracker.git
cd expense-tracker

2. Set Up Virtual Environment
Create a virtual environment to manage dependencies:

# On macOS/Linux
python3 -m venv venv

# On Windows
python -m venv venv

Activate the virtual environment:

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate

3. Install Dependencies

With the virtual environment activated, install the required Python packages from requirements.txt:

pip install -r requirements.txt

4. Set Up the Database
If you're using PostgreSQL or another database, update the DATABASES settings in settings.py to match your local database configuration.

Run the migrations to set up your database schema:

python manage.py migrate

5. Create a Superuser
You can create an admin user to access the Django admin panel:

python manage.py createsuperuser
Follow the prompts to set up the username, email, and password.

6. Run the Development Server
Start the Django development server:

python manage.py runserver
The app will be available at http://127.0.0.1:8000/.

7. Testing the API
If you want to run the tests to ensure everything is set up correctly, use the following command:

python manage.py test

8. API Endpoints
Once the server is running, you can test the following API endpoints:

* POST /api/auth/signup: Create a new user (Sign Up)
* POST /api/auth/login: Login and obtain a token
* POST /api/auth/logout: Logout and invalidate the token
* GET /api/auth/user/{userID}/profile: Get user profile details
* POST /api/income-list: Create a new income entry
* GET /api/income-detail/{id}: Get details of an income entry
* POST /api/expenditure-list-create: Create a new expenditure entry
* GET /api/expenditure-detail/{id}: Get details of an expenditure entry

9. Additional Configuration
Authentication: The app uses Token-based authentication. Make sure to include the token in the header when making requests. For example:

curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/income-list/

10. Troubleshooting
If you encounter issues, check the console for error logs and make sure all dependencies are installed correctly.
If migrations fail, ensure that your database is set up correctly and that you're using the correct database settings.
