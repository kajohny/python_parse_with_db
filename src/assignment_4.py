from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3tk3y'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column('id', db.Integer, primary_key=True)
    coin_name = db.Column('coin_name', db.String(50), index=True, unique=True)
    news_paragraph = db.Column('news_paragraph', db.Text)
    def __init__(self, coin_name, news_paragraph):
        self.coin_name = coin_name
        self.news_paragraph = news_paragraph

class Blogs(db.Model):
    __tablename__ = 'blogs'
    id = db.Column('id', db.Integer, primary_key=True)
    coin_name = db.Column('coin_name', db.String(50), index=True, unique=True)
    blogs_paragraph = db.Column('blogs_paragraph', db.Text)
    def __init__(self, coin_name, blogs_paragraph):
        self.coin_name = coin_name
        self.blogs_paragraph = blogs_paragraph
db.create_all()

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        coin = request.form.get('coin')
        results = News.query.filter_by(coin_name = coin).first()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        driver.get('https://coinmarketcap.com/currencies/' + coin + '/news/')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if results:
            newsList = soup.select('p.sc-1eb5slv-0.svowul-3.ddtKCV')

            n = ''
            for lists in newsList:
                for x in lists.text:
                    n += '' + x

            results.news_paragraph = n
            db.session.commit()
            return results.news_paragraph
        else:
            newsList = soup.select('p.sc-1eb5slv-0.svowul-3.ddtKCV')
            n = ''

            for lists in newsList:
                for x in lists.text:
                    n += '' + x

            new_paragraph = News(coin, n)
            db.session.add(new_paragraph)
            db.session.commit()
            return new_paragraph.news_paragraph


    return '''
              <form method="POST">
                  <div><label>Coin name: <input type="text" name="coin"></label></div>
                  <input type="submit" value="Show news">
              </form>'''

@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    if request.method == 'POST':
        coin = request.form.get('coin')
        results = Blogs.query.filter_by(coin_name = coin).first()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
        driver.get('https://coinmarketcap.com/currencies/' + coin)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if results:
            return results.blogs_paragraph
        else:
            blogsList = soup.select('div.sc-16r8icm-0.kjciSH.contentClosed.hasShadow, p')
            b = ''

            for lists in blogsList[4:-8]:
                for x in lists.text:
                    b += '' + x

            new_paragraph = Blogs(coin, b)
            db.session.add(new_paragraph)
            db.session.commit()
            return new_paragraph.blogs_paragraph


    return '''
              <form method="POST">
                  <div><label>Coin name: <input type="text" name="coin"></label></div>
                  <input type="submit" value="Show blogs">
              </form>'''

if __name__ == '__main__':
    app.run(debug=True) 