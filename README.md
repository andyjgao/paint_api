# Paint API

This API, in conjunction with Color Monarch's API, allows for user to query paint color details of PPG PAINTS as well as find color harmonies of a specified paint color


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Required Dependencies

```
flask, flask-restful, flask-pymongo, colormath, requests, pillow, pandas
```


### Installing

To install dependencies, enter the following with the dependencies's name

```
pip install [dependency]
```

## Deployment
To deploy type the following in the file folder

```
python app.py
```

* __/colors?name=`[insert paint name]`:__ seaches for paint based on Color Name  (i.e. /colors?name=fresh+lemonade)
* __/colors?R=`[R]`&G=`[G]`&B=`[B]`:__ seaches for paint based on RGB values (i.e. /colors?R=236?G=230?B=120)
* __/colors?color-number=`[insert PPG Color Number]`:__ seaches for paint based on PPG Color Number (i.e. /colors?color number=ppg1216-5)
* __/<string:harmony>?name=`[insert paint name]`:__ returns the requested harmony based on Color Name (i.e. /complementary?name=fresh+lemonade)
* __/<string:harmony>R=`[R]`&G=`[G]`&B=`[B]`:__ returns the requested harmony based on RGB values (i.e. /complementary?R=236?G=230?B=120)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
