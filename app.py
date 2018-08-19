# -------------------------------------------------------------------------------
# Author: Chase Midler, Andy Gao
# -------------------------------------------------------------------------------
# Tools uses:
# MongoDb, Flask,Python
# -------------------------------------------------------------------------------
import requests
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from output_json import output_json
from colorharmonies import *
from deltaE import deltaE
from get_color_image import color_image
import base64, io, urllib
from PIL import Image

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)
app = Flask(__name__)

# initializing db
app.config['MONGO_DBNAME'] = 'ppgcolors'
app.config['MONGO_URI'] = 'mongodb://ppg_paint:ppgpaint1@ds125862.mlab.com:25862/ppgcolors'
mongo = PyMongo(app)

# fix for json double encoding and initializing API
DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = Api(app)
api.representations = DEFAULT_REPRESENTATIONS

@app.route('/')
def read_me():
    return render_template('readme.html')


# output for when rgb is not in db
def errorOutput(r, g, b, string):
    return string.format(
        str(r) + ", " + str(g) + ", " + str(b))

# colorharmoniesFunctions
function = {'complementary': complementaryColor, 'triadic': triadicColor, 'split_complementary': splitComplementaryColor, 'tetradic': tetradicColor, 'analogous': analogousColor, 'monochromatic': monochromaticColor,'lighter': tintColor,'darker': shadeColor}


# @route GET /colors?
# @desc Searches for Color in Database based on given arguments
# @access Public
class ColorSearch(Resource):

    # initializing url queries  
    def __init__(self):
        self.reqparse = reqparse.RequestParser() 
        self.reqparse.add_argument('name', type = str, location = 'args')
        self.reqparse.add_argument('color-number', type = str, location = 'args')
        self.reqparse.add_argument('R', type = str, location = 'args')
        self.reqparse.add_argument('G', type = str, location = 'args')
        self.reqparse.add_argument('B', type = str, location = 'args')
        super().__init__()

    # searching for color in dataset based on Color Name
    def get(self):  
        argslist = self.reqparse.parse_args()
        colors = mongo.db.colors
        if argslist['name']:
        
            paintName = argslist['name'].upper()
            
            colorExist = colors.find_one({'Color Name': paintName})
            value1 = 'Name'
            value2 = paintName
            
        elif (argslist['R'] and argslist['G'] and argslist['B']):
            R = int(argslist['R'])
            G = int(argslist['G'])
            B = int(argslist['B']) 
            colorExist = colors.find_one(
                {'R': R, 'G': G, 'B': B})
            if colorExist == None:
                dE = deltaE(colors, R, G, B)
                R,G,B= int(dE[0]),int(dE[1]),int(dE[2])
                
            colorExist = colors.find_one({'R': R, 'G': G, 'B': B})
            value1 = 'RGB'
            value2 = '{},{},{}'.format(R,G,B)
    
        elif argslist['color-number']:
            color_number = argslist['color-number'].upper()
            
            colorExist = colors.find_one({'Color Number': color_number})
            value1 = 'Number'
            value2 = color_number
            

        else:
            return 404
      
        if colorExist:
            imgURL = color_image(colorExist['R'],colorExist['G'],colorExist['B'])
            colorExist['imgURL'] = imgURL
            result = colorExist
        else:
            result = 'The Color {}: {} does not exist in the Database'.format(value1,value2)
        return {'result': result}, 200 if argslist else 404
      

# @route GET /<string:colorharmony>?
# @desc Given a specific color harmony function listed in functions dictionary, performs function on color
# @access Public
class ColorConvert(Resource):

    # initializing url queries  
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'args')
        self.reqparse.add_argument('R', type = str, location = 'args')
        self.reqparse.add_argument('G', type = str, location = 'args')
        self.reqparse.add_argument('B', type = str, location = 'args')
        super().__init__()


    def get(self,func):
        argslist = self.reqparse.parse_args()
        colors = mongo.db.colors
        R,G,B = "","",""
        if argslist['name']:

            paintName = argslist['name'].upper()

            # Searching for Color 
            if colors.find_one({'Color Name': paintName}):
                colorExist = colors.find_one({'Color Name': paintName})
                R = colorExist['R']
                G = colorExist['G']
                B = colorExist['B']
            else:
                return 404
        elif (argslist['R'] and argslist['G'] and argslist['B']):
            R = argslist['R']
            G = argslist['G']
            B = argslist['B'] 
        else:
            return 404
        rgb = [int(R), int(G), int(B)]
        color = Color(rgb, "", "")
        
        #based on url, finds the correct function
        colorConvert = function[func](color)
        

        is2dList = isinstance(colorConvert[0], list)
        result = []
        cnt = 1
        
        # returns result with different puncuations based of whether it is 2dList or not
        if is2dList:
            colorConvert = list(map((lambda x: [int(c) for c in x] ), colorConvert))
            colorDic = {}
            for lst in colorConvert:
            
                # runs deltaE function to find nearest color that matches harmony result in dataset 
                dE =list(map((lambda x: int(x)), deltaE(colors, lst[0],lst[1],lst[2]) )) 
                colorExist = colors.find_one({'R': dE[0], 'G': dE[1], 'B': dE[2]})
             
                imgURL = color_image(colorExist['R'],colorExist['G'],colorExist['B'])
                addColor = {'color{}'.format(cnt): {'R': dE[0], 'G': dE[1], 'B': dE[2], 'Name': colorExist['Color Name'], 'desc': colorExist['Color Description'], 'imgURL': imgURL} }
                colorDic.update(addColor)
                cnt += 1
            result.append(colorDic)
        else:
            lst = [int(c) for c in colorConvert]
            
            # runs deltaE function to find nearest color that matches harmony result in dataset 
            dE =list(map((lambda x: int(x)), deltaE(colors, lst[0],lst[1],lst[2]) )) 
            colorExist = colors.find_one({'R': dE[0], 'G': dE[1], 'B': dE[2]})
            imgURL = color_image(colorExist['R'],colorExist['G'],colorExist['B'])
            addColor = {'color{}'.format(cnt): {'R': dE[0], 'G': dE[1], 'B': dE[2], 'Name': colorExist['Color Name'], 'desc': colorExist['Color Description'],'imgURL': imgURL}} 
            result.append(addColor)

        return {'result': result }, 200 if result else 404

# @route POST /
# @desc Given an image, finds most dominant color in database and returns said color
# @access Public
class imgTo64(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser() 
        self.reqparse.add_argument('url', type = str)
        super().__init__()

    def post(self):
        argslist = self.reqparse.parse_args()
        url = argslist['url']
        the_file = io.BytesIO(urllib.request.urlopen(url).read())
        img=Image.open(the_file)
        size = 250,250
        img.thumbnail(size)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        base = base64.b64encode(buffered.getvalue())
        width, height = img.size

        data = {
            "original": base.decode("utf-8"),
             "coordinates": [[0, 0], [width, height]]
        }
        
        response = requests.post(url = "https://get-colors-service-dot-color-monarch-flex.appspot.com", json = data)
        result = response.json()
        return {'result': result }, 200 if result else 404 
        

api.add_resource(ColorSearch, '/colors')
api.add_resource(ColorConvert, '/<string:func>')
api.add_resource(imgTo64,'/')
if __name__ == "__main__":
	app.run(port=6969,debug=True)
