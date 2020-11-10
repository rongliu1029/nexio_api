FROM python:3.8-alpine 

# container 裡面的工作目錄
WORKDIR /code 
# Copy the current directory contents into the container at /app 
# ADD：將檔案加到 images 內
ADD . /code 
 
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
CMD ["python", "api.py"]
