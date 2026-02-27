import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

@csrf_exempt
def product_api(request, pk=None):
    # CREATE (POST)
    if request.method == 'POST':
        root = ET.fromstring(request.body)
        item = Product.objects.create(
            name=root.find('name').text,
            category=root.find('category').text,
            price=root.find('price').text
        )
        return HttpResponse(f"<response><status>success</status><id>{item.id}</id></response>", content_type='application/xml')

    # READ (GET)
    elif request.method == 'GET':
        products = Product.objects.all()
        root = ET.Element("product_list")
        for p in products:
            node = ET.SubElement(root, "product")
            ET.SubElement(node, "id").text = str(p.id)
            ET.SubElement(node, "name").text = p.name
            ET.SubElement(node, "category").text = p.category
            ET.SubElement(node, "price").text = str(p.price)
        return HttpResponse(ET.tostring(root), content_type='application/xml')

    # UPDATE (PUT)
    elif request.method == 'PUT':
        root = ET.fromstring(request.body)
        Product.objects.filter(pk=pk).update(
            name=root.find('name').text,
            category=root.find('category').text,
            price=root.find('price').text
        )
        return HttpResponse("<response><message>Product Updated</message></response>", content_type='application/xml')

    # DELETE (DELETE)
    elif request.method == 'DELETE':
        Product.objects.filter(pk=pk).delete()
        return HttpResponse("<response><message>Product Deleted</message></response>", content_type='application/xml')