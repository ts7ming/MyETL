from flask import Blueprint, render_template, request, redirect, url_for, flash
from cheap.models import EtlJob, session_context

main = Blueprint('main', __name__)


# 定义首页路由
@main.route('/')
def index():
    jobs = EtlJob().get_job()
    return render_template('index.html', jobs=jobs)


# 定义关于页面路由
@main.route('/about')
def about():
    return render_template('about.html', title="关于我们")


# 定义一个简单的表单处理路由
@main.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 假设表单中有一个名为 'name' 的字段
        name = request.form.get('name')
        if name:
            # 使用 Flask 的 flash 消息功能显示一条消息
            flash(f'你好, {name}!', 'success')
            # 重定向到首页
            return redirect(url_for('main.index'))
        else:
            flash('请输入一个名字。', 'danger')
    # 如果是 GET 请求，渲染提交表单的模板
    return render_template('submit.html')


# 定义一个动态路由
@main.route('/user/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)
