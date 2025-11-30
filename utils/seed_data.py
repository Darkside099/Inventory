# Seed script: idempotent insertion of sample users, branches, items and alerts.
from models.models import User, Branch, Item, Alert
from werkzeug.security import generate_password_hash

def seed_all(db):
    if User.query.first():
        return
    admin = User(username='admin', password=generate_password_hash('adminpass'), role='Admin')
    manager = User(username='manager', password=generate_password_hash('managerpass'), role='Manager')
    staff = User(username='staff', password=generate_password_hash('staffpass'), role='Staff')
    db.session.add_all([admin, manager, staff])

    b1 = Branch(name='Mumbai Warehouse', location='Mumbai, India')
    b2 = Branch(name='Delhi Distribution', location='New Delhi, India')
    b3 = Branch(name='Bengaluru Hub', location='Bengaluru, India')
    db.session.add_all([b1, b2, b3])
    db.session.flush()
    items = [
        Item(sku='SKU-1001', name='Cloud Router', description='High throughput router', quantity=25, threshold=10, price=350.0, branch_id=b1.id),
        Item(sku='SKU-1002', name='Edge Switch', description='48-port switch', quantity=8, threshold=10, price=120.0, branch_id=b1.id),
        Item(sku='SKU-2001', name='Power Supply', description='Redundant PSU', quantity=0, threshold=5, price=75.0, branch_id=b2.id),
        Item(sku='SKU-3001', name='Fiber Patch Cable', description='10m LC-LC', quantity=50, threshold=20, price=5.0, branch_id=b3.id)
    ]
    db.session.add_all(items)
    db.session.flush()

    alerts = []
    for it in items:
        if it.quantity < it.threshold or it.quantity <= 0:
            alerts.append(Alert(item_id=it.id, message=f'Auto-generated alert for {it.name} (qty={it.quantity})', level='warning'))
    db.session.add_all(alerts)

    db.session.commit()
