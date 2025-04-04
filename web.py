from flask import Flask, render_template_string
from pyqueen import DataSource


ds = DataSource(**db)

app = Flask(__name__)


# 网页路由
@app.route('/')
def show_data():
    # 连接数据库
    # 查询数据
    items = ds.read_sql("SELECT * FROM etl_job").values

    # 渲染模板
    return render_template_string('''
        
    ''', items=items)


if __name__ == '__main__':
    # 启动 Flask 开发服务器
    app.run(debug=True)