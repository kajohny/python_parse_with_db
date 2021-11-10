# PYTHON PARSING PARAGRAPHS INTO DATABASE

## Installation
```
pip install flask
pip install flask-sqlalchemy
pip install bs4
pip install selenium
pip webdriver_manager
```

## Usage
```
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
```
## Examples

*SQLAlchemy*:
```
app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True) 
```

*Routes*:
```
@app.route('/news', methods=['GET', 'POST'])
@app.route('/blogs', methods = ['GET'])
```

*Selenium and webdriver*:
```
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
driver.get(url)
```

*Database table*:
```
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column('id', db.Integer, primary_key=True)
    coin_name = db.Column('coin_name', db.String(50), index=True, unique=True)
    news_paragraph = db.Column('news_paragraph', db.Text)
    def __init__(self, coin_name, news_paragraph):
        self.coin_name = coin_name
        self.news_paragraph = news_paragraph
```
