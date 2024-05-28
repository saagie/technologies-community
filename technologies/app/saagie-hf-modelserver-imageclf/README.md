# Saagie-HF-ModelServer-ImageCLF


## Description
Saagie-HF-ModelServer-ImageCLF: Custom app based on Dash/Flask that deploys the deep learning models from HuggingFace and makes predictions via the GUI or API. 


## How to use
To deploy the app: you need to create the app with port `8080` exposed, `Base path variable:SAAGIE_BASE_PATH`, don't select `Use rewrite url` and set the port access as `PROJECT`. 

Once the app is up, you can open the page of port 8080, enter a model for image classification on Hugging Face in `Model Name` on the left, then click `Deploy`.

When the model is successfully deployed, you can upload the images to be predicted in `Upload File` on the right side. Then click `Predict` to get the predicted results.

> An example is: 
> 
> Model Name:google/vit-base-patch16-224
> 
> (With a photo "otter.jpg" of a sea otter being uploaded)
> 
> Inference Results: 1. "otter.jpg": 97.7% :  	  otter  	  1.2% : weasel  	  0.3% : mink  	  


You can use the API with the following python sample code. 

1. Save the following code into a file named "__main__.py" and compress it into a zip along with multiple .jpeg images to predict.

2. Run it in your Project on the Saagie platform, your App's url needs to be stored as an environment variable with the name "APP_SHF_IMGCLF".

``` python
import os
import requests

################################
#%% Deployment
url = os.environ['APP_SHF_IMGCLF']

headers = {
    "Accept": "application/json",
    "Content-type": "application/json"
}


payload = {
    'model_dir': 'google/vit-base-patch16-224'
}

response = requests.post(url+'/deploy', headers=headers, json=payload)

print(response.text)


################################
#%% Prediction
def send_image(filename, url):
    # Open the image file
    with open(filename, 'rb') as file:
        # Prepare the data to be sent
        files = {'image': file}
        # Send the POST request to the server
        response = requests.post(url, files=files)
        # Print the server's response
        print(filename)
        print(response.text)

if __name__ == '__main__':
    # Image file to be sent
    for image_file in os.listdir():
        if image_file[-3:] == 'jpg':
            # Send the image to the server
            send_image(image_file, url+'/predict')
```