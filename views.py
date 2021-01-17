import os
from flask.views import View
from flask import render_template, current_app, request
from model import db, LineItem, Customer, Vendor
import requests
from datetime import datetime
from sqlalchemy import and_
import boto3
from botocore.config import Config

API_ENDPOINT = "http://data.fixer.io/api/latest"
API_KEY = os.getenv("FIXER_API_KEY")

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


class Home(View):
    def dispatch_request(self):
        if request.args:
            filters_list = []
            from_date = datetime.strptime(request.args.get("daterange").split('-')[0].strip(), '%d/%m/%Y')
            to_date = datetime.strptime(request.args.get("daterange").split('-')[1].strip(), '%d/%m/%Y')
            filters_list.append(and_(LineItem.line_date >= from_date, LineItem.line_date <= to_date))

            if request.args.get("customer") != '':
                filters_list.append(LineItem.customer_id == request.args.get("customer"))
            if request.args.get("vendor") != '':
                filters_list.append(LineItem.vendor_id == request.args.get("vendor"))
            if request.args.get("kind"):
                filters_list.append(LineItem.kind == request.args.get("kind"))

            filters = tuple(filters_list)

            all_line_items = db.session.query(LineItem) \
                .filter(*filters) \
                .order_by(LineItem.line_date.desc()) \
                .all()
        else:
            all_line_items = db.session.query(LineItem).order_by(LineItem.line_date.desc()).all()
        customers = db.session.query(Customer).all()
        vendors = db.session.query(Vendor).all()

        # Base currency is EUR
        response = requests.get(url=API_ENDPOINT, params={"access_key": API_KEY, "symbols": 'CHF,USD'})
        CHF_rate = float(response.json()["rates"]["CHF"])
        USD_rate = float(response.json()["rates"]["USD"])

        # print(f'CHF: {CHF_rate}, USD: {USD_rate}')
        # CHF_rate = 1.084
        # USD_rate = 1.2225

        total_balance = 0
        for line_item in all_line_items:
            line_item.date = line_item.line_date.strftime('%d/%m/%Y')
            if line_item.currency == 'EUR':
                line_item.currency = '€'
                line_item.CHF_value = line_item.amount * CHF_rate
            elif line_item.currency == 'USD':
                line_item.currency = '$'
                EUR_value = line_item.amount / USD_rate
                line_item.CHF_value = EUR_value * CHF_rate
            else:
                line_item.CHF_value = line_item.amount

            if line_item.kind == "Invoice":
                total_balance += line_item.CHF_value
            else:
                total_balance -= line_item.CHF_value

            for customer in customers:
                if customer.id == line_item.customer_id:
                    line_item.customer = customer

            for vendor in vendors:
                if vendor.id == line_item.vendor_id:
                    line_item.vendor = vendor

            if line_item.file:
                line_item.presigned_url = \
                    client.generate_presigned_url('get_object',
                                                  Params={'Bucket': os.environ.get('S3_BUCKET'),
                                                          'Key': line_item.file,
                                                          'ResponseContentType': "application/pdf"},
                                                  ExpiresIn=3600)

        return render_template('index.html', line_items=all_line_items, customers=customers, vendors=vendors,
                               total_balance=round(total_balance, 2),
                               uploads_directory=os.path.join(current_app.config['UPLOAD_FOLDER']),
                               query=request.args.to_dict(), print=print, str=str)
