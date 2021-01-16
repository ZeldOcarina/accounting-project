from flask import request, redirect, render_template, url_for
from flask.views import View
from forms import CreateVendor
from model import db, Vendor, Customer


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
                # customer = Customer.from_form_data(request.form)
                db.session.add(vendor)
                db.session.commit()
                print(vendor)
            return redirect('/')
        return render_template('new_customer.html', form=form, type="vendor")


class AllCustomers(View):
    def dispatch_request(self):
        customers = db.session.query(Customer).all()
        for customer in customers:
            customer.view_creation_date = customer.creation_date.strftime("%d/%m/%Y")
        return render_template('customer_list.html', customers=customers)


class SingleCustomer(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, customer_id):
        customer = Customer.query.get(customer_id)
        form = CreateCustomer(
            name=customer.name,
            address=customer.address,
            email=customer.email,
            zip_code=customer.zip_code,
            iva_code=customer.iva_code,
            phone_number=customer.phone_number,
        )
        if request.method == 'POST':
            if form.validate_on_submit():
                customer.name = request.form.get("name")
                customer.address = request.form.get("address")
                customer.email = request.form.get("email")
                customer.zip_code = request.form.get("zip_code")
                customer.iva_code = request.form.get("iva_code")
                customer.phone_number = request.form.get("phone_number")
                db.session.commit()
                return redirect(url_for('all_customers'))
        return render_template('new_customer.html', form=form, edit=True, customer=customer)
