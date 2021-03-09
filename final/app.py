# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
import logging
import os
import pandas as pd

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision_v1


CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")


app = Flask(__name__)


@app.route("/")
def homepage():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind="final")
    image_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template("homepage.html", image_entities=image_entities)


@app.route("/upload_photo", methods=["GET", "POST"])
def upload_photo():
    photo = request.files["file"]

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(photo.read(), content_type=photo.content_type)

    # Make the blob publicly viewable.
    blob.make_public()

    # Create a Cloud Vision client.
    vision_client = vision_v1.ImageAnnotatorClient()

    # Use the Cloud Vision client to detect label annotations for our image.
    source_uri = "gs://{}/{}".format(CLOUD_STORAGE_BUCKET, blob.name)
    image = vision_v1.Image(source=vision_v1.ImageSource(gcs_image_uri=source_uri))
    image_info = vision_client.label_detection(image=image)
    image_desc = image_info.label_annotations
    
    #use pandas package to parse
    df = pd.DataFrame(columns=['description', 'score'])
    for desc in image_desc:
        df = df.append(
            dict(
                description=desc.description,
                score=desc.score
            ),
            ignore_index=True
        )
    # If an image is detected, save to datastore the description of image
     
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Fetch the current date / time.
    current_datetime = datetime.now()

    #iterte over our datafram to add descriptions and score
    #only show values over .85
    img = []
    score = []
    for index, row in df.iterrows():
        if row['score'] >= .85:
            img.append(row['description'])
            score.append(row['score'])
  

    # The kind for the new entity.
    kind = "final"

    # The name/ID for the new entity.
    name = blob.name

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, storage_public_url, timestamp, and joy.
    entity = datastore.Entity(key)
    entity["blob_name"] = blob.name
    entity["image_public_url"] = blob.public_url
    entity["timestamp"] = current_datetime
    entity["image_description"] = img
    entity["image_score"] = score

    # Save the new entity to Datastore.
    datastore_client.put(entity)

    # Redirect to the home page.
    return redirect("/")


@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=5000, debug=True)