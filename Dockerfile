FROM python:3.8

WORKDIR /opt/portscanner

# ENTRYPOINT ["/bin/bash"]
# CMD ["/bin/bash", "sleep", "60"]
CMD ["sleep", "600"]
# # copy the dependencies file to the working directory
# COPY requirements.txt .

# # install dependencies
# RUN pip install -r requirements.txt

# # copy the content of the local src directory to the working directory
# COPY src/ .

# # command to run on container start
# CMD [ "python", "./server.py" ]

