"""rapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^gen-reporte/$', 'principal.views.reporteGen',name='reportegen'),
    url(r'^reporte/', 'principal.views.visualizarReporte',name='reporte'),
    url(r'^login/$', 'principal.views.visualizarLogin', name='login'),
    url(r'^logout/$','principal.views.Logout',name='logout'),
    url(r'^informacion-reporte/$','principal.views.reporteAjax',name='reporteA'),
    url(r'^index/', 'principal.views.visualizarPrincipal',name='index'),
    url(r'^listatenciones/', 'principal.views.visualizarListaAtenciones',name='lista1'),
    url(r'^alertas/', 'principal.views.visualizarAlertas',name='alertas'),
    url(r'^editar-alertas/(?P<pk>.+)/$', 'principal.views.editarAlertas',name='alertas2'),
    url(r'^editar-alertas1/(?P<pk>.+)/$', 'principal.views.editaralertas1',name='editalertas1'),
    url(r'^editar-alertas2/(?P<pk>.+)/$', 'principal.views.editaralertas2',name='editalertas2'),
    url(r'^alertas-personal/', 'principal.views.visualizarAlertasAjax',name='alertas1'),
    url(r'^raph-admin/', 'principal.views.AdministradorView',name='raphadmin'),
    url(r'^newuser/', 'principal.views.CrearUsuarioView',name='newuser'),
    url(r'^busquedaA/', 'principal.views.busquedaView',name='busquedaA'),
    url(r'^busquedaR/', 'principal.views.BusquedaResult',name='busquedaResult'),
    url(r'^newpsw/', 'principal.views.cambiarpswView',name='newpsw'),
    url(r'^newpswR/(?P<pk>.+)/$', 'principal.views.cambiarpswViewR',name='newpswR'),
    url(r'^infouser/', 'principal.views.informacionUserView',name='infouser'),
    url(r'^infouserR/', 'principal.views.informacionUserViewR',name='infouserR'),
    url(r'^printinfo/', 'principal.views.ImprimirInformacion',name='printinfo'),
    url(r'^pacienteingreso/', 'principal.views.IngresoPaciente',name='ingresopaciente'),
    url(r'^pacienteasignar/(?P<pk>.+)/$', 'principal.views.AsignarPaciente',name='asignarpaciente'),
    url(r'^pacienteasignar2/(?P<pk>.+)/$', 'principal.views.AsignarPaciente2',name='asignarpaciente2'),
    url(r'^cama/', 'principal.views.SeleccionarCama',name='seleccionaracama'),
    url(r'^asignarcama/', 'principal.views.IngresarPacienteCama',name='asignarcama'),
    url(r'^pacientesalida/', 'principal.views.SalidaPaciente',name='salidapaciente'),
    url(r'^pacientes/', 'principal.views.PacienteView',name='menupaciente'),
    url(r'^listapaciente/', 'principal.views.ListaPaciente',name='listapaciente'),
    url(r'^salidapaciente/', 'principal.views.MarcarSalida',name='marcarsalida'),
]
