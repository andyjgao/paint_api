import requests
import json
def color_image(r,g,b):
  path = 'https://svg-to-png-color.herokuapp.com/image?R={}&G={}&B={}'.format(r,g,b)
  return path