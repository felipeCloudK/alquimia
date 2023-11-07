
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
from .forms import CalendarioForm, CustomUserCreationForm, InventarioForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import  AuthenticationForm
from django.db.models import Q
from AlquimiaApp.models import Calendario, Inventario, User 
import sweetify
from django.shortcuts import render
from datetime import date

fecha_actual = date.today()

#inicio de sesion
def Login(request):
    if request.user.is_authenticated:
        if request.user.is_administrador:
            return redirect('/Organizacion/')
        if request.user.is_chef:
            return redirect('usuarios/lista/')

    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                sweetify.error(request,f'El usuario o la contraseña ingresada son incorrectas')
            if form.is_valid():
                login(request,user)
                first_name=form.cleaned_data['username']
                sweetify.success(request,f'Bienvenido {first_name} a la aplicación ')
                if request.user.is_administrador:
                    return redirect('Organizacion/')
                if request.user.is_chef:
                    return redirect('usuarios/lista/')
    data = {'form' : form , 'title':'Iniciar Sesión'}
    return render(request, 'Home.html',data)  


def SignOut(request):
    logout(request)
    return redirect('/')

#usuarios

def crear_usuario(request):
# if request.user.is_authenticated:
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try: 
                form.save()
                first_name=form.cleaned_data['first_name']
            
                sweetify.success(request, f'Usuario {first_name} ha sido creado correctamente')
                form = CustomUserCreationForm()
                return redirect("../../usuarios/crear/")
            except:
                sweetify.error(request,f'El usuario no se pudo crear') 
    else:
        form=CustomUserCreationForm()
# else:
#     return redirect('/')

    data = {'form' : form , 'title':'Registrar nuevo usuario','button': 'Registrar','fechaHoy':fecha_actual}
    return render(request, 'Administrador/crear_usuario.html',data)

def ver_usuario(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        fecha=users.filter(date_joined = fecha_actual)
        activo = users.filter(is_active='True')
        inactivo = users.filter(is_active='False')
        totalActivo=activo.count()
        totalInactivo=inactivo.count()
        registroTotal = users.count()
        registroTotalHoy = fecha.count()
        data = {'users':users,'fechaHoy':fecha_actual,'registroTotal':registroTotal,'registroTotalHoy':registroTotalHoy,'inactivo':totalInactivo,'activo':totalActivo}
        return render(request, 'Administrador/lista_usuario.html',data)
    else:
        return redirect('/')
    
def Searcher(request):
    if request.user.is_authenticated:
        search = request.GET['busemp']
        users = User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) 
                                | Q(date_joined__icontains=search) | Q(username__icontains=search)
                                | Q(is_administrador__icontains=search) | Q(is_chef__icontains=search))
        data={'users':users}
        return render(request, 'Administrador/lista_usuario.html',data)
    else:
        return redirect('/')
  
def editar_usuario(request, id):
    if request.user.is_administrador:
        user = User.objects.get(id=id)
        form = CustomUserCreationForm(instance=user)
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, instance=user)
            try:
                form.save()
                first_name = form.cleaned_data['first_name']
                sweetify.success(request, f'Usuario {first_name} ha sido actualizado correctamente')
                return redirect('../usuarios/lista/')
            except Exception as e:
                print(str(e))  # Imprime el error para depuración
                sweetify.error(request, f'El usuario no se pudo actualizar: {str(e)}')
        data = {'form': form, 'title': 'Actualizar usuario', 'button': 'actualizar','fechaHoy':fecha_actual}
        return render(request, 'Administrador/crear_usuario.html', data)
    else:
        sweetify.error(request, f'Usuario incorrecto')
    return redirect('/')

def UserDelete(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        try:
            # user.is_administrador = False
            # user.is_chef = False
            user.delete()
            sweetify.success(request,f'Usuario desactivado exitosamente!')
        except:
            sweetify.error(request, f'El usuario no se pudo desactivar') 
        return redirect('../usuarios/lista/')
    else:
        return redirect('/')


          


# ORGANIZACION

class OrganizacionView(View):
    template_name = 'Organizacion/Organigrama.html'

    def get(self, request):
        if request.user.is_authenticated:
            date = Calendario.objects.all()
            registrosHoy=date.filter(start_time__date=fecha_actual)
            insumo = Inventario.objects.all()
            form = CalendarioForm()
            registrosTotales=date.count()
            registrosTotalesHoy=registrosHoy.count()
            porcionesTotalBodega=0
            porcionesUtilizadasTotal=0
            
            for registro in registrosHoy:
                if registro.Porciones is not None:
                    porcionesUtilizadasTotal += registro.Porciones
                    
            for item in insumo:
                porcionesTotalBodega += item.porciones_disponibles
         
             
            context = {'date': date, 'form': form, 'title': 'Registrar evento', 'button': 'Registrar','fechaHoy':fecha_actual,
                       'porcionesTotal':porcionesTotalBodega,'porcionesUtilizadasTotal':porcionesUtilizadasTotal
                       ,'registrosTotales':registrosTotales,'registrosHoy':registrosTotalesHoy}
            return render(request, self.template_name, context)
        else:
            return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            form = CalendarioForm(request.POST)
            if form.is_valid():
                try:
                    instance = form.save()
                    Nombre = instance.nombre
                    sweetify.success(request, f'El evento {Nombre} ha sido creado correctamente')
                    form = CalendarioForm()
                    return redirect('/Organizacion/')  # Puedes usar reverse aquí si tienes una URL nombrada
                except Exception  as e:
                    sweetify.error(request, f'El evento no se pudo crear {str(e)}')
            date = Calendario.objects.all()
            context = {'date': date, 'form': form, 'title': 'Registrar evento', 'button': 'Registrar','fecha_actual':fecha_actual}
            return render(request, self.template_name, context)
        else:
            return redirect('/')
    

#Inventario


def crear_inventario(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = InventarioForm(request.POST)
            if form.is_valid():
                try: 
                    form.save()
                    sweetify.success(request, f'El insumo se registró correctamente')
                    form = InventarioForm()
                    return redirect("../../Inventario/crear/")
                except:
                    sweetify.error(request, f'El insumo no se pudo crear') 
        else:
            form = InventarioForm()
    else:
        return redirect('/')  # Redirect to the appropriate URL

    data = {'form' : form , 'title':'Registrar nuevo platillo','button': 'Registrar','fechaHoy':fecha_actual}
    return render(request, 'Bodega/Agregarinventario.html',data)

  
def ver_inventario(request):
    if request.user.is_authenticated:
        insumo = Inventario.objects.all()
        insumosTotal = insumo.count()
        insumosHoy = insumo.filter(fecha = fecha_actual)
        porcionesTotal = 0
        dineroTotal = 0
        for item in insumo:
            porcionesTotal += item.porciones_disponibles
            dineroTotal += item.precio
            
        insumosTotalHoy = insumosHoy.count()
        data = {'insumo':insumo , 'insumosTotal':insumosTotal,'insumosHoy':insumosTotalHoy,
                'fechaHoy':fecha_actual,'porcionesTotal':porcionesTotal,'dineroTotal':dineroTotal}
        return render(request, 'Bodega/listaInsumo.html',data)
    else:
        return redirect('/')    