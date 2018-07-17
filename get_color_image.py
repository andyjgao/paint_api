import requests
import json
def color_image(r,g,b):
  path = 'http://www.thecolorapi.com/id?rgb='+str(r)+','+str(g)+','+str(b)
  request = requests.get(path)
  info = request.json()
  return info['image']['bare']
