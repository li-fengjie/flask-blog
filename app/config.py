import os

# config所在目录
base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jiangxiligong'
    # 数据库的操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    # MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.qq.com'
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or '1640105751@qq.com'
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or 'lpeaarzmxvbydeia'
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.126.com'
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or 'gaohj66666@126.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or 'zxasqw12'

    # bootstrap
    BOOTSTRAP_SERVE_LOCAL = True

    # 文件上传
    MAX_CONTENT_LENTH = 1024 * 1024 * 8
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')

    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'static/db/bbs_dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'static/db/bbs_test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'static/db/bbs.sqlite')


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
