$(document).ready(function(){
    // Función para enviar el formulario de recuperación de contraseña
    $("#passwordRecoveryForm").submit(function(e){
      e.preventDefault(); // Evitar que se recargue la página
      var email = $("#email").val(); // Obtener el correo electrónico del campo de entrada
      // Aquí puedes agregar código para enviar el correo electrónico de recuperación a la dirección proporcionada
      console.log("Correo electrónico enviado para recuperación a: " + email);
    });
  });