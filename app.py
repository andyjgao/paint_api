from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from output_json import output_json
from colorharmonies import *


app = Flask(__name__)

# initializing db
app.config['MONGO_DBNAME'] = 'ppgcolors'
app.config['MONGO_URI'] = 'mongodb://supagao:ppgpaint1@ds163410.mlab.com:63410/ppgcolors'
mongo = PyMongo(app)

# fix for json double encoding and initializing API
DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

# output for when rgb is not in db
def errorOutput(r, g, b, string):
    return string.format(
        str(r) + ", " + str(g) + ", " + str(b))

#colorharmoniesFunctions
function = {'complementary': complementaryColor, 'triadic': triadicColor, 'split_complementary': splitComplementaryColor, 'tetradic': tetradicColor, 'analogous': analogousColor, 'monochromatic': monochromaticColor}

class NameSearch(Resource):
    def __init__(self):
      self.reqparse = reqparse.RequestParser()
      self.reqparse.add_argument('name', type = str, location = 'args')
      super().__init__()

    def get(self):  
      argslist = self.reqparse.parse_args()
      paintName = argslist['name'].upper()
      colors = mongo.db.colors
      colorExist = colors.find_one(
          {'Color Name': paintName})
      if colorExist:
          result = colorExist
      else:
          result = 'The Color Name, {}, does not exist in the Database'.format(paintName)
      return {'result': result}, 200 if result else 404
      


class RGBSearch(Resource):
    def get(self, R, G, B):
        colors = mongo.db.colors
        colorExist = colors.find_one(
            {'R': R, 'G': G, 'B': B})
        if colorExist:
            result = colorExist
        else:
            result = errorOutput(R, G, B,"The RGB value {} does not exist in Database")

        return {'result': result}, 200 if result else 404

class ColorConvert(Resource):
    def get(self, R, G, B, func):
        rgb = [R, G, B]
        color = Color(rgb, "", "")
        colorConvert = function[func](color)
        is2dList = isinstance(colorConvert[0], list)
        result = []
        cnt = 1
        if is2dList:
          colorConvert = list(map((lambda x: [int(c) for c in x] ), colorConvert))
          colorDic = {}
          for lst in colorConvert:
            addColor = {'color{}'.format(cnt): {'R': lst[0], 'G': lst[1], 'B': lst[2]} }
            colorDic.update(addColor)
            cnt += 1
          result.append(colorDic)
        else:
          lst = [int(c) for c in colorConvert]
          addColor = {'color{}'.format(cnt): {'R': lst[0], 'G': lst[1], 'B': lst[2]}} 
          result.append(addColor)

        return {'result': result }, 200 if result else 404

api.add_resource(NameSearch, '/colors')
api.add_resource(RGBSearch, '/colors/<int:R>/<int:G>/<int:B>')
api.add_resource(ColorConvert, '/<string:func>/<int:R>/<int:G>/<int:B>')

app.run(host='0.0.0.0') 
