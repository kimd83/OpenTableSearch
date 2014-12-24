$(function()
{
    $("#restaurants").pickList();
});

$(function() {
    $( "#start_date" ).datepicker({
        dateFormat: "mm/dd/yy"
    }).datepicker("setDate","0");
});

$(function() {
    $( "#end_date" ).datepicker({
        dateFormat: "mm/dd/yy"
    }).datepicker("setDate","0");
});

function loadData(){
    var form = $(this);
    var restaurants = document.getElementById("restaurants");
    var selected = [];
    for (var i=0;i<restaurants.options.length;i++){
        if(restaurants.options[i].selected == true){
            selected.push(restaurants.options[i].value);
        }
    }
    var start_date = document.getElementById("start_date").value;
    var end_date = document.getElementById("end_date").value;
    var time = document.getElementById("time").value;
    var people = document.getElementById("people").value;
    var data = {selected: selected, start_date: start_date, end_date: end_date, time: time, people: people};
        
    // var page_url = "http://www.opentable.com"
    // var page_url = 'http://www.opentable.com/opentables.aspx?t=rest&r=restaurant_id&m=8&p=people&d=1/7/2015%206:00:00%20PM&scpref=100'
    var request = $.ajax({
        type: form.prop('method'),
        url: window.location.protocol+'//'+window.location.host+"/crossdomain",
        data: JSON.stringify(data),
        success: function( response ) {
          var result = response;
          // $("#tables").append('<li>' + selected + '</li>');
          // $("#tables").append('<li>' + start_date + '</li>');
          // $("#tables").append('<li>' + end_date + '</li>');
          // $("#tables").append('<li>' + time + '</li>');
          // $("#tables").append('<li>' + people + '</li>');
          var result = $.parseJSON(result);
          console.log(result);
          $("#tables").empty();
          for(var key in result){
            console.log(key);
            console.log(result[key]);
            console.log(result[key][1])
            $("#tables").append('<li>' + key + '</li>');
            for(var i=0;i<result[key].length;i++){
                $("#tables").append('<li><a href='+ result[key][i].split(" ")[2] + ">" + result[key][i].split(" ")[0] + " " + result[key][i].split(" ")[1] + '</a></li>');
            }
        }
        }
    });
    
    // request.done(function(reply){
    //     $('#tables').append(reply.value);
    return false;
};

$('#form-container').submit(loadData);

