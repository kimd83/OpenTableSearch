$(function(){
  $("#start_date, #end_date" ).datepicker({
    dateFormat: "mm/dd/yy"
  }).datepicker("setDate","0");
});

$(function(){
  if(localStorage.getItem("start_time") != null){
    $("#start_time").val(localStorage.getItem('start_time'));
  };
  if(localStorage.getItem("end_time") != null){
    $("#end_time").val(localStorage.getItem('end_time'));
  };
  if(localStorage.getItem("people") != null){
    $("#people").val(localStorage.getItem('people'));
  };

  function date_to_string(date){
    var dd = date.getDate()
    var mm = date.getMonth() + 1;
    var yyyy = date.getFullYear();
    if(dd<10){
      dd = '0'+dd;
    }
    if(mm<10){
      mm = '0'+mm;
    }
    return mm + '/' + dd + '/' + yyyy;
  }

  var today = new Date();
  var today_string = date_to_string(today);
  
  if(localStorage.getItem("start_date") != null){
    $("#start_date").val(localStorage.getItem('start_date'));
  };
  if(new Date(localStorage.getItem("start_date")) < today){
    $("#start_date").val(today_string);
  };

  var tmr = new Date(today.setDate(today.getDate()+1));
  var tmr_string = date_to_string(tmr);

  if(localStorage.getItem("end_date") != null){
    $("#end_date").val(localStorage.getItem('end_date'));
  };
  if(new Date(localStorage.getItem("end_date")) < today){
    $("#end_date").val(tmr_string);
  };

  if(localStorage.getItem('selected') != null){
    var restaurants = $("#restaurants")[0];
    for(var i=0; i<restaurants.options.length; i++){
      restaurants.options[i].removeAttribute("selected","selected");
      if(localStorage.getItem('selected').split(",").indexOf(restaurants.options[i].value)>-1){
        restaurants.options[i].setAttribute("selected","selected");
      }
    }
  };
});

$(function(){
  $("#restaurants").pickList();
});

function loadData(){
  var form = $(this);
  var start_date = $("#start_date")[0].value;
  var end_date = $("#end_date")[0].value;
  var start_time = $("#start_time")[0].value;
  var end_time = $("#end_time")[0].value;
  var people = $("#people")[0].value;
  var restaurants = $("#restaurants")[0];
  var selected = [];
  for (var i=0; i<restaurants.options.length; i++){
    if(restaurants.options[i].selected == true){
      selected.push(restaurants.options[i].value);
    }
  }
  localStorage.clear();
  localStorage.setItem('start_date', start_date);
  localStorage.setItem('end_date', end_date);
  localStorage.setItem('start_time', start_time);
  localStorage.setItem('end_time', end_time);
  localStorage.setItem('people', people);
  localStorage.setItem('selected', selected);
  var data = {start_date: start_date, end_date: end_date, start_time: start_time, end_time: end_time, people: people, selected: selected};    
  var request = $.ajax({
    type: form.prop('method'),
    url: window.location.protocol+'//'+window.location.host+"/scrape",
    data: JSON.stringify(data),
    success: function( response ) {
      var result = $.parseJSON(response);
      $("#tables").empty();
      for(var key in result){
        $("#tables").append('<b>' + key + '</b><br>');
        if(result[key].length < 1){
          $("#tables").append('<li>No Tables Available</li>');
        }
        else{
          for(var i=0; i<result[key].length; i++){
            $("#tables").append('<li><a href='+ result[key][i].split(",")[0] + ">" + result[key][i].split(",")[1] + '</a></li>');
          }
        }
      $("#tables").append('<br>');
      }
    }
  });
  return false;
};

$(document).ajaxStart(function(){
  $("#loading").show();
  $("#result").hide();
});

$(document).ajaxStop(function(){
  $("#loading").hide();
  $("#result").show();
});

$('#form-container').submit(loadData);

