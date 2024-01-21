FROM python:3.11-alpine3.19

# Install python dependencies
COPY ./requirements.txt /
RUN pip install -r requirements.txt \
 && rm /requirements.txt

# Copy app data
COPY . /app
WORKDIR /app

# Launch command
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
