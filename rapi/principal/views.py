# coding=utf-8
from cStringIO import StringIO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from reportlab.lib.pagesizes import A4, cm
from reportlab.platypus import Paragraph, Table, TableStyle
from models import Atencion , Personal, Puesto, Edicion, Area, Cama, Paciente
from django.db.models import Count
from django.core import  serializers
from principal.forms import Login, CreateUser, CreatePaciente
from rapi import settings
from rapi.settings import BASE_DIR
from reportlab.lib.colors import Color, PCMYKColor, white
import PieChart, BarChart, ColumChart


@login_required
def visualizarListaAtenciones(request):

    ObjAtenciones = Atencion.objects.all()
    return render(request, "rapi/rapi_listatencion.html",locals())

def reporteGen(request):
    fecha_actual = datetime.date.today()
    USUARIO_ = request.user

    if(request.POST):
        seleccion = request.POST.get('sele1',0)
        if(seleccion == "1"):
            ATENCIONES = Atencion.objects.filter(TiempoA__day=fecha_actual.day)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=Reportedia-'+'.pdf'

            temp = BytesIO()
            # Create the PDF object, using the StringIO object as its "file."
            p = canvas.Canvas(temp,pagesize=A4)
            ancho,alto = A4
            #print ancho,alto
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'RAPH')

            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Registro de Atencion de Pacientes Hospitalizados')
            url_imagen_logo = BASE_DIR + '/principal/static/imagenes/logo_essalud.jpg'
            p.drawImage( url_imagen_logo,440,690,width=110,height=110)

            p.line(30,710,560,710)
            p.drawString(255,685,'REPORTE DEL DIA')
            p.drawString(30,660,'Nombre de Usuario:')
            p.drawString(30,630,'Fecha de Emision:')
            p.drawString(30,600,'Cantidad de Atenciones:')
            p.drawString(420,660,USUARIO_.username)
            p.drawString(420,630,str(fecha_actual))
            p.drawString(420,600,str(ATENCIONES.count()))
            p.setStrokeColor(black)
            p.setFont('Helvetica-Bold',16)
            p.drawString(30,570,"Tabla de Atenciones")
            p.setFont('Helvetica',14)
            p.drawString(30,530,"Atendidos = A")
            p.drawString(30,515,"No Atendidos = N")

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.line(30, 65,560,65)
            p.drawString(30,50,"Reporte del Dia: " + str(format(fecha_actual,"%d-%m-%y"))+" - Registro de Atencion de Pacientes Hospitalizados")

            styles = getSampleStyleSheet()
            styleBH = styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10

            numero_rapi = Paragraph('''Nro''', styleBH)
            cama_rapi = Paragraph('''Cama''', styleBH)
            hora_rapi = Paragraph('''Hora''', styleBH)
            perso_rapi = Paragraph('''Personal''', styleBH)
            edi_rapi = Paragraph('''Nro Ediciones''', styleBH)
            esta_rapi = Paragraph('''Estado''', styleBH)

            data = []

            data.append([numero_rapi, cama_rapi, hora_rapi, perso_rapi, edi_rapi, esta_rapi])

            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7

            high = 480
            this_atencion = None
            for Natencion in ATENCIONES:
                # try:
                #     personal_seleccionado = Personal.objects.get(id=Natencion.ID_P)
                # except Exception as e:
                #     personal_seleccionado ="No se asigno un profesional a la atencion"
                estado = None
                if Natencion.Estado==True:
                    estado = "A"
                else:
                    estado = "N"
                Ediciones_total = 0
                list_ediciones = Edicion.objects.filter(idAtencion=Natencion)
                for edi in list_ediciones:
                    Ediciones_total += edi.TotalE
                try:
                    this_atencion = [Natencion.id,Natencion.NroCamaA.Nro_Cama,format(Natencion.TiempoA.time(),"%H:%M:%S"),
                             Natencion.ID_P.NombreS + ", " + Natencion.ID_P.ApellidoS,Ediciones_total,estado]
                except Exception as e:
                    this_atencion = [Natencion.id,Natencion.NroCamaA.Nro_Cama,format(Natencion.TiempoA.time(),"%H:%M:%S"),
                             "No se registro nadie",Ediciones_total,estado]

                # try:
                #     this_atencion = [Natencion.id,Natencion.NroCamaA,Natencion.TiempoA.hour,
                #              personal_seleccionado.NombreS + ", " + personal_seleccionado.ApellidoS,Natencion.DescripcionA,
                #              Natencion.NroEdiciones,estado]
                # except Exception as e:
                #     this_atencion = [Natencion.id,Natencion.NroCamaA,Natencion.TiempoA.hour,
                #              "No se registro nadie","Esta campo se considera no registrado tambien",
                #              Natencion.NroEdiciones,estado]
                data.append(this_atencion)
                high = high -25

            table = Table(data, colWidths=[1*cm,1.4*cm,2*cm,4.5*cm,1.7 *cm,1.6*cm])
            table.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0),(-1,-1), 0.25, colors.black), ]))
            table.wrapOn(p,ancho,alto)
            table.drawOn(p,30,high)

            p.showPage()
            p.save()
            newpdf=temp.getvalue()
            temp.close()
            # Get the value of the StringIO buffer and write it to the response.
            response.write(newpdf)
            return response

        if(seleccion == "2"):
            MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                     "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            ATENCIONES = Atencion.objects.filter(TiempoA__month=fecha_actual.month).order_by('-NroCamaA')
            try:
                ATENCIONES_MES1 = Atencion.objects.filter(TiempoA__month=fecha_actual.month-1).order_by('-NroCamaA')
            except Exception as e:
                ATENCIONES_MES1 = None

            # ATENCIONES2 = Atencion.objects.annotate(NroAtenciones = Count('NroCamaA'))[:5]
            ATENCIONES2 = Atencion.objects.filter(TiempoA__month=fecha_actual.month).values('NroCamaA').annotate(Total=Count('NroCamaA_id')).order_by('-Total')[:5]
            ATENCIONES3 = Atencion.objects.filter(TiempoA__month=fecha_actual.month).values('Nombre_U').annotate(Total=Count('Nombre_U')).order_by('-Total')
            #print ATENCIONES3

            #CAMAS = Cama.objects.all().order_by('id')
            USUARIOS = User.objects.all()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=ReporteMes-'+'.pdf'

            temp = BytesIO()
            # Create the PDF object, using the StringIO object as its "file."
            p = canvas.Canvas(temp,pagesize=A4)
            ancho,alto = A4
            #print ancho,alto
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'RAPH')

            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Registro de Atencion de Pacientes Hospitalizados')
            url_imagen_logo = BASE_DIR + '/principal/static/imagenes/logo_essalud.jpg'
            p.drawImage( url_imagen_logo,440,690,width=110,height=110)

            p.line(30,710,560,710)
            p.drawString(255,685,'REPORTE DEL MES')
            p.drawString(30,660,'Nombre de Usuario:')
            p.drawString(30,630,'Fecha de Emision:')
            p.drawString(30,600,'Cantidad de Atenciones:')
            p.drawString(420,660,USUARIO_.username)
            p.drawString(420,630,str(fecha_actual))
            p.drawString(420,600,str(ATENCIONES.count()))
            p.setStrokeColor(black)
            p.setFont('Helvetica-Bold',16)
            p.drawString(255,570,"Estadisticas")





            if ATENCIONES_MES1 is None:
                p.setFont('Helvetica',14)
                p.drawString(235,545,"TOTAL DE ATENCIONES")
                cant_atendidos , cant_noatendidos = 0,0
                for atencioN in ATENCIONES:
                    if atencioN.Estado == True:
                       cant_atendidos+=1
                    else:
                       cant_noatendidos+=1
                PIE_CHART = PieChart.PieChart02()
                PIE_CHART.width = 200
                PIE_CHART.height = 200
                PIE_CHART.pie.data = [cant_atendidos,cant_noatendidos]
                PIE_CHART.pie.slices[0].fillColor = PCMYKColor(100,0,90,50,alpha=100)
                PIE_CHART.pie.slices[1].fillColor = PCMYKColor(0,100,100,40,alpha=100)
                PIE_CHART.legend.colorNamePairs = [(PCMYKColor(100,0,90,50,alpha=100), ('Atendidos', str(cant_atendidos))), (PCMYKColor(0,100,100,40,alpha=100), ('No Atendidos', str(cant_noatendidos)))]
                PIE_CHART.drawOn(p,50,320)
            else:

                COLUMN_CHART = ColumChart.ColumChart()
                COLUMN_CHART.width = 200
                COLUMN_CHART.height = 200
                cant_atendidos1, cant_noatendidos1 = 0,0
                cant_atendidos2, cant_noatendidos2 = 0,0
                for atencioN in ATENCIONES:
                    if atencioN.Estado == True:
                       cant_atendidos1+=1
                    else:
                       cant_noatendidos1+=1
                for atencioN2 in ATENCIONES_MES1:
                    if atencioN.Estado == True:
                       cant_atendidos2+=1
                    else:
                       cant_noatendidos2+=1
                MES_ACTUAL = fecha_actual.month
                MES_PASADO = fecha_actual.month-1
                if MES_PASADO == 0:
                    MES_PASADO = 12
                COLUMN_CHART.chart.seriesNames ="Atendidos","No Atendidos"
                COLUMN_CHART.chart.data = [[cant_atendidos1,cant_atendidos2],[cant_noatendidos1,cant_noatendidos2]]
                COLUMN_CHART.chart.titleText = "Comparacion de Atenciones con el mes Anterior"
                COLUMN_CHART.chart.categoryNames = (MESES[MES_ACTUAL-1],MESES[MES_PASADO-1])
                COLUMN_CHART.drawOn(p,100,340)
            BAR_CHART = BarChart.BarChart04()

            # BAR_CHART.x = 30
            # BAR_CHART.y = 540
            BAR_CHART.width = 200
            BAR_CHART.height = 200
            # PIE_CHART.x = 30
            # PIE_CHART.y = 320
            p.setFont('Helvetica',14)
            p.drawString(195,310,"CAMAS CON MAYOR CANTIDAD DE ATENCIONES")
            CAMAS = []
            DATOS_CAMA = []
            for id_cama in ATENCIONES2:
                id_temporal = id_cama['NroCamaA']
                cama_sel = Cama.objects.get(id=id_temporal)
                CAMAS.append("Cama Nro: " + str(cama_sel.Nro_Cama))
                DATOS_CAMA.append(id_cama['Total'])
            BAR_CHART.chart.data = [DATOS_CAMA]
            BAR_CHART.chart.categoryAxis.categoryNames = CAMAS
            BAR_CHART.chart.bars[0].fillColor = PCMYKColor(100,60,0,50,alpha=100)
            BAR_CHART.chart.bars[1].fillColor = PCMYKColor(100,0,90,50,alpha=100)
            BAR_CHART.drawOn(p,100,120)


            # DRAW_CHART.wrapOn(p,ancho,alto)
            # DRAW_CHART.drawOn(p,30,540)

            p.showPage()
            #AQUI EMPIEZA LA OTRA PAGINA DEL REPORTE
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'RAPH')

            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Registro de Atencion de Pacientes Hospitalizados')
            url_imagen_logo = BASE_DIR + '/principal/static/imagenes/logo_essalud.jpg'
            p.drawImage( url_imagen_logo,440,690,width=110,height=110)
            p.line(30,710,560,710)

            p.setFont('Helvetica',14)
            p.drawString(235,545,"TOTAL DE REGISTROS POR USUARIO")

            PIE_CHART2 = PieChart.PieChart02()
            list_colors= [PCMYKColor(100,67,0,23,alpha=100), PCMYKColor(70,46,0,16,alpha=100), PCMYKColor(50,33,0,11,alpha=100), PCMYKColor(30,20,0,7,alpha=100), PCMYKColor(20,13,0,4,alpha=100), PCMYKColor(10,7,0,3,alpha=100), PCMYKColor(0,0,0,100,alpha=100), PCMYKColor(0,0,0,70,alpha=100), PCMYKColor(0,0,0,50,alpha=100), PCMYKColor(0,0,0,30,alpha=100), PCMYKColor(0,0,0,20,alpha=100), PCMYKColor(0,0,0,10,alpha=100)]
            USERS_ARRAY = []
            PIE_CHART2.pie.data = []
            PIE_CHART2.legend.colorNamePairs = []
            for UsuarioTemp in ATENCIONES3:
                id_temporal = UsuarioTemp['Nombre_U']
                if id_temporal is None:
                    break
                usuario_sel = User.objects.get(id=id_temporal)
                if usuario_sel.is_active:
                    USERS_ARRAY.append(str(usuario_sel.username))
                    PIE_CHART2.pie.data.append(UsuarioTemp['Total'])
            PIE_CHART2.legend.colorNamePairs = []

            for i in range(len(PIE_CHART2.pie.data)):
                try:
                    PIE_CHART2.pie.slices[i].fillColor = list_colors[i]
                    PIE_CHART2.legend.colorNamePairs.append((list_colors[i],(USERS_ARRAY[i],str(PIE_CHART2.pie.data[i]))))
                except Exception as e:
                    break
            # PIE_CHART2.pie.slices[0].fillColor = PCMYKColor(100,0,90,50,alpha=100)
            # PIE_CHART2.pie.slices[1].fillColor = PCMYKColor(0,100,100,40,alpha=100)
            # PIE_CHART2.legend.colorNamePairs = [(PCMYKColor(100,0,90,50,alpha=100), ('Atendidos', str(cant_atendidos))), (PCMYKColor(0,100,100,40,alpha=100), ('No Atendidos', str(cant_noatendidos)))]
            PIE_CHART2.drawOn(p,50,420)

            styles = getSampleStyleSheet()
            styleBH = styles["Normal"]
            styleBH.alignment = TA_CENTER
            styleBH.fontSize = 10

            cabecera1 = Paragraph('''INFORMACION''', styleBH)
            cabecera2 = Paragraph('''DATOS RESALTANTES''', styleBH)

            data = []
            data.append([cabecera1, cabecera2])

            styleN = styles["BodyText"]
            styleN.alignment = TA_CENTER
            styleN.fontSize = 7

            high = 400

            #DATOS RESALTANTES
            #Cantidad de datos en las am
            Atenciones_7am1 = Atencion.objects.filter(TiempoA__month=fecha_actual.month,TiempoA__hour__gte=7,
                                                      TiempoA__hour__lt=13)
            Atenciones_1pm7 = Atencion.objects.filter(TiempoA__month=fecha_actual.month,TiempoA__hour__gte=13,
                                                      TiempoA__hour__lt=19)
            Atenciones_7pm7 = Atencion.objects.filter(TiempoA__month=fecha_actual.month,TiempoA__hour__gte=19,
                                                      TiempoA__hour__lt=7)
            MEJOR_PERSONAL = Atencion.objects.filter(TiempoA__month=fecha_actual.month).values('ID_P').annotate(Total=Count('ID_P')).order_by('-Total')[:1]

            REGISTRO_MOD = Edicion.objects.filter(TiempoE__month=fecha_actual.month).order_by('-TotalE')[:1]

            CAM_POCAS_ATEN = Atencion.objects.filter(TiempoA__month=fecha_actual.month).values('NroCamaA').annotate(Total=Count('NroCamaA_id')).order_by('Total')[:5]

            data.append(["Total de Atenciones durante el turno 7:00 am - 1:00 pm",Atenciones_7am1.count()])
            high -= 45
            data.append(["Total de Atenciones durante el turno 1:00 pm - 7:00 pm",Atenciones_1pm7.count()])
            high -= 45
            data.append(["Total de Atenciones durante el turno 7:00 pm - 7:00 am",Atenciones_7pm7.count()])
            high -= 45
            Persona_seleccionada = Personal.objects.get(id=MEJOR_PERSONAL[0]["ID_P"])
            data.append(["Personal que mas atendio a los pacientes",str(Persona_seleccionada.NombreS)
                         + "," + str(Persona_seleccionada.ApellidoS)+ ": "+ str(MEJOR_PERSONAL[0]["Total"])])
            high -= 45

            atencion_seleccionada = Atencion.objects.get(id=REGISTRO_MOD[0].idAtencion.id)
            data.append(["Registro de Atencion mas Editado o Modificado","Registro Nro: " + str(atencion_seleccionada.id)
                         + "\n Cama: " + str(atencion_seleccionada.NroCamaA.Nro_Cama)
                         + "\n Registrada el: " + str(atencion_seleccionada.TiempoA)
                         + "\n Total de Ediciones: " + str(REGISTRO_MOD[0].TotalE)])
            high -= 45
            tabla = Table(data, colWidths=[10*cm,8*cm])
            tabla.setStyle(TableStyle([('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0),(-1,-1), 0.25, colors.black), ]))
            tabla.wrapOn(p,ancho,alto)
            tabla.drawOn(p,30,high)

            p.save()
            newpdf=temp.getvalue()
            temp.close()
            # Get the value of the StringIO buffer and write it to the response.
            response.write(newpdf)
            return response
        else:
            return render(request, "rapi/rapi_reportes.html")

    return render(request, "rapi/rapi_reportes.html")

@login_required
def visualizarPrincipal(request):
    return render(request, "rapi/rapi_principal.html")


def visualizarLogin(request):
    # next = request.GET.get('next', '/index/')
    if(request.method=='POST'):
        usuario = request.POST['username']
        contra = request.POST['password']
        #form = Login(request.POST)
        # if form.is_valid():
        #     usuario = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        acceso = authenticate(username=usuario,password=contra)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return HttpResponseRedirect('/index')
            else:
                return HttpResponse('usuario inactivo.')
                    # ("rapi/rapi_login.html", context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    # else:
    #     form = Login
    return render(request,"rapi/rapi_login.html")

def Logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def visualizarAlertas(request):
    personal = Personal.objects.all()
    alertas = Atencion.objects.filter(Estado=False,ID_P=None,Nombre_U=None)
    return render(request, "rapi/rapi_ALERTAS.html",locals())

@login_required
def visualizarReporte(request):
   return render(request, "rapi/rapi_reportes.html")


def visualizarAlertasAjax(request):
    datos =""
    if(request.GET):
        id_personal = request.GET['id']
        persona = Personal.objects.values(id_personal)
        datos = serializers.serialize('json',persona,fields=('NombreS','ApellidoS'))
    return HttpResponse(datos,content_type="application/json")


def editaralertas1(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    # if request.POST:
    #     if request.POST['atendido']:
    atencion.Nombre_U = request.user
    atencion.Estado = True
    #edition_created= Edicion.objects.create(TiempoE=timezone.now(),TotalE=1,IdUsuarios=request.user,idAtencion=atencion)
    atencion.save()
    return redirect(reverse('alertas2',kwargs={'pk':pk}))
    # else:
    #         return redirect(reverse('alertas'))
    # return render(request, 'rapi/rapi_ALERTAS.html')


def editaralertas2(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    # if request.POST:
    #     if request.POST['atendido']:
    atencion.Nombre_U = request.user
    #edition_created= Edicion.objects.create(TiempoE=timezone.now(),TotalE=1,IdUsuarios=request.user,idAtencion=atencion)
    atencion.save()
    return redirect(reverse('alertas2',kwargs={'pk':pk}))

@login_required
def editarAlertas(request, pk):
    atencion = Atencion.objects.get(pk=pk)
    personal = Personal.objects.all()
    current_edition = None
    try:
        current_edition = Edicion.objects.get(IdUsuarios=request.user, idAtencion=atencion)
    except Exception as e:
        current_edition = None
    if current_edition is None:
        current_created = Edicion.objects.create(TiempoE=timezone.now(),TotalE=0,IdUsuarios=request.user,idAtencion=atencion)
    if request.POST:
        try:
            id_personal = int(request.POST.get('id-personal',None))
        except Exception as e:
            id_personal = None
        if(id_personal>0):
            personal_atendio = Personal.objects.get(id=id_personal)
            atencion.ID_P = personal_atendio
        atencion.DescripcionA = request.POST.get('descripcion-atencion',None)
        atencion.save()
        if current_edition is not None:
            suma = current_edition.TotalE + 1
            current_edition.TotalE = suma
            current_edition.TiempoE = timezone.now()
            current_edition.save()
        return redirect(reverse('alertas'))
    else:
        return render(request, "rapi/rapi_editalertas.html",locals())


def reporteAjax(request):
    if(request.method == 'POST'):
        fecha_actual = datetime.datetime.now()
        # inicio_semana = timezone.now() - datetime.timedelta(days=7)
        # fin_semana= timezone.now()
        opcion = request.POST['seleccion']
        atencionesD=0
        # atencionesS=0
        atencionesM=0
        dato1=None

        if(opcion=="1"):
            atencionesD = Atencion.objects.filter(TiempoA__day=fecha_actual.day)
            dato1 = serializers.serialize('json',atencionesD)
        # if(opcion=="2"):
        #     atencionesS = Atencion.objects.filter(TiempoA__range=[inicio_semana,fin_semana])
        #     dato1 = serializers.serialize('json',atencionesS)
        if(opcion=="2"):
            atencionesM = Atencion.objects.filter(TiempoA__month=fecha_actual.month)
            dato1 = serializers.serialize('json',atencionesM)
        # atenciones1 = Atencion.objects.filter(TiempoA__lte=datetime.date.today())
        return HttpResponse(dato1,content_type='application/json')

def AdministradorView(request):
    return render(request,'rapi/rapi_admin.html')


def CrearUsuarioView(request):
    mensaje = ""
    if(request.POST):
        createuserform = CreateUser(request.POST)
        if(createuserform.is_valid()):
            createuserform.save()
            mensaje = "Usuario creado con exito"
            return render(request,'rapi/rapi_admin.html',locals())
        else:
            mensaje = "Error al crear un Usuario, intente nuevamente"
            return render(request,'rapi/rapi_admin.html',locals())
    else:
        createuserform = CreateUser()
    return render(request,'rapi/rapi_crearuser.html',locals())

def busquedaView(request):
    return render(request,'rapi/rapi_busquedaA.html')

def BusquedaResult(request):
    atencion,EdicionesxUser,Totalediciones,Last_Time = "","","",""
    if request.POST:
        ID= request.POST["IDATENCION"]
        try:
            atencion = Atencion.objects.get(id=ID)
            EdicionesxUser = Edicion.objects.filter(idAtencion=atencion).order_by('-TiempoE')
        except Exception as e:
            return render(request,'rapi/rapi_busquedaA.html')
        Totalediciones = 0
        try:
            Last_Time = EdicionesxUser[0].TiempoE
            for edicion in EdicionesxUser:
                Totalediciones += edicion.TotalE
        except Exception as e:
            Last_Time = atencion.TiempoA
            Totalediciones = 1
        return render(request,'rapi/rapi_busquedaResult.html',locals())
    return render(request,'rapi/rapi_busquedaResult.html',locals())
def cambiarpswView(request):
    users = User.objects.all()
    message_confirm = ""
    return render(request,'rapi/rapi_psw.html',locals())


def informacionUserView(request):
    users = User.objects.all()
    return render(request,'rapi/rapi_infouser.html',locals())


def ImprimirInformacion(request):
    pass


def cambiarpswViewR(request,pk):
    usuario = User.objects.get(pk=pk)
    if request.POST:
        if request.POST["password"] and request.POST["password2"]:
            pass1 = request.POST["password"]
            pass2 = request.POST["password2"]
            if pass1 == pass2:
                if usuario.is_active:
                    usuario.set_password(pass1)
                    usuario.save()
                    message_confirm = "Se cambio correctamente la contraseña, por su seguridad, recuerde que no debe brindarla a nadie."
                    users = User.objects.all()
                    return render(request,'rapi/rapi_psw.html',locals())
                else:
                    message_confirm = "El usuario se encuentra inactivo, no se puede cambiar de contraseña "
            else:
                message_confirm = "Las contraseñas no coinciden, intente nuevamente"
        else:
            message_confirm = "Ingrese la contraseña que desea cambiar en ambos campos"
    return render(request,'rapi/rapi_pswR.html',locals())


def informacionUserViewR(request):
    if request.POST:
        iduser=request.POST["seleccion"]
        usuarioseleccionado = User.objects.filter(pk=iduser)
        userinfo = serializers.serialize('json',usuarioseleccionado)
        print "convirtio"
        # registros = Edicion.objects.filter(IdUsuarios_id=usuarioseleccionado)
        # registros_editados = registros.count()
        # registros2 =Atencion.objects.filter(Nombre_U_id=usuarioseleccionado)
        # registros_manejados = registros2.count()
        # informaciontotal = [registros_editados,registros_manejados]
        # registros_cont = serializers.serialize('json',informaciontotal)
        return HttpResponse(userinfo,content_type='application/json')
    return HttpResponse("Error no selecciono ningun usuario")


def busquedaViewAjax(request):
    pass


def IngresoPaciente(request):
    mensaje = ""
    if(request.POST):
        ingresarpacienteform = CreatePaciente(request.POST)
        if ingresarpacienteform.is_valid():
            DNI = ingresarpacienteform.cleaned_data['Dni_P']
            DNI = ingresarpacienteform.clean_dni(DNI)
            try:
                pacientenuevo = Paciente.objects.get(Dni_P=DNI)
                mensaje = "El paciente ya esta registrado"
                return render(request,'rapi/rapi_ingresopaciente.html',locals())
            except Exception as e:
                ingresarpacienteform.save()
                pacientenuevo = Paciente.objects.get(Dni_P=DNI)
                pacientenuevo.Fecha_Ingreso = timezone.now()
                pk = pacientenuevo.id
                mensaje = "Nuevo paciente ingresado con exito"
                return redirect(reverse('asignarpaciente'),kwargs={'pk':pk})
        else:
            mensaje = "Error al ingresar un Paciente, intente nuevamente"
            return render(request,'rapi/rapi_pacientes.html',locals())
    else:
        ingresarpacienteform = CreatePaciente()
    return render(request,'rapi/rapi_ingresopaciente.html',locals())



def AsignarPaciente(request,pk):
    Areas = Area.objects.all()
    paciente_nuevo = Paciente.objects.get(pk=pk)
    return render(request,'rapi/rapi_asignarcama.html',locals())


def SalidaPaciente(request):
    return render(request,'rapi/rapi_salidapaciente.html')


def PacienteView(request):
    return render(request,'rapi/rapi_pacientes.html')


def SeleccionarCama(request):
    pass


def AsignarPaciente2(request,pk):
    if(request.POST):
        idarea = request.POST["areaselect"]
        CAMAS = Cama.objects.filter(Area=idarea)
        Estados_Cama = []
        for estadocama in CAMAS:
            if estadocama.EstadoC is False:
                Estados_Cama.append(0)
            else:
                Estados_Cama.append(1)
        paciente = Paciente.objects.get(pk=pk)
        return render(request,'rapi/rapi_asignarcama2.html',locals())
    else:
        return redirect(reverse('asignarpaciente'))
    return render(request,'rapi/rapi_pacientes.html')