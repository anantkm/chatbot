docker build -t dentist_service .
docker run -p 127.0.0.1:5001:5000 -t dentist_service __init__.py

