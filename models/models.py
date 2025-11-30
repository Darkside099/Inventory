from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # In production store hashed passwords
    role = Column(String(20), nullable=False, default='Staff')  # Admin, Manager, Staff
    created_at = Column(DateTime, default=datetime.utcnow)

    # convenience
    def is_admin(self):
        return self.role.lower() == 'admin'

class Branch(db.Model):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    location = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship('Item', back_populates='branch', cascade="all, delete-orphan")

class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    sku = Column(String(60), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    quantity = Column(Integer, default=0)
    threshold = Column(Integer, default=10)  # auto alert when quantity < threshold
    price = Column(Float, default=0.0)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship('Branch', back_populates='items')

    @property
    def status(self):
        if self.quantity <= 0:
            return 'out_of_stock'
        if self.quantity < self.threshold:
            return 'low_stock'
        return 'in_stock'

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    message = Column(String(500))
    level = Column(String(20), default='warning')  # warning, critical, info
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship('Item')
