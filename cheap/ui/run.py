from cheap.ui import create_app
from pyqueen import DataSource
from settings import SERVERS


class Config:
    SQLALCHEMY_DATABASE_URI = DataSource(**SERVERS['main']).get_jdbc_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭警告


app = create_app(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    app.run(debug=True)
