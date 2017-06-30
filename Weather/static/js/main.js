function getGeoPosAndMap()
{
    if (!navigator.geolocation)
    {
        alert("Geolocation is not supported by your browser");
        return;
    }

    var agree = false;

    function getPosition(latitude, longitude)
    {
        var zoomMap = 10;

        if(agree)
            zoomMap = 15;

        $('#city-geo').text('City coordinates: [' + latitude.toFixed(2)+', ' + longitude.toFixed(2) + ']');
        sendRequest(latitude, longitude);

        getMap(latitude,longitude,zoomMap, agree);
        // var coords = new google.maps.LatLng(latitude, longitude);
        // var mapOptions = {
        //     zoom: zoomMap,
        //     center: coords,
        //     mapTypeControl: true,
        //     navigationControlOptions: {
        //         style: google.maps.NavigationControlStyle.SMALL
        //     },
        //     mapTypeId: google.maps.MapTypeId.ROADMAP
        // };
        // var map = new google.maps.Map(
        //     document.getElementById("map"), mapOptions
        // );
        // if (agree)
        // {
        //     var marker = new google.maps.Marker({
        //         position: coords,
        //         map: map,
        //         title: "Your current location!"
        //     });
        // }
    }

    function success(position) {
        agree=true;
        getPosition(position.coords.latitude, position.coords.longitude);

    }

    navigator.geolocation.getCurrentPosition(success);
    getPosition(47.8466359, 35.124197);
}

function sendRequest(latitude, longitude)
{
    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        url: "",
        type: "POST",
        data:
            {
                'lat': latitude,
                'lon': longitude
            },
        success: onAjaxSuccess
    });

    function onAjaxSuccess(data)
    {
        if(data['WeatherIcon'].slice(-1) === 'n')
            $('#weather-now').css('background-image', 'url(../static/images/night.jpg)');

        $('#city-name').html(data['Name'] + ', ' + data['Country'] +
            "     <img src='http://openweathermap.org/images/flags/" + data['Country_icon_low'] + ".png'>");
        $('#city-temp').text(data['Temp'] + ' °C' + "   ");
        $('#city-w-icon').html("<img src='http://openweathermap.org/img/w/" + data['WeatherIcon'] + ".png'>");
        $('#city-sun-r').text('Sunrise: ' + data['Sunrise']);
        $('#city-sun-s').text('Sunset: ' + data['Sunset']);
        $('#city-weather-descr').text('Cloudiness: ' + data['Cloudiness']);


        eqnum = 0;
        jQuery.each(data, function (i, val) {
            if (eqnum === 4) {
                return false;
            }
            $('.city-block-value:eq('+ eqnum +')').text(val);
            eqnum++;
        });
    }
}

function searchCity() {

    $("#input_field").autocomplete({
        source: function(request, response){
            $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                url: "",
                type: "POST",
                dataType: "json",
                data:{ 'term': request.term},
                success: onAjaxSuccess
            });
        },
        minLength: 3,
        delay:500
    });

    function onAjaxSuccess(data)
    {
        $('#search_res-list').remove();
        var cities = '<ul id="search_res-list">';

        for (var city in data) {
            cities += "<li><a class='elem-of-res' href='/forecast/" + city + "'>" + data[city] + '</a>' + '</li>';
        }
        cities += '</ul>';
        $('#search_res_placeholder').text('');
        document.getElementById('search_res').innerHTML += cities;
    }
}

function blurField() {
    var interval = setTimeout(function () {
        $('.elem-of-res').hide();
        $('#search_res_placeholder').text('');
    },200);

}

function focusField() {
    if (document.getElementById("input_field").value === "") {
        $('.elem-of-res').remove();
        $('#search_res_placeholder').text('No items to display');
    }
    else{
        $('.elem-of-res').show();
    }
}

function getMap(latitude, longitude, zoomMap, markerMap){
    var coords = new google.maps.LatLng(latitude, longitude);
    var mapOptions = {
        zoom: zoomMap,
        center: coords,
        mapTypeControl: true,
        navigationControlOptions: {
            style: google.maps.NavigationControlStyle.SMALL
        },
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(
        document.getElementById("map"), mapOptions
    );

    if (markerMap){
        var marker = new google.maps.Marker({
            position: coords,
            map: map,
            title: "Your current location!"
        });
    }
}