/**
 * Created by Jesus on 19/04/2016.
 */
$(document).ready(function() {
    	$('select').on('change','actualizar');
        function actualizar(){
            var id = $(this).val();
            $.ajax({
                data : {'id':id},
                url  : '/alertas-personal/',
                type : 'get',
                success: function(datos){
                    var personal_seleccionado = ""
                    personal_seleccionado = "El paciente fue atendido por: " + datos
                    $('#personal_sel').html(personal_seleccionado);
                }

            })

        }
	} );
