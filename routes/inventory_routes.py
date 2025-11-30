# Inventory CRUD routes and dashboard
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.models import Item, Branch, Alert
from sqlalchemy import func

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory', template_folder='../templates')

@inventory_bp.route('/dashboard')
@login_required
def dashboard():
    # Dashboard statistics
    total_stock = db.session.query(func.sum(Item.quantity)).scalar() or 0
    low_stock = Item.query.filter(Item.quantity < Item.threshold).count()
    out_of_stock = Item.query.filter(Item.quantity <= 0).count()
    branches = Branch.query.all()
    # Chart data: quantity per branch
    chart_data = []
    for b in branches:
        qty = db.session.query(func.sum(Item.quantity)).filter(Item.branch_id == b.id).scalar() or 0
        chart_data.append({'branch': b.name, 'quantity': int(qty)})
    # Auto-generate alerts for low-stock items (dashboard-only)
    low_items = Item.query.filter(Item.quantity < Item.threshold).all()
    # Upsert simple alerts (non-duplicating)
    for it in low_items:
        existing = Alert.query.filter_by(item_id=it.id, resolved=False).first()
        if not existing:
            a = Alert(item_id=it.id, message=f'Low stock for {it.name} (qty={it.quantity})', level='warning')
            db.session.add(a)
    db.session.commit()
    alerts = Alert.query.filter_by(resolved=False).order_by(Alert.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', total_stock=total_stock, low_stock=low_stock,
                           out_of_stock=out_of_stock, chart_data=chart_data, alerts=alerts, branches=branches)

@inventory_bp.route('/')
@login_required
def list_items():
    branch_id = request.args.get('branch', type=int)
    query = Item.query
    if branch_id:
        query = query.filter_by(branch_id=branch_id)
    items = query.order_by(Item.name).all()
    branches = Branch.query.all()
    return render_template('inventory.html', items=items, branches=branches, selected_branch=branch_id)

@inventory_bp.route('/create', methods=['POST'])
@login_required
def create_item():
    data = request.form
    item = Item(
        sku=data.get('sku'),
        name=data.get('name'),
        description=data.get('description'),
        quantity=int(data.get('quantity') or 0),
        threshold=int(data.get('threshold') or 10),
        price=float(data.get('price') or 0.0),
        branch_id=int(data.get('branch_id')) if data.get('branch_id') else None
    )
    db.session.add(item)
    db.session.commit()
    flash('Item created', 'success')
    return redirect(url_for('inventory.list_items'))

@inventory_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.form
    item.name = data.get('name')
    item.description = data.get('description')
    item.quantity = int(data.get('quantity') or item.quantity)
    item.threshold = int(data.get('threshold') or item.threshold)
    item.price = float(data.get('price') or item.price)
    item.branch_id = int(data.get('branch_id')) if data.get('branch_id') else item.branch_id
    db.session.commit()
    flash('Item updated', 'success')
    return redirect(url_for('inventory.list_items'))

@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted', 'info')
    return redirect(url_for('inventory.list_items'))
