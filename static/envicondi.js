$(document).ready(function() {
    $('#form_temperature').on('submit', function(event) {
      event.preventDefault();
      $.ajax({
        data : {
          start_temp_date : $('#datetimepicker1').val(),
          end_temp_date : $('#datetimepicker2').val(),
          option_temp : $('#option_temperature').val(),
          form_type : 'Temperature'
        },
        type : 'POST',
        url : '/envicondi2'
      })
      .done(function(data) {
        alert("Form_temperature");
        drawTemperatureChart(data.temp_label,data.temp_data);
      });

    });

  $('#form_humidity').on('submit', function(event) {
      $.ajax({
        data : {
          start_humid_date : $('#datetimepicker3').val(),
          end_humid_date : $('#datetimepicker4').val(),
          option_humid : $('#option_humidity').val(),
          form_type : 'Humidity'
        },
        type : 'POST',
        url : '/envicondi2'
      })
      .done(function(data) {
        drawHumidityChart(data.humid_label,data.humid_data);
      });

      event.preventDefault();
    });

  $('#form_brightness').on('submit', function(event) {
      $.ajax({
        data : {
          start_bright_date : $('#datetimepicker5').val(),
          end_bright_date : $('#datetimepicker6').val(),
          option_bright : $('#option_brightness').val(),
          form_type : 'Brightness'
        },
        type : 'POST',
        url : '/envicondi2'
      })

      .done(function(data) {
        drawBrightnessChart(data.brightness_label,data.brightness_data);
      });

      event.preventDefault();
    });
});
