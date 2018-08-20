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

Now you can type /image?R=`[R]`&G=`[G]`&B=`[B]` to get desired image of color


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
