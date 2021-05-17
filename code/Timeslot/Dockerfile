#we are using alpine (a simple Linux Kernel) as our base container
From alpine:latest

#Install python and pip
RUN apk add --no-cache py-pip
RUN pip3 install --upgrade pip

#Copy the package files to the container and then move into the directory
COPY ./timeslot_app /service
WORKDIR /service

#Install requirements
RUN pip3 install -r requirements.txt

#open port 5000 for external communication
EXPOSE 5000

#run our service
WORKDIR /service/timeslot
ENTRYPOINT ["python3"]
CMD ["__init__.py"]