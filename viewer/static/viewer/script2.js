function calculateTotalPrice(prices, startDate, endDate, roomType) {
    var totalPrice = 0;
    var currentDate = new Date(startDate);
    var endDateObj = new Date(endDate);

    currentDate.setDate(currentDate.getDate());
    endDateObj.setDate(endDateObj.getDate() + 1);

    console.log('Výpis cen za každý den:');
    while (currentDate < endDateObj) {
        var matchingPrice = prices.find(function (price) {
            var priceStartDate = new Date(price.arrival_date);
            var priceEndDate = new Date(price.departure_date);

            return currentDate >= priceStartDate && currentDate < priceEndDate;
        });

        // Pokud není nalezena odpovídající cena, použijte poslední nalezenou cenu
        if (!matchingPrice) {
            matchingPrice = prices[prices.length - 1];
        }

        console.log('Datum: ' + currentDate.toISOString().split('T')[0] + ', Cena za den: ' + matchingPrice[roomType]);

        totalPrice += parseFloat(matchingPrice[roomType]);
        currentDate.setDate(currentDate.getDate() + 1);
    }

    console.log('Celková cena za ' + roomType + ': ' + totalPrice.toFixed(2));
    return totalPrice;
}


var apiUrl = 'http://127.0.0.1:8000/api/prices_api/5/';
var startDate = '2024-07-20';
var endDate = '2024-08-18';
var roomType = 'price_single_room';

// AJAX požadavek pro získání cen z API
var xhr = new XMLHttpRequest();
xhr.open('GET', apiUrl, true);

xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var prices = JSON.parse(xhr.responseText);

        // Výpočet celkové ceny
        var totalSingleRoomPrice = calculateTotalPrice(prices, startDate, endDate, roomType);
    }
};

xhr.send();
