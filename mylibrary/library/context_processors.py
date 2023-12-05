from .views import menu


def get_menu(request):
    return {'mainmenu': menu}
