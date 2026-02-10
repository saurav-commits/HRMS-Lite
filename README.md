HRMS-Lite
A simple Human Resource Management System (HRMS) built with Django & React
=========================================================================


LIVE URLS
---------

Backend (Django – Railway)
https://hrms-lite.up.railway.app

Frontend (React – Vercel)
https://hrms-lite-wrlp.vercel.app/attendance


PROJECT OVERVIEW
----------------

HRMS-Lite is a full-stack web application designed to manage HR-related
operations such as employee management, authentication, and internal
workflows.

This project is built as a monorepo with:

- Backend: Django (REST APIs)
- Frontend: React (Create React App)
- Deployment:
  - Backend hosted on Railway
  - Frontend hosted on Vercel


TECH STACK
----------

Backend:
- Python
- Django
- Gunicorn
- MongoDb (Railway)
- Whitenoise
- django-cors-headers

Frontend:
- React (Create React App)
- Axios
- React Router DOM

DevOps / Deployment:
- Railway
- Vercel
- GitHub


PROJECT STRUCTURE
-----------------

project-root/
│
├── backend/
│   ├── HRMS-Lite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── Procfile
│   ├── requirements.txt
│   └── venv/        (ignored)
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── package-lock.json
│
└── README.txt


ENVIRONMENT VARIABLES
---------------------

Backend (Railway):
Set these in Railway → Service → Variables

DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=auto-provided-by-railway


Frontend (Vercel):
Set these in Vercel → Project → Settings → Environment Variables

REACT_APP_API_BASE_URL=https://hrms-lite.up.railway.app


LOCAL DEVELOPMENT SETUP
-----------------------

Backend (Django):

cd backend
python -m venv venv
source venv/bin/activate        (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Backend runs at:
http://localhost:8000


Frontend (React):

cd frontend
npm install
npm start

Frontend runs at:
http://localhost:3000


CONNECTING FRONTEND TO BACKEND
------------------------------

Frontend API calls use the base URL from environment variables.

Example:

axios.get(
  process.env.API_BASE_URL + "/api/endpoint"
)


DEPLOYMENT SUMMARY
------------------

Backend (Railway):
- Root Directory: backend
- Gunicorn used via Procfile
- PostgreSQL plugin enabled
- Public networking enabled

Frontend (Vercel):
- Root Directory: frontend
- Framework: Create React App
- Build Command: npm run build
- Output Directory: build


HEALTH CHECK
------------

Django Admin:
GET /admin/


KEY LEARNINGS
-------------

- Monorepo deployment
- Environment variables in production
- Django and React integration
- Railway and Vercel deployment
- CORS handling


CONTRIBUTING
------------

This project is currently a learning and personal project.
Feel free to fork and experiment.


LICENSE
-------

MIT License


AUTHOR
------

Saurav Kumar
Backend / Full-Stack Developer
