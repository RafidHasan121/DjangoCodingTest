from ast import And
from asyncio.windows_events import NULL
from turtle import title
from django.views import generic
from django.shortcuts import render
import product.models
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers

def product_view(request):
    try:
        output1 = request.session['output1']
        for obj in serializers.deserialize("json", output1):
            output1 = obj
        print(output1)
        output1 = product.models.Product.objects.filter(id = output1.val())
        print(output1)
    except:
        output1 = product.models.Product.objects.all()
    try:
        output2 = request.session['output2']
        for obj in serializers.deserialize("json", output2):
            output2 = obj
        print(output2)
        output2 = product.models.ProductVariant.objects.filter(id = output2.val())
        print(output2)
    except:
        output2 = product.models.ProductVariant.objects.all()
    
    output3 = product.models.ProductVariantPrice.objects.all()
    #print(output1[0].created_at)
    return render(request, 'products/list.html', {'p': output1, 'pv': output2, 'pvp': output3})

def product_search(request, title=None, variant=None, price_from=None, price_to=None, date=None):
    if (title != None):
        output1 = product.models.Product.objects.filter(title = title)
    elif( date != None):
        output1 = product.models.Product.objects.filter(created_at = date)
    else:
        output1 = product.models.Product.objects.all()
    if (variant != None):
        output2 = product.models.ProductVariant.objects.filter(variant_title = variant)
    else:
        output2 = product.models.ProductVariant.objects.all()
    if (price_from != None and price_to != None):
        pass
    print(output1)
    print(output2)
    output1 = serializers.serialize('json', output1)
    output2 = serializers.serialize('json', output2)
    request.session['output1'] = output1
    request.session['output2'] = output2

    return product_view(request)


def search(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        variant = request.POST.get('variant')
        price_from = request.POST.get('price_From')
        price_to = request.POST.get('price_to')
        date = request.POST.get('date')
    print(title, date)
    try:
        price_from = float(price_from)
        price_to = float(price_to)
    except:
        price_from = None
        price_to = None
    return product_search(request, title, variant, price_from, price_to, date)

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = product.models.Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    
