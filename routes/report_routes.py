# Reports: simple CSV export of current stock
from flask import Blueprint, send_file, make_response
from flask_login import login_required
from io import StringIO
import csv
from models.models import Item
from extensions import db

report_bp = Blueprint('report', __name__, url_prefix='/reports', template_folder='../templates')

@report_bp.route('/')
@login_required
def reports():
    # Reports page (template will provide export link)
    from flask import render_template
    items = Item.query.order_by(Item.name).all()
    return render_template('reports.html', items=items)

@report_bp.route('/export_csv')
@login_required
def export_csv():
    items = Item.query.order_by(Item.name).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['SKU','Name','Quantity','Threshold','Price','Branch'])
    for it in items:
        branch_name = it.branch.name if it.branch else ''
        cw.writerow([it.sku, it.name, it.quantity, it.threshold, it.price, branch_name])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=stock_report.csv"
    output.headers["Content-type"] = "text/csv"
    return output
