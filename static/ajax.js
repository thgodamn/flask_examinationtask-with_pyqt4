//обновляем список файлов в папке "uploads"
function view_uploads() {
  $.ajax({ url: '/files',
           success: function(data) {
                        $('#view_files').html(data);
                    },
  });
}

//программа запущена или нажали кнопку отправки файла, обновляем список файлов в приложении
$(document).ready(function(){
  $('#view_files').load('/files');
  //нажитие кнопки
  $('#button_send').click(function(){
    view_uploads();
    setTimeout(view_uploads, 1000);
    setTimeout(view_uploads, 5000);
  });
})
