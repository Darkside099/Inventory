import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '!@#$%^&*()(*&^%$#@!)')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root1234@inventory.cmz8mc8mmzsm.us-east-1.rds.amazonaws.com:3306/inventory'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 20
