from django.shortcuts import render
from django.http import HttpResponse
from affiliation.models import Band, BlogPost
from affiliation.forms import ContactUsForm, BandForm
from django.core.mail import send_mail
from django.shortcuts import redirect


def band_list(request):
    bands = Band.objects.all()
    return render(request, 
                'affiliation/band_list.html',
                {'bands': bands})
def about(request):
    return render(request,
                'affiliation/about.html')

def band_detail(request, id):
    band = Band.objects.get(id=id)
    return render(request, 'affiliation/band_detail.html', {'band': band})#pass id to model

def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
            return redirect('band-list')  # ajoutez cette instruction de retour
    else:
        form = ContactUsForm()
    return render(request,
                'affiliation/contact.html',
                {'form':form})

def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band = form.save()
            return redirect('band-detail', band.id)
    else:
            form = BandForm()
    return render(request,
            'affiliation/band_create.html',
            {'form':form})


def band_update(request, id):
    band = Band.objects.get(id=id)
    form = BandForm(instance=band)
    return render(request, 'affiliation/band_update.html',
                    {'form':form})

def band_delete(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        band.delete()
        return redirect('band-list')
    return render(request,
                    'affiliation/band_delete.html',
                    {'band':band})

def home(request):
    posts = BlogPost.objects.all()
    return render(request, 
                'affiliation/blogpost_list.html',
                {'posts': posts})


def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    return render(request,
                'affiliation/blogpost_detail.html',
                {'post':post})