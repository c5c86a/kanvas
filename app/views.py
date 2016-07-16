from django.shortcuts import render
from django.views.generic import ListView, DetailView
from app.models import Canvas, Vote
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from app.forms import CanvasForm
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, Textarea, ClearableFileInput
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def company(request, pk):
    """
    This is function and not a generic view as it points to a different template from canvas_detail with less fields
    :param request:
    :param pk: primary key of Canvas as a named group of a regular expression at urls
    :return:
    """
    try:
        obj = Canvas.objects.get(pk=pk)
    except Canvas.DoesNotExist:
        raise Http404("Canvas does not exist")
    return render(request, 'app/company_detail.html', {'obj': obj})

@login_required
def update_field(request, pk, field):
    """
    This is function and not a CreateView/Update as it points to a template with less fields
    :param request:
    :param pk: primary key of Canvas
    :param field: which field to update
    :return:
    """
    widgets = {}
    if field=='logo':
        widgets[field] = ClearableFileInput()
    else:
        widgets[field] = Textarea(attrs={'rows':4, 'cols':150})
    CanvasForm = modelform_factory(Canvas, fields=(field,), widgets=widgets)
    if request.method == 'POST':
        form = CanvasForm(request.POST)
        if form.is_valid():
            obj = Canvas.objects.get(id=pk)
            if obj.originalauthor == request.user: # more maintainable than dfunckt/django-rules
                if 'logo' in request.FILES:
                    data = ContentFile(request.FILES['logo'].file.read())
                    filename = request.FILES['logo'].name
                    form.cleaned_data['logo'] = filename
                    default_storage.save(filename, data)
                setattr(obj, field, form.cleaned_data[field])
                obj.save()
                return HttpResponseRedirect('/canvas/'+pk)
            else:
                return HttpResponseRedirect('/login/')
    else:
        form = CanvasForm(instance = Canvas.objects.get(id=pk))

    return render(request, 'app/canvas_form.html', {'formfield': form})


def voteup(request, pk):
    return do(request, pk, 'upvotes')


def votedown(request, pk):
    return do(request, pk, 'downvotes')


def do(request, pk, vote):
    """
    :param request:
    :param pk: primary key of Canvas
    :param field: which field to update
    :return: response accessible with AJAX
    """
    result = {}
    if vote=='downvotes':
        opposite = 'upvotes'
        act = -1
    else:
        opposite = 'downvotes'
        act = 1
    obj = Canvas.objects.get(id=pk)   # decorator login_required would redirect
    if request.user.is_authenticated():         # else do nothing
        votes = Vote.objects.filter(voter=request.user, canvas=obj)
        if votes:
            if votes.filter(act=-act):           # else do nothing
                setattr(obj, vote, getattr(obj, vote) + 1)
                value = getattr(obj, opposite) - 1
                setattr(obj, opposite, value)
                obj.save()
                votes.update(act=act)
                result[opposite] = value
        else:
            setattr(obj, vote, getattr(obj, vote) + 1)
            obj.save()
            Vote.objects.create(voter=request.user, canvas=obj, act=act)
    result[vote] = getattr(obj, vote)
    return JsonResponse(result)

@login_required
def create_canvas(request):
    """
    This is function and not a CreateView/Update as it points to a template with less fields
    :param request:
    :param pk: primary key of Canvas
    :param field: which field to update
    :return:
    """
    if request.method == 'POST':
        form = CanvasForm(request.POST)
        if form.is_valid():
            form.cleaned_data['originalauthor'] = request.user
            if 'logo' in request.FILES:
                data = ContentFile(request.FILES['logo'].file.read())
                filename = request.FILES['logo'].name
                form.cleaned_data['logo'] = filename
                default_storage.save(filename, data)
            obj = Canvas.objects.create(**form.cleaned_data)
            return HttpResponseRedirect("/canvas/%d" % obj.id)
    else:
        form = CanvasForm() # blank form

    return render(request, 'app/canvas_new.html', {'company': form['company'],'description': form['description'],'logo': form['logo']})


class CanvasList(ListView):
    """
    For debugging, check as_view() http://ccbv.co.uk/projects/Django/1.8/django.views.generic.list/ListView/
    """
    model = Canvas


class CanvasDetailView(DetailView):
    model = Canvas


class CanvasDelete(DeleteView):
    model = Canvas
    success_url = reverse_lazy('canvas-list')

