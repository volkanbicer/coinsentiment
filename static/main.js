var _data = [];

function loadData(){
  let query = $('#query').val();
  $('#loading').show();
  $.ajax({
    url: 'reddit/headlines',
    data: {'query': query},
    dataType: 'json',
    type: 'GET',
    success: (res) => {
      $('#loading').hide();
      console.log(_data);
      _data = res.data;
      buildChart();
      renderHeadlines();
    }})
}

function buildChart(){
  Highcharts.setOptions({
 colors: ['#4caf50', '#ff9800', '#e51c23']
});
  Highcharts.chart('container', {
    chart: {
        pie:{
          colors:[
            '#50B432',
            '#ED561B',
            '#DDDF00'
          ]
        },
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'last ' +_data.total_count+ ' headlines on ' + $('#query').val()
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: getSeries()
  });
}
  function getSeries(){
    positive_percentage = 100 * _data.pos.length / _data.total_count;
    negative_percentage = 100 * _data.neg.length / _data.total_count;
    notr_percentage = 100 * _data.notr.length / _data.total_count;
    let data = [
      {name: 'positive', y: positive_percentage, sliced: true, selected: true},
      {name: 'notr', y: notr_percentage},
      {name: 'negative', y:negative_percentage}
    ];
    let series = [{
      name: 'Headlines',
      colorByPoint: true,
      data: data
    }];
    return series
  }


  function renderHeadlines(){
    $("#pos").empty();
    $("#neg").empty();
    $("#notr").empty();

    render(_data.pos, 'pos');
    render(_data.neg, 'neg');
    render(_data.notr);

    function render(data, status = 'notr'){
      for (var i = 0; i<data.length; i++){
        let link =  $('<a>').attr({'href': data[i].link, 'target': '_blank'});
        let date = new Date(data[i].time * 1000)
        let time = moment(date).format("LLL");
        if (status == 'pos'){
          let  element = $('<div class="alert alert-success" role="alert" style="font-weight:bold;">').text(data[i].title);
          element.append($('<p class="text-right" style="font-size:10px; font-weight:400">').text(time));
          link.append(element);
          $("#pos").append(link);
        }else if (status == 'neg'){
          let element = $('<div class="alert alert-danger" role="alert" style="font-weight:bold;">').text(data[i].title);
          element.append($('<p class="text-right" style="font-size:10px; font-weight:400">').text(time));
          link.append(element);
          $("#neg").append(link);
        }else{
          let element = $('<div class="alert alert-warning" role="alert" style="font-weight:bold;">').text(data[i].title);
          element.append($('<p class="text-right" style="font-size:10px; font-weight:400">').text(time));
          link.append(element);
          $("#notr").append(link);
        }
      }
    }
  }

// Initialize
$(document).ready(function(){
			loadData();
});
