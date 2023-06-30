import os
import weaviate
import base64
import json
from deepface import DeepFace

def populateVectorDatabase():
    class_obj = {
        'class': 'Celebrity',
        'properties': [
            {
                'name':'image',
                'dataType': ['blob']
            },
            {
                'name': 'text',
                'dataType': ['string']
            }
        ] 
    }
    client.schema.create_class(class_obj)
    for file_name in os.listdir("scraped-images"):
        img_path = os.path.join("scraped-images", file_name)
        img_file = open(img_path, "rb")
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
        img_file.close()
        try:
            vector = DeepFace.represent(img_path=img_path, model_name='Facenet')[0]["embedding"]
        except:
            print(f"couldn't find face in {file_name}")
            continue
        uuid = client.data_object.create(
            data_object={
                'image': b64_string,
                'name': 'Hi'
            }, 
            class_name='Celebrity',
            vector=vector
        )
        print(f"added {file_name} to vector database")

def queryVectorDatabase(img_path):
    vectorTest = DeepFace.represent(img_path=img_path, model_name='Facenet')[0]["embedding"]
    response = (
        client.query
        .get('Celebrity', 'image')
        .with_near_vector({
            "vector": vectorTest
        })
        .with_limit(1)
        .with_additional(["distance"])
        .do()
    )
    with open("response.json", "w") as outfile:
        json.dump(response, outfile)

client = weaviate.Client("http://localhost:8080")
#populateVectorDatabase()
queryVectorDatabase("test\dicaprio.jpg")