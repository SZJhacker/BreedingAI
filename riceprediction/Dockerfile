# Use an official Python runtime as a parent image
FROM python:3.8.0

# Set the working directory to /gBreeder
WORKDIR /gBreeder

# Copy the current directory contents into the container at /app
COPY ./requirement.txt  /gBreeder/
SHELL ["/bin/bash","-c"]
# -- Install dependencies
ENV PIP_INDEX_URL https://mirrors.aliyun.com/pypi/simple/
RUN pip install --upgrade pip && pip install -r requirement.txt

CMD ["gunicorn", "-w", "5", "-t", "600", "-b", "0.0.0.0:5000", "riceprediction:app"]
