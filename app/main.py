# -*- coding: utf-8 -*-
"""test_docker_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ah-Cc9rcEN6FRJigYEJ5rVSYFwT-znPS
"""

import uvicorn
from uvicorn import Config, Server
import fastapi
from fastapi import FastAPI, File, UploadFile
import pydantic
from pydantic import BaseModel# o validate the input and output of the RESTful API, we can define the schema in FastAPI with pydantic, which will be used to generate the OpenAPI docs and ReDoc automatically.

import PIL
from PIL import Image
#import io
#import pyngrok
#import nest_asyncio
#from pyngrok import ngrok
from fastapi.responses import HTMLResponse, StreamingResponse
import cv2
import numpy as np


#this is my ngrok account to see the final APP
#!ngrok config add-authtoken 2OvVxoK97Q4xGawagb7WKLJTQi8_4wEepnHMTPYUDAUSxcGnt

app = FastAPI(title='Deploying a ML Model with FastAP')


# Define class for image requests
#me: If a user passes something that is incorrect, a response is returned to the user letting them know that the request could not be processed due to a data validation error
class ImageRequest(BaseModel):
    file_name: str
    file_content: UploadFile




@app.get("/")  
async def main():
    """Create a basic home page to upload a file

    :return: HTML for homepage
    :rtype: HTMLResponse
    """

    content = """<body>
          <h3>Upload an image to get ....</h3>
          <form action="/predict" enctype="multipart/form-data" method="post">
              <input name="files" type="file" multiple>
              <input type="submit">
          </form>
      </body>
      """
    return HTMLResponse(content=content)






#1- async type:
# Define API endpoint for image classification
@app.post("/predict/")
async def predict(files: UploadFile = File(...)):  
        # # first, VALIDATE INPUT FILE
        # filename = file.filename
        # fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png")
        # if not fileExtension:
        #     raise HTTPException(status_code=415, detail="Unsupported file provided.")  
        image = await files.read()
        image = Image.open(io.BytesIO(image)).convert('RGB')
        image=np.array(image)# cv2 need np.array format
        cv2.circle(image,(50,50),20,(0,0,255), -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("cv_sil.jpg", image) #????cv2.imencode
        new_image=open("cv_sil.jpg",mode="rb")#read the image as a binary
        return StreamingResponse(new_image,media_type="image/jpeg") #send binay image to the site


# Start the app in normal deployment
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

