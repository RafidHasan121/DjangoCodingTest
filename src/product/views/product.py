from turtle import title
from django.views import generic
from django.shortcuts import render
import product.models

def product_view(request):
    output1 = product.models.Product.objects.all()
    output3 = product.models.ProductVariantPrice.objects.all()
    output2 = product.models.ProductVariant.objects.all()
    print(output1[0].created_at)
    return render(request, 'products/list.html', {'p': output1, 'pv': output2, 'pvp': output3})
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = product.models.Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    
