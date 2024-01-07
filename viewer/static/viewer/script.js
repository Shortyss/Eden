function updateTime() {
    var dateTimeElement = document.getElementById("date-time");
    var now = new Date();

    var options = {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
    };
    var formattedDateTime = " " + "Dnes je " + now.toLocaleDateString('cs-CZ', options);

    dateTimeElement.textContent = formattedDateTime;
}

setInterval(updateTime, 1000);
updateTime();

//function showCities(countryId) {
//      fetch(`/get_cities/${countryId}/`)
//        .then(response => response.json())
//        .then(data => {
//          const citiesContainer = document.getElementById('cities-container');
//          citiesContainer.innerHTML = '<h2>Cities:</h2>';
//          data.forEach(city => {
//            citiesContainer.innerHTML += `<p>${city.name}</p>`;
//          });
//        });
//}
//
//// stars.js
//document.addEventListener('DOMContentLoaded', function () {
//  let stars = document.querySelectorAll('.star');
//
//  stars.forEach(function (star) {
//    star.addEventListener('click', function () {
//      this.querySelector('input').click();
//    });
//  });
//});
//
