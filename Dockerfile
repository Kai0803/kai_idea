# use Python image 
FROM python:3.9

# set directory
WORKDIR /app

# copy Sdata.py
#COPY /home/kai/Sdata.py ./

# copy requirements.txt and install depend...
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy doc
COPY . .

# set container start command
#CMD ["python", "bybit_eth.py"]
CMD ["python", "bybit_eth.py"]
