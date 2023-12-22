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