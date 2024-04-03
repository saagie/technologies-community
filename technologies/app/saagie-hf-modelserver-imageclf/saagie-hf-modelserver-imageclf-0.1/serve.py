#%% Dependencies
import os
import logging
import numpy as np
import pandas as pd
import torch
import ast
from datetime import datetime

from flask import Flask, jsonify, request
from flask import current_app, abort, Response
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

## Logger, App, Device config
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from transformers import AutoModelForImageClassification, ImageClassificationPipeline
from transformers import pipeline

## Image Processing
from PIL import Image
import io
import re
import base64




#%% App Layout
# Dash with Responsive UI
app = dash.Dash(__name__
                , meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}] 
                , external_stylesheets=[dbc.themes.BOOTSTRAP]#)
                , url_base_pathname=os.environ["SAAGIE_BASE_PATH"]+"/"
                )
## Flask Server
server = app.server


## Layout Params
base_height = 200
btn_color = "primary"
border_color = "#D9DBE3"
border_radius = 6
btn_style = {"height": 40, "width": 100, "border-radius":border_radius}
layout_col_width = 5
bg_color = 'white'
text_color = '#263D5C' 
text_color2 = '#7B899B'
banner_color = '#1F3046'
padding_style = {'margin-left' : '30px', 'margin-top' : '30px', 'background-color': bg_color, 'color': text_color}
text_area_style = {'height': '20%', 'width': '100%', 'border-color': border_color, 'margin-bottom' : '18px'}

desc = "Custom Saagie app that deploys the deep learning image classification models from HuggingFace avnd makes predictions via the GUI.  \n\n\n\n"
## Model For Testing
model = "google/vit-base-patch16-224"

## Layout
app.layout = dbc.Container(fluid=True,children=[
    ## Title
    dbc.Row([
        dbc.Col([html.H2("Saagie HuggingFace Model Server - Image CLF"),], width = 10),
        dbc.Col([
            html.H4("🛈", title=desc)
            ], width = 2)
        ]
    , style={'background-color': banner_color, 'color':  'white', 'margin-bottom' : '10px', 'padding-top': '40px', 'padding-left': '60px', 'padding-bottom': '40px'}
    ),
    
    ## Main App
    dbc.Col([
        dbc.Row([
            ## Left part: deployment
            dbc.Col([
                ## Model and label for the deployment
                html.H6("Model Name"),                 
                dcc.Textarea(id='modeldir'
                    , value= 'Enter the HuggingFace model repository, e.g. \n'+model
                    , style=text_area_style
                    ), 
                
                ## Deploy button
                dbc.Row(dbc.Button("Deploy"
                    , id="deploy"
                    , n_clicks=0
                    , size='sm'
                    , style={"height": 40, "width": 100, "color": "#132d81", "background-color": "#cef0fd", 'border-color': "White", "border-radius":border_radius, 'margin-bottom' : '27px'})
                    , justify="center"
                    ),
                ## Deploy loading icon
                dbc.Row(dcc.Loading(id="loading"
                    , type="circle"
                    , children='Loading Model'
                    , color="#132d81")
                    , justify="center"
                    ),
                html.P(id='placeholder', children=''), 
            ]
            , width=layout_col_width 
            , style={'margin-left' : '60px', 'margin-top' : '30px', 'background-color': bg_color, 'color': text_color, "border-right": "1px solid #d9dbe3", "padding-right": "4%"}
            ),

            ## Right part: Inference
            dbc.Col([                
                ## Image-Input
                html.H6("Upload File"), 
                dcc.Upload(id='upload-image',
                    children=html.Div(['Drag and Drop for Adding Images']),
                    style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin-bottom': '18px'},
                    multiple=True
                ),
                ## Images Preview
                dbc.Carousel(id='carousel', items=[], controls=True, indicators=True, interval=3000,
                             style={'width': '100%', 'height': '300px', 'overflow': 'hidden', 'margin-bottom' : '8px'}
                             ),                
                dbc.Row([
                    dbc.Col(html.Span("Valid format: .jpeg"), width={"size": 6, "offset": 0}),
                    dbc.Col(html.Span(id='upload-count', children="0 uploaded images"), width={"size": 6, "offset": 0}, style={'textAlign': 'right'})
                    ], style={'width': '100%', 'margin': '18px 0', 'color' : text_color2}
                    ),
                ## Inference button
                dbc.Row(dbc.Button("Predict", id="predict", n_clicks=0, size='sm', color=btn_color, style=btn_style), justify="center", 
                        style={'margin-bottom' : '8px'}
                        ),
                ## Predictions
                html.H6("Inference Results"), 
                dcc.Textarea(id='pred_out'
                    , value='Predictions'
                    , style = {'height': '25%', 'display': 'block', 'border-color': border_color, 'width': '100%', 'background-color' : 'white', 'color' : "#587193"}
                    ),
                html.H5("")
                ]
                , width=layout_col_width 
                , style=padding_style
                ),
            ]),
            ## padding bottom space
            dbc.Row([html.H6('.  ')], style = {'color': bg_color}), 
        ])
    ], style = {'background-color': bg_color, 'color': text_color}
    )
    
  


#%% App functions
device = "cpu"
uploaded_names = []
uploaded_images = []


## utils
def format_predictions(preds, uploaded_names):
    formatted_output = ""
    for i, prediction in enumerate(preds):
        formatted_output += f"{i + 1}. \"{uploaded_names[i]}\":\n"
        print(prediction)
        for item in prediction[:3]:
            score = item['score'] * 100
            label = item['label']
            formatted_output += f"{score:.1f}% : {label}  \t  "
        formatted_output += "\n\n"
    return formatted_output


def base64_to_pil(img_base64):
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    return pil_image


def pipeline_predict(input_texts: list, pipeline):
    return pipeline(input_texts)


def list_to_string(l: list):
    # print(l)
    return '\n'.join([', '.join(["%s: %s"%(k,v) if type(v) == str else "%s: %.4f"%(k,v) for k, v in item.items()]) for item in l])


def parse_contents(contents):
    return html.Div([
        html.Img(src=contents, style={'maxWidth': '100%', 'height': '60px'}),
        html.Hr(),
    ])


def resize_image(image, max_size=288):
    """
    Resize the image to ensure its maximum dimension is no greater than max_size,
    maintaining the aspect ratio.
    """
    if max(image.size) > max_size:
        scale = max_size / max(image.size)
        new_size = tuple([int(x*scale) for x in image.size])
        return image.resize(new_size, Image.ANTIALIAS)
    return image



## Processing uploaded Images
@app.callback(
    [Output('carousel', 'items'),
    Output('upload-count', 'children')],
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename'),
    State('carousel', 'items')]
)
def update_output(uploaded_contents, uploaded_filenames, existing_items):
    ## If using global variable lists, the historical images will be saved, 
    ## otherwise, with the following three inits, they will be deleted
    global uploaded_names, uploaded_images  
    uploaded_names = []
    uploaded_images = []
    existing_items = []
    if uploaded_contents is not None:
        for content, name in zip(uploaded_contents, uploaded_filenames):
            content_type, content_string = content.split(',')
            
            # Base64 to PIL image
            decoded_image = base64.b64decode(content_string)
            image = Image.open(io.BytesIO(decoded_image))
            uploaded_names.append(name)
            uploaded_images.append(image)
            
            # back to Base64 for Carousel
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode()
            item = {
                'key': name,
                'src': f'data:image/jpeg;base64,{encoded_image}'
            }
            existing_items.append(item)
    upload_count_text = f"{len(uploaded_images)} uploaded images" if uploaded_images else ""
    return existing_items, upload_count_text


## Predict
@app.callback(
    Output(component_id = 'pred_out', component_property = 'value'),
    [Input(component_id = 'predict', component_property = 'n_clicks')],
)
def predict(click):
    logger.info('-- PREDICT function called --')
    if click and len(uploaded_images)>0:
        global classifier
        preds = []
        for img in uploaded_images:
            print(uploaded_images)
            # img_resized = resize_image(img) ## Back up a smaller size of image if needed
            preds.append(classifier(img))
        formatted_preds = format_predictions(preds, uploaded_names)
        return formatted_preds
    else: 
        return ' '


## Deploy a model
@app.callback(
    Output(component_id = 'loading', component_property = 'children'),
    [Input(component_id = 'deploy', component_property = 'n_clicks')],
    [State(component_id = 'modeldir', component_property = 'value')],
)
def deploy(click, model_tag):
    if click:
        logger.info('-- DEPLOY function called --')
        try:
            global classifier            
            print('|||||||||||||||||||||')
            print(model_tag)
            classifier = pipeline("image-classification", model=model_tag)
            logger.info('-- Pipeline Deployed--')
            logger.info(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+model_tag)
            return model_tag+' is deployed.'
        except Exception as err:
            return model_tag+' is not deployed due to ' + str(err)
    else:
        return ''


@server.route('/deploy', methods=['POST'])
def deploy_api():
    # Read inputs/classes or Return reason of abort
    print(vars(request))
    if 'model_dir' in request.json:
        model_tag = request.json['model_dir']
        if ':' in model_tag:
            model_name = model_tag.split(':')[0]
            model_ver = model_tag.split(':')[1]
        else:
            model_name = model_tag
            model_ver = "main"
    else:
        abort(Response('Json not understandable, make sure that you have "model_dir" and "label" key.'))
    logger.info('-- DEPLOY API called --')
    try:
        ## make deployments via API
        global classifier            
        print('|||||||||||||||||||||')
        print(model_tag)
        classifier = pipeline("image-classification", model=model_tag)
        logger.info('-- Pipeline Deployed--')
        logger.info(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+model_name+':'+model_ver)
        return jsonify({'response': model_name+':'+model_ver+' is deployed.'}), 201
    except Exception as err:
        return jsonify({'response': model_name+':'+model_ver+' is not deployed due to ' + str(err)}), 501


@server.route('/predict', methods=['POST'])
def predict_api():
    # Read inputs/classes or Return reason of abort
    logger.info('-- PREDICT API called --')
    # Get the image file from the request
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    resized_image = resize_image(image)    
    # Perform classification
    prediction = classifier(resized_image)
    formatted_output = ''
    for item in prediction[:3]:
        score = item['score'] * 100
        label = item['label']
        formatted_output += f"{score:.1f}% : {label}  \t  "
    formatted_output += "\n"
    # Return the prediction as JSON
    return jsonify(prediction), 201

    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False, port=8080, dev_tools_hot_reload=True)