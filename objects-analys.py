from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

subscription_key = "b632d5855ee04ebf8d9ed06ec02688b6"
endpoint = "https://20221101image.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def get_tags(filepath):
    local_image = open(filepath, "rb")

    tags_result = computervision_client.tag_image_in_stream(local_image)

    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
        
    return tags_name


def detect_objects(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)

    objects = detect_objects_results.objects
    
    return objects




st.title('物体分析アプリ')

upload = st.file_uploader('choose image:', type=['jpg','png'])

if upload is not None:
    img = Image.open(upload)

    ##読みこんだ画像ファイルをimgフォルダに格納する
    img_path = f'img/{upload.name}'
    st.image(img)

    ##格納した画像ファイルを保存する
    img.save(img_path)

    objects = detect_objects(img_path)

    #描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h

        caption = object.object_property

        font = ImageFont.truetype(font='./Helvetica.ttf',size=50)

        text_w,text_h = draw.textsize(caption, font = font)
        draw.rectangle([(x,y), (x+w,y+h)], fill=None, outline='red',width=5)
        draw.rectangle([(x,y), (x+text_w,y+text_h)], fill='red')
        draw.text((x,y), caption, fill = 'white', font = font)
        
    st.image(img)

    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)

    st.markdown('**認識された物体**')
    st.markdown(f'>{tags_name}')
