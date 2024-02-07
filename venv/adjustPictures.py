import cv2
class adjustPictur:
    def __init__(self) -> None:
      pass
    
    def crop_image(image,cropped_boundaries):
      x,y,w,h = cropped_boundaries
      cropped_hand = image[y:y+h,x:x+w]
      return cropped_hand
    
    def makeARectangle(image, x,y,w,h):
      img_with_rectangle = image.copy()  # Create a copy of the image
      cv2.rectangle(img_with_rectangle, (x, y), (x+w+10, y+h+10), (0, 255, 0), 2)
      return img_with_rectangle
