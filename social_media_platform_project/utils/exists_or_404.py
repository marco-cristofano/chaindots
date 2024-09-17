from django.http import Http404


def exists_object_or_404(model, id: int) -> bool:
    """
    Return True if object exists or raise 404 error.
    args:
        model: model class
        id: id of object
    return:
        bool: true if object exists
    """
    exists = model.objects.filter(id=id).exists()
    if exists:
        return True
    raise Http404('No %s matches the given query.' % model._meta.object_name)
