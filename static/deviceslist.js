var list = {

    list_element : '#devices_list',
    button_container: '#filtering',

    init: function(){
        this.generate_default_list();
        //this.generate_buttons();
    },

    generate_buttons: function(current_type, current_device){

        var parent = $('<div/>', {'class': 'btn-group', 'role': 'group', 'id':'buttonsy'});
        var cheated_href = '#chart/'+current_device + '/' + current_type + '/';
        var cheated_href_hour = cheated_href + 'hour';
        var cheated_href_day = cheated_href + 'day';
        var cheated_href_month = cheated_href + 'month';
        var filter_label = $('<a/>', {'class': 'btn btn-primary btn-lg disabled', 'role': 'button', 'aria-disabled':'true'}).text('Choose filtering:');
        var filter_hour = $('<a/>', {'class': 'btn btn-secondary btn-lg', 'role': 'button', 'aria-disabled':'true', 'href':cheated_href_hour}).text('Last hour');
        var filter_day = $('<a/>', {'class': 'btn btn-secondary btn-lg', 'role': 'button', 'aria-disabled':'true', 'href':cheated_href_day}).text('Last day');
        var filer_month = $('<a/>', {'class': 'btn btn-secondary btn-lg', 'role': 'button', 'aria-disabled':'true', 'href':cheated_href_month}).text('Last month');

        parent.append(filter_label);
        parent.append(filter_hour);
        parent.append(filter_day);
        parent.append(filer_month);
        $(list.button_container).append(parent);
    },


    generate_default_list:  function(){

        $.get("devices/sensors", function(data, status) {

            if(data.data === undefined) {
                alert(' dupa zmiennej nie ma data.data')
            }

            var parent = $('<div/>', {'class': 'btn-group-vertical col-md-10', 'role': 'group'});

            $.each(data.data, function(index, item) {
                var element = $('<div/>', {'class':'btn-group dropright', 'role': 'group'});
                var button = $('<button/>', {'id':item.sensor_name+'_button', 'type':"button", 'class':'btn btn-secondary dropdown-toggle',
                                             'data-toggle':'dropdown', 'aria-haspopup':'true', 'aria-expanded':'false'} ).text(item.sensor_name)

                element.append(button)
                parent.append(element)

                var element_dropdown = $('<div/>', {'class':'dropdown-menu'});

                $.each(item.sensor_types, function(index, items){
                    var hrex = '#chart/' + item.sensor_name+'/'+items+'/hour';
                    var a_element = $('<a/>',{'class': 'dropdown-item', 'href':hrex}).text(items);
                    element_dropdown.append(a_element);
                });
                element.append(element_dropdown)
            });
            $(list.list_element).append(parent)
        }, 'json');
    }
}

var config;
/////////////////////////////////////////////////////////////////////////////////////
////generowanko wykresu
var chart = {

    chart_holder : '#chart_holder',

    init: function(){
       // this.generate_default_chart('malina2','Temperature', 'hour');
    },

    generate_default_chart: function(devicename, devicetype, filter){

    $.get("devices/chartdata",{device: devicename, type: devicetype, filtering: filter}, function(data, status) {
        console.log(data.data)
        if(data.data === undefined) {
                alert(' dupa zmiennej nie ma data.data')
            }

        config = {
               type: 'line',
               data: {
                   labels: data.data[0][0],
                   datasets: [{
                       label: devicetype,
                       backgroundColor: 'rgb(255, 99, 132)',
                       borderColor: 'rgb(255, 99, 132)',
                       data: data.data[0][1],
                   }]
               },
               options: {
               responsive: true,

                   title: {
                       display: true,
                       text: devicetype + ' Line Chart'
                   },
                   tooltips: {
                       mode: 'index',
                       intersect: false,
                   },
                   hover: {
                       mode: 'nearest',
                       intersect: true
                   },
                   scales: {
                       xAxes: [{
                           display: true,
                           scaleLabel: {
                               display: true,
                               labelString: 'Month'
                           }
                       }],
                       yAxes: [{
                           ticks: {
                               // the data minimum used for determining the ticks is Math.min(dataMin, suggestedMin)
                               suggestedMin: data.data[0][3],
                               // the data maximum used for determining the ticks is Math.max(dataMax, suggestedMax)
                               suggestedMax: data.data[0][2]
                           }
                       }]}}
               }

        var parent = $('<canvas/>', {'id': 'myChart'});

        $(chart.chart_holder).append(parent)

        var ctx = document.getElementById('myChart').getContext('2d');
        window.myLine = new Chart(ctx, config);
     }, 'json');
    }
    };


var common = {

    current_device: '',
    current_type: '',

    init: function(){
        this.restore_anchor_link()
        this.load_router()
    },

    restore_anchor_link: function(){
        $('body').on('click', 'a', function() {
            if($(this).attr('href').indexOf('#') == 0) {
                //window.location = $(this).attr('href');
            }
        });
    },

    load_router: function(){
        var Workspace = Backbone.Router.extend({

          routes: {
            "chart/:device/:type/:filtering": "buildchart" // #chart/malinaX/typ
          },

          buildchart: function(device, type, filtering){
                $('#buttonsy').remove();
                $('#myChart').remove();
                this.current_device = device;
                this.current_type = type;
                list.generate_buttons(this.current_type, this.current_device);
                chart.generate_default_chart(device, type, filtering);
          }
        });
        new Workspace();
    }
};

$(window).on('load', function(){
    common.init();
    list.init();
    chart.init();
    Backbone.history.start();
});