from etl import create_app, config

app = create_app(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    app.run(debug=True)