from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
import numpy as np
try:
    training_key  = os.environ['AZURE_KEY']
    ENDPOINT = os.environ['AZURE_ENDPOINT']
    projectid = os.environ['AZURE_PROJECTID']
    nameIter = os.environ['AZURE_NAME']
    ResourceId = os.environ['AZURE_RESOURCE_ID']
except:
    print("Please set the environment variables")
    exit(1)    

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
Ones = {
    "one0": [377, 175, 197, 111],
    "one1": [348, 155, 222, 117],
    "one2": [341, 167, 208, 83],
    "one3": [380, 163, 203, 105],
    "one4": [325, 180, 179, 132],
    "one5": [403, 160, 213, 122],
    "one6": [342, 156, 212, 117],
    "one7": [352, 154, 240, 127],
    "one8": [401, 185, 181, 91],
    "one9": [464, 202, 159, 82] ,   
    "one10": [345, 175, 179, 102],
    "one11": [388, 218, 181, 77],
    "one13": [535, 210, 182, 80],
    "one14": [347, 204, 179, 81],
    "one15": [431, 189, 179, 107],
   "one16": [402, 177, 207, 112],
  "one17": [451, 169, 180, 73],
    "one18": [431, 170, 197, 82],
    "one19": [387, 187, 197, 96],
    "one20": [317, 221, 147, 123],
}
Ones_tag = trainer.create_tag(projectid,"one")
# iteration_name = 'MyIteration'
# new_iter = trainer.update_iteration(projectid,"174a4e4d-2085-484c-8a15-2416d7cc9ff1", nameIter, is_default=True)
# print(Ones_tag)
base_image_location = os.path.join (os.path.dirname(__file__), "Data")
print ("Adding images...")
tagged_images_with_regions = []
for filename in Ones.keys():
    x,y,w,h = Ones[filename]
    regions = [ Region(tag_id=Ones_tag.id, left=x,top=y,width=w,height=h) ]
    with open(os.path.join (base_image_location, filename + ".jpg"), mode="rb") as image_contents:
        # tagged_images_with_regions.append(ImageFileCreateEntry(name=filename, contents=image_contents.read(), regions=regions))
        #Convert images to bytes
        image_bytes = np.fromfile(os.path.join (base_image_location, filename + ".jpg"), np.uint8)
        upload_result = trainer.create_images_from_data(projectid, image_bytes.tobytes(), [Ones_tag.id])

# print("All Iterations:", trainer.get_iterations(projectid))

trainer.train_project(projectid)
while True:
    iteration  = trainer.get_iteration(projectid,"174a4e4d-2085-484c-8a15-2416d7cc9ff1")
    if iteration.status=="Completed":
        break
    print("Training status: " + iteration.status)
    time.sleep(1)
print("Training Completed!")

# if not upload_result.is_batch_successful:
#     print("Image batch upload failed.")
#     for image in upload_result.images:
#         print("Image status: ", image.status)
#     exit(-1)
# print ("Training...")
# iteration = trainer.train_project(projectid)
# while (iteration.status != "Completed"):
#     iteration = trainer.get_iteration(projectid, iteration.id)
#     print ("Training status: " + iteration.status)
#     time.sleep(1)
# print("Done")

# for filename in Ones.keys():
#     x,y,w,h = Ones[filename]
#     regions = [ Region(tag_id=Ones_tag.id, left=x,top=y,width=w,height=h) ]
#     with open(os.path.join (base_image_location, filename + ".jpg"), mode="rb") as image_contents:
#         tagged_images_with_regions.append(ImageFileCreateEntry(name=filename, contents=image_contents.read(), regions=regions))
# upload_result = trainer.create_images_from_files(projectid, ImageFileCreateBatch(images=tagged_images_with_regions))