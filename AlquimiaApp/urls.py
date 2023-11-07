from django.urls import path
from .views import  (
    OrganizacionView, crear_usuario, ver_inventario,ver_usuario,editar_usuario,
    UserDelete,Searcher,Login,SignOut,crear_inventario
    )

urlpatterns = [
    # INICIO
    path('', Login , name='Inicio'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('usuarios/lista/', ver_usuario , name='ver_usuario'),
    path('editar/<int:id>',editar_usuario,name='editar'),
    path('UserDelete/<int:id>',UserDelete,name='userDelete'),
    path('Search/',Searcher,name='Search'),
    path('logout/',SignOut, name='logout'),
    
    # ORGANIZACIÓN
    path('Organizacion/', OrganizacionView.as_view(), name='organizacion'),
    
    #Bodega
    path('Inventario/', ver_inventario,name='ver_inventario'),
    path('Inventario/crear/', crear_inventario,name='crear_inventario'),

]
