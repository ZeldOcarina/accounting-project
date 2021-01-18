from flask import request, redirect, render_template, url_for
from flask.views import View
from forms import CreateVendor
from model import db, Vendor, Customer
from datetime import datetime


class CreateVendorView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = CreateVendor()
        if request.method == 'POST':
            if form.validate_on_submit():
                vendor = Vendor(
                    name=request.form.get("name"),
                    address=request.form.get("address"),
                    email=request.form.get("email"),
                    zip_code=request.form.get("zip_code"),
                    iva_code=request.form.get("iva_code"),
                    phone_number=request.form.get("phone_number"),
                )
                db.session.add(vendor)
                db.session.commit()
                return redirect('/')

        return render_template('new_customer.html', form=form, type="vendor")
