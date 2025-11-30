import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '!@#$%^&*()(*&^%$#@!)')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root@localhost:3306/cloud_inventory_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 20
