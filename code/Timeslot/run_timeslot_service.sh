docker build -t timeslot_service .
docker run -p 127.0.0.1:5003:5000 -t timeslot_service __init__.py
