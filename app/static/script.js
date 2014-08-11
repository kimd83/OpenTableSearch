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
				// $("#rlist").append('<li>Carbone</li>');
				
				break;
		};

	});
	});



$(document).ready(function () {
    $("#button1").click(function () {
        $("#list1 > option:selected").each(function () {
            $(this).remove().appendTo("#list2");
            rearrangeList("#list2");
        });
    });

    $("#button2").click(function () {
        $("#list2 > option:selected").each(function () {
            $(this).remove().appendTo("#list1");
            rearrangeList("#list1");
        });
    });

function byValue(a, b) {
    return a.value > b.value ? 1 : -1;
};

function rearrangeList(list) {
    $(list).find("option").sort(byValue).appendTo(list);
};
    
});