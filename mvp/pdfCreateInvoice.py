from datetime import datetime, date
from django.core.files import File

from .pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from .pyinvoice.templates import SimpleInvoice
import os


def CreatePDFInvoice(invoice, invoice_nb, facture_date, due_date):
    doc = SimpleInvoice('invoice.pdf')

    # Invoice info, optional
    doc.invoice_info = InvoiceInfo(
        invoice_id=invoice_nb,
        invoice_datetime=facture_date,
        due_datetime=due_date,
    )

    # Service Provider Info, optional
    doc.service_provider_info = ServiceProviderInfo(
        name=invoice.company.name,
        street='My Street',
        city='My City',
        country='My Country',
        post_code=' 75009',
        vat_tax_number=invoice.company.siret
    )

    client = invoice.contract.client
    # Client info, optional
    doc.client_info = ClientInfo(
        email=client.email,
        # email='client@example.com',
        name=client.name,
        street='27 rue Bleue',
        country='France',
    )

    # Add Item
    percent = invoice.price / invoice.contract.price
    for licence in (invoice.contract.license_set.all() or None):
        doc.add_item(Item('License', licence.description, 1,
                          int(percent * licence.price)))
    for conseil in (invoice.contract.conseil_set.all() or None):
        doc.add_item(Item('Prestation', conseil.description, 1,
                          int(percent * conseil.price)))

    # Tax rate, optional
    doc.set_item_tax_rate(20)  # 20%

    # Optional
    doc.set_bottom_tip("<br /><br /><br />N'hésitez pas à nous contacter.<br /> Email: %s" %
                       invoice.contract.factu_manager.user.email)

    doc.finish()
    f = open('invoice.pdf', 'rb')
    object_file = File(f)
    os.remove('invoice.pdf')
    return object_file