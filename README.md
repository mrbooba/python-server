# Event Manager

## Description
This is a Python server and its CLI client to manage events.
This application is based 


- FastAPI server for event CRUD (MongoDB)
- Python CLI client
- HTML/JS web interface
- Automated testing

## Installation & Deployment

### Prerequisites
- Docker and Docker Compose

### Build the image and launch the application

\`\`\`
docker-compose up -d --build
\`\`\`

The API is available at [http://localhost:8000]


### Stop and delete the docker application
\`\`\`
docker-compose down
\`\`\`

### Use CLI client on command line

\`\`\`
pip install requests
python cli/client.py add --start 1717000000 --tags meeting urgent
python cli/client.py list
python cli/client.py remove --tags meeting
\`\`\`

### Run tests

\`\`\`
pip install pytest
pytest test/test_app.py

or from docker

docker-compose run --rm test
\`\`\`




