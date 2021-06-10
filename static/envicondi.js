//Draw Chart.js
function drawTemperatureChart(labels, data) {
    var temperatureCanvas = document.getElementById("TemperatureChart").getContext("2d");
    globalThis.temperature_chart;
    if (typeof temperature_chart == "undefined") {
        temperature_chart = new Chart(temperatureCanvas, {
        animationEnabled: true,
        zoomEnabled: true,
        title: {
        text: "Temperature Chart"
        },
        axisX: {
        title: "Date time"
        },
        axisY: {
        title: "Temperature"
        },
        data: {
            labels: labels,
            datasets: [
                {
                label: "Temperature",
                data: data,
                fill: false,
                borderColor: "rgb(255,0,0)",
                lineTension: 0.1,
                type: "line"
                }
            ]
            },
            options: {
            responsive: true
            }
        });
    }
    else {
        temperature_chart.destroy();
        temperature_chart = new Chart(temperatureCanvas, {
            animationEnabled: true,
            zoomEnabled: true,
            title: {
            text: "Temperature Chart"
            },
            axisX: {
            title: "Date time"
            },
            axisY: {
            title: "Temperature"
            },
            data: {
                labels: labels,
                datasets: [
                    {
                    label: "Temperature",
                    data: data,
                    fill: false,
                    borderColor: "rgb(255,0,0)",
                    lineTension: 0.1,
                    type: "line"
                    }
                ]
                },
                options: {
                responsive: true
                }
            });
    }
  }

  function drawHumidityChart(labels, data) {
    var humidityCanvas = document.getElementById("HumidityChart").getContext("2d");
    globalThis.humidity_chart;
    if ((typeof humidity_chart) == 'undefined') {
        humidity_chart = new Chart(humidityCanvas, {
        animationEnabled: true,
        zoomEnabled: true,
        title: {
        text: "Humidity Chart"
        },
        axisX: {
        title: "Date time"
        },
        axisY: {
        title: "Humidity"
        },
        data: {
            labels: labels,
            datasets: [
                {
                label: "Humidity",
                data: data,
                fill: false,
                borderColor: "rgb(0,0,255)",
                lineTension: 0.1,
                type: "line"
                }
            ]
            },
            options: {
            responsive: true
            }
        });
    }
    else {
        humidity_chart.destroy();
        humidity_chart = new Chart(humidityCanvas, {
            animationEnabled: true,
            zoomEnabled: true,
            title: {
            text: "Humidity Chart"
            },
            axisX: {
            title: "Date time"
            },
            axisY: {
            title: "Humidity"
            },
            data: {
                labels: labels,
                datasets: [
                    {
                    label: "Humidity",
                    data: data,
                    fill: false,
                    borderColor: "rgb(0,0,255)",
                    lineTension: 0.1,
                    type: "line"
                    }
                ]
                },
                options: {
                responsive: true
                }
            });
    }
  }

  function drawBrightnessChart(labels,data) {
    var brightnessCanvas = document.getElementById("BrightnessChart").getContext("2d");
    globalThis.brightness_chart;
    if ((typeof brightness_chart) == 'undefined') {
        brightness_chart = new Chart(brightnessCanvas, {
        animationEnabled: true,
        zoomEnabled: true,
        title: {
        text: "Brightness Chart"
        },
        axisX: {
        title: "Date time"
        },
        axisY: {
        title: "Brightness"
        },
        data: {
            labels: labels,
            datasets: [
                {
                label: "Brightness",
                data: data,
                fill: false,
                borderColor: "rgb(210,180,140)",
                lineTension: 0.1,
                type: "line"
                }
            ]
            },
            options: {
            responsive: true
            }
        });
    }
    else {
        brightness_chart.destroy();
        brightness_chart = new Chart(brightnessCanvas, {
            animationEnabled: true,
            zoomEnabled: true,
            title: {
            text: "Brightness Chart"
            },
            axisX: {
            title: "Date time"
            },
            axisY: {
            title: "Brightness"
            },
            data: {
                labels: labels,
                datasets: [
                    {
                    label: "Brightness",
                    data: data,
                    fill: false,
                    borderColor: "rgb(210,180,140)",
                    lineTension: 0.1,
                    type: "line"
                    }
                ]
                },
                options: {
                responsive: true
                }
            });
    }
  }
  

//AJAX

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
        drawTemperatureChart(data.temp_label,data.temp_data);
      });

    });

  $('#form_humidity').on('submit', function(event) {
    event.preventDefault();
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

    });

  $('#form_brightness').on('submit', function(event) {
    event.preventDefault(); 
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

    });
});
