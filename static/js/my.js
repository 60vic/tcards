//начальная инициализация
$.getJSON( "_get_init", function( data ) {
	$.each(data['roles'], function (k,v) {
		$('#form1 select[name="role"]').append("<option name='"+v+"'>"+v+"</option>");
		$('#form2 select[name="role"]').append("<option name='"+v+"'>"+v+"</option>");
		});
	$.each(data['positions'], function (k,v) {
		$('#form1 select[name="pos"]').append("<option name='"+v+"'>"+v+"</option>");
		$('#form2 select[name="pos"]').append("<option name='"+v+"'>"+v+"</option>");
		});
	$.each(data['reqcats'], function (k,v) {
		$('#form3 select[name="reqcat"]').append("<option name='"+v+"'>"+v+"</option>");
		});		
  });


//вспомогательные функции
function notifymy(data) {
	if (data['reply']['error']) {
		$.notify(data['reply']['error'], "error");
	}
	if (data['reply']['good']) {
		$.notify(data['reply']['good'], "success");
	}
}

//установим маску для полей ввода телефонов  
$(document).ready(function(){ 
	$('#form1 input[name="mob"]').mask('+7(000)000-00-00');
});  
$(document).ready(function(){ 
	$('#form1 input[name="tel"]').mask('+7(81100)00-00-00');
});

//сохранение
$('#save2db').bind('click', function() {
	$.post('/save2db',
	$('#form1').serialize(), 
	function (data) {
		notifymy(data);
	});
	$.each($("#form2 :input"),function (){
		$(this).val("")
	});
});


  

//динамически меняем маску для города и районов
$("#form1 input[name='tel']").on('input load', function() {
	$('#save2db').prop('disabled',true);
	var v = $("#form1 input[name='tel']").val();
	$('#asd').text(v);
	if ( v.slice(0,7) == "+7(8112" )
	{
		$("#form1 input[name='tel']").mask('+7(8112)00-00-00');
	}
	else 
	{
		$("#form1 input[name='tel']").mask('+7(81100)0-00-00');
	}
});


//удаление карточки из базы, а также из спика результатов поиска
$('#carddel').bind('click', function() {
	$.post('/carddel', 
	{"rowid": $('#form2 input[name="rowid"]').val()},
	function (data) {
		notifymy(data);
	});
	$.each($("#slist .drid"), function () {
		if ( $(this).text() == $('#form2 input[name="rowid"]').val() ) {
			$(this).parent().remove();	
		} 
	});
	$.each($("#form2 :input"),function (){
		$(this).val("")
	});
});


//перенос из формы 2 в 1 если поле-приемник пустое
$('#card2to1').bind('click', function() {
	$.each($("#form2 :input"),function (){
		if ( $(`#form1 :input[name='${this.name}']`).val() === "" ) {
			$(`#form1 :input[name='${this.name}']`).val(this.value);
		}
	});
});

//поиск
$('#search2db').bind('click', function() {
	$('#form1 input[name="rowid"]').val("");
	$.post('/search2db',
	$('#form1').serialize(),
	function(data) {
		$('#slist .dtr').remove();
		$.each(data['result'], function (k,v) {
			$('#slist').append(`<tr class="dtr"><td class="drid">${v["rowid"]}</td><td>${v["tel"]}</td>td><td>${v["mob"]}</td>td><td>${v["fio"]}</td>td><td>${v["org"]}</td>td></li>`);
		});
		$('.drid').bind('click',function() {
			$("input[name='tel2']").val($(this).text());
			$.post('/get2rowid',{"rowid": $(this).text()}, function(data) {
				$.each(data['result'], function (k,v) {
					$.each(v, function (k,v) {
						$(`#form2 :input[name='${k}']`).val(v);
					});
				});
			});
		});
	});
	$('#save2db').removeAttr('disabled');
});
