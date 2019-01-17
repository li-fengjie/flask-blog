import os
from flask import Blueprint, render_template, url_for, request, flash, get_flashed_messages, redirect, current_app
from app.forms import RegisterForm, LoginForm, UploadForm, FindPwdForm, passwordForm, emailForm
from app.models import User
from app.exts import db, photos
from app.email import send_mail
from flask_login import login_required, login_user, logout_user, current_user
from PIL import Image

users = Blueprint('users', __name__)


# 注册
@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(u)
        db.session.commit()

        # 生成token  用u对象调用模型中的方法
        token = u.generate_active_token()
        send_mail(u.email, '账户激活', 'email/activate', username=u.username, token=token)
        flash("恭喜注册成功,请点击邮件中的链接完成激活")
        return redirect(url_for('users.login'))
    return render_template('user/register.html', form=form)


# 这个方法用来验证token  给用户邮箱发送过去一个完整的url
@users.route('/active/<token>', methods=['GET', 'POST'])
def active(token):
    if User.check_active_token(token):
        flash("账户激活成功")
        return redirect(url_for('users.login'))
    else:
        flash("账户激活失败")
        return redirect(url_for('main.index'))


# 登录
@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash("该用户名不存在")
        elif not u.confirmed:
            flash("该账户没有激活,请激活后登录")
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            flash("登录成功")
            return redirect(request.args.get('next') or url_for("main.index"))
        else:
            flash("密码不正确")
    return render_template('user/login.html', form=form)


# 退出登录
@users.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("退出登录成功")
    return redirect(url_for('main.index'))


@users.route('/test/', methods=['GET', 'POST'])
@login_required
def test():
    return 'this is test'


# 找回密码
@users.route('/find_pwd/', methods=['GET', 'POST'])
def find_pwd():
    form = FindPwdForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u:
            flash("该用户名不存在")
        elif not u.email == form.email.data:
            flash("邮箱不正确！！")
        else:
            # 生成token  用u对象调用模型中的方法
            token = u.generate_active_token()
            send_mail(u.email, '密码找回', 'email/findpwd', username=u.username, token=token)
            flash("请点击邮件中的链接找回密码")
            return redirect(url_for('users.find_pwd'))
    return render_template('user/find_pwd.html', form=form)


# 这个方法用来验证token  给用户邮箱发送过去一个完整的url 生成新密码
@users.route('/acfpwd/<username>/<token>', methods=['GET', 'POST'])
def acfpwd(username, token):
    if User.check_active_token(token):
        new_pwd = random_string()
        u = User.query.filter_by(username=username).first()
        u.password = new_pwd
        db.session.commit()
        flash("新密码为：" + new_pwd)
        return redirect(url_for('users.login'))
    else:
        flash("密码找回失败")
        return redirect(url_for('main.index'))


# 修改密码
@users.route('/change_pwd/', methods=['GET', 'POST'])
@login_required
def change_pwd():
    form = passwordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldPassword.data):
            current_user.password = form.newPassword1.data
            # db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功')
            logout_user()
            flash('请重新登录')
            return redirect(url_for("users.login"))
        else:
            flash('密码修改失败')
    return render_template('user/change_pwd.html', form=form)


# 修改邮箱
@users.route('/change_email/', methods=['GET', 'POST'])
@login_required
def change_email():
    form = emailForm()
    if form.validate_on_submit():
        if current_user.email == form.oldEmail.data:
            current_user.email = form.newEmail1.data
            # db.session.add(current_user)
            db.session.commit()
            current_user.confirmed = False
            token = current_user.generate_active_token()
            send_mail(current_user.email, '账户激活', 'email/activate', username=current_user.username, token=token)
            flash("请点击邮件中的链接完成激活")
            return redirect(url_for('users.login'))
    return render_template('user/change_email.html', form=form)


# 修改头像
@users.route('/change_icon/', methods=['GET', 'POST'])
@login_required
def change_icon():
    img_url = ''
    form = UploadForm()
    if form.validate_on_submit():
        # 获取文件后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 随机文件名  拼接
        filename = random_string() + suffix
        photos.save(form.icon.data, name=filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        img = Image.open(pathname)
        img.thumbnail((128, 128))
        img.save(pathname)
        if current_user.icon != 'default.jpg':
            os.remove(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon)
        current_user.icon = filename  # 将新上传的文件名 赋值给 用户的头像
        db.session.add(current_user)  # 保存在数据库中
        flash("头像上传成功")
        return redirect(url_for("users.change_icon"))
    img_url = photos.url(current_user.icon)
    return render_template('user/change_icon.html', form=form, img_url=img_url)


# 生成随机字符串
def random_string(length=16):
    import random
    base_str = '1234567890abcdefhijklmnopqrstuvwxyz'
    return ''.join(random.choice(base_str) for i in range(length))
