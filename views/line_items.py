from datetime import datetime
import os
from io import StringIO
from flask import request, redirect, render_template, url_for, g, flash, current_app
from flask.views import View
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy.exc import InterfaceError
from forms import CreateLine
from model import db, LineItem, Customer, Vendor
import boto3
from botocore.config import Config

my_config = Config(
    region_name=os.environ.get("AWS_REGION"),
    signature_version='s3v4',
)

client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
    endpoint_url='https://s3.eu-central-1.amazonaws.com',
    config=my_config
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_file(filename):
    client.delete_object(Bucket=os.environ.get("S3_BUCKET"), Key=filename)



class CreateLineItemView(View):
    decorators = [login_required]
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = CreateLine()
        form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
        form.vendor.choices = [(v.id, v.name) for v in Vendor.query.all()]

        if request.method == 'POST':
            date_time_str = request.form.get("line_date")
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

            if 'document' in request.files:
                file_name = secure_filename(
                    f"{request.form.get('kind').lower()}-{datetime.now().strftime('%d%m%Y%H%M%S')}"
                    f".{request.files['document'].filename.split('.')[-1]}")
                buffer = request.files['document'].read()

                client.put_object(
                    Body=buffer,
                    Key=file_name,
                    Bucket=os.environ.get("S3_BUCKET"))

            if form.validate_on_submit():
                try:
                    line_item = LineItem(
                        line_date=date_time_obj,
                        kind=request.form.get("kind"),
                        item=request.form.get("item"),
                        currency=request.form.get("currency"),
                        amount=request.form.get("amount"),
                        paid=True if request.form.get("paid") == 'y' else False,
                        customer_id=request.form.get("customer") if request.form.get("kind") == 'Invoice' else None,
                        vendor_id=request.form.get("vendor") if request.form.get("kind") == 'Expense' else None,
                        author_id=g.user.id,
                        file=file_name if isinstance(file_name, str) else None
                    )
                    db.session.add(line_item)
                    db.session.commit()
                except InterfaceError:
                    flash("Please fill all needed data")
                    return redirect(url_for('new_line_item'))
                else:
                    return redirect(url_for('home'))
        return render_template('new_line.html', form=form)


class EditLineView(View):
    decorators = [login_required]
    methods = ['GET', 'POST', 'DELETE']

    def dispatch_request(self, line_item_id):
        line_item = LineItem.query.get(line_item_id)
        form = CreateLine(obj=line_item)
        form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
        form.customer.default = int(line_item.customer_id) if line_item.customer_id else 1
        form.process(obj=line_item)

        if request.method == 'POST':
            if line_item.file and 'document' in request.files:
                delete_file(line_item.file)

            if 'document' in request.files:
                new_file_name = secure_filename(
                                    f"{request.form.get('kind').lower()}-{datetime.now().strftime('%d%m%Y%H%M%S')}"
                                    f".{request.files['document'].filename.split('.')[-1]}")
                line_item.file = new_file_name
                buffer = request.files['document'].read()

                client.put_object(
                    Body=buffer,
                    Key=new_file_name,
                    Bucket=os.environ.get("S3_BUCKET"))

            date_time_str = request.form.get("line_date")
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')

            dict = request.form.to_dict()

            line_item.date = date_time_obj
            line_item.kind = dict["kind"]
            line_item.item = dict["item"]
            line_item.currency = dict["currency"]
            line_item.amount = dict["amount"]
            line_item.paid = True if request.form.get("paid") == "y" else False
            line_item.customer_id = dict["customer"] if dict["kind"] == 'Invoice' else None
            line_item.author_id = g.user.id

            db.session.commit()
            return redirect("/")

        if request.method == 'DELETE':
            if line_item.file:
                delete_file(os.path.join(current_app.config['UPLOAD_FOLDER'], line_item.file), line_item.file)
            db.session.delete(line_item)
            db.session.commit()
            return redirect(url_for('home'))

        return render_template('new_line.html', form=form)
