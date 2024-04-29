{% extends "maintemplate.html" %}




{% block main_container %}
<div class="col" style="justify-items: center; width: 100%;">
<form action="" id="maps" class="container" >
  <div class="row" style="border-style: dotted;" >
    <div class="col-5" id="map" style="width: 500px; height: 500px;"></div>
    <div class="col-7" >
      <label for="keyword">검색할 장소를 입력하세요</label>
      <input type="text" id="keyword" name="keyword" class="controls" placeholder="입력하기"
        value="{{request._query_params.keyword}}">
      <button formethod=get >Search</button>
      <!-- onclick="searchPlaces()"></onclick> -->
      <div class="row">
        <table id="places">
          <thead>
            <tr>
              <th>Name</th>
              <th>Address</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
          {% for result in results %}
          <tr>
            <td>{{result.name}}</td>
            <td>{{result.formatted_address}}</td>
          </tr>
          {% endfor %}
        </table>
      </div>
    </div>
  </div>
</form>
</div>

{% endblock main_container%}




{% block js %}

<script type="text/javascript">
  // Python에서 전달된 results 데이터를 JavaScript 변수로 변환
  var resultsFromPython = {{ results | tojson | safe }};
</script>

<script>
  let map, infoWindow, service, pos;
  function callback(results, status) {
    console.log(results);
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      for (let i = 0; i < results.length; i++) {
        createMarker(results[i]);
      }
    }
  }
  function initMap() {
    infowindow = new google.maps.InfoWindow();

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (position) {
        pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        map = new google.maps.Map(document.getElementById('map'), {
          center: pos,
          zoom: 15,
          draggable: true, // 지도 드래그 가능
          zoomControl: true,
        });
        callback(resultsFromPython, google.maps.places.PlacesServiceStatus.OK);
      }, function () {
        handleLocationError(true, infowindow, map.getCenter());
      });
    } else {
      handleLocationError(false, infowindow, map.getCenter());
    }

  }

  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    pos = { lat: 37.5665, lng: 126.9780 };
    map = new google.maps.Map(document.getElementById('map'), {
      center: pos,
      zoom: 15,
    });

    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
      'Error: The Geolocation service failed.' :
      'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }

  function clearTable() {
    var table = document.getElementById('places').getElementsByTagName('tbody')[0];
    while (table.hasChildNodes()) {
      table.removeChild(table.firstChild);
    }
  }

  function createMarker(results) {
    if (!results.geometry || !results.geometry.location) return;
    const marker = new google.maps.Marker({
      map,
      position: results.geometry.location,
    });

    google.maps.event.addListener(marker, 'click', function () {
      infowindow.setContent(results.name);
      infowindow.open(map, this);
    });
  }

  window.onload = function () {
    initMap();
  }
</script>
<!-- Google Maps API Script -->
<script src="https://maps.googleapis.com/maps/api/js?key={{ API_KEY }}&libraries=places&callback=initMap" async
  defer></script>
{% endblock js %}