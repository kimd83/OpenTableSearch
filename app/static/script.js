$(document).ready(function(){
	$("#rtype").change(function(){
		var type = $(this).find("option:selected").attr("id");

		switch (type){

			case "All":
				$("#rlist").html("");
				$("#rlist").append('<li>Daniel</li>')
				$("#rlist").append('<li>Eleven Madison Park</li>')
				$("#rlist").append('<li>Marea</li>')
				break;

			case "American":
				$("#rlist").html("");
				$("#rlist").append('<li>Eleven Madison Park</li>');
				break;

			case "French":
				$("#rlist").html("");
				$("#rlist").append('<li>Daniel</li>');
				break;

			case "Italian":
				$("#rlist").html("");
				$("#rlist").append('<li>Marea</li>');
				break;
		};

	});
	});