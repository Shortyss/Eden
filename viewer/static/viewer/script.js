document.addEventListener('DOMContentLoaded', function () {
    function showAlert(message) {
        alert(message);
    }

    showAlert('Pozor nejedná se o skutečnou cestovní kancelář! Jde pouze o ukázkovou stránku.')

    function getAvailableRooms(hotelId, arrivalDate, departureDate) {
        return fetch(`/api/hotel_custom_api/${hotelId}/?arrival_date=${arrivalDate}&departure_date=${departureDate}`)
            .then(response => response.json())
            .then(data => {
                return data.available_rooms;
            })
            .catch(error => console.error('Error fetching available rooms:', error));
    }

    function updateAvailableRoomsCount(hotelId, arrivalDate, departureDate) {
        return getAvailableRooms(hotelId, arrivalDate, departureDate).then(availableRooms => {
            // Zobrazit počet volných pokojů pro každý typ pokoje
            document.getElementById('available_single_rooms').textContent = availableRooms.single_rooms;
            document.getElementById('available_double_rooms').textContent = availableRooms.double_rooms;
            document.getElementById('available_family_rooms').textContent = availableRooms.family_rooms;
            document.getElementById('available_suite_rooms').textContent = availableRooms.suite_rooms;
        });
    }

    function checkCapacity(adults, children, numberOfRooms, maxCapacity) {
        var totalCapacity = numberOfRooms * maxCapacity;

        if ((adults + children) > totalCapacity) {
            return 'Překročena maximální kapacita pro vybraný počet pokojů.';
        }

        return '';
    }

    function calculateTotalPriceForDay(prices, roomType, currentDate) {
        var matchingPrice = prices.find(function (price) {
            var priceStartDate = new Date(price.arrival_date);
            var priceEndDate = new Date(price.departure_date);

            return currentDate >= priceStartDate && currentDate < priceEndDate;
        });

        if (!matchingPrice) {
            matchingPrice = prices[prices.length - 1];
        }

        return parseFloat(matchingPrice[roomType]);
    }

    function calculateTotalPrice(prices, roomType, pricesRoomTypes, numberOfRooms, startDate, endDate) {
        var totalPrice = 0;
        var currentDate = new Date(startDate);
        var endDateObj = new Date(endDate);
        endDateObj.setDate(endDateObj.getDate());

        while (currentDate < endDateObj) {
            totalPrice += calculateTotalPriceForDay(prices, pricesRoomTypes, currentDate);
            currentDate.setDate(currentDate.getDate() + 1);
        }

        return totalPrice;
    }

    function calculateMealPlanPrice(mealPlan, adults, children, stayDuration) {
        var mealPlanPrice = parseFloat(mealPlan.price);
        return mealPlanPrice * stayDuration * (adults + children);
    }

    function calculateTransportationPrice(transportation, adults, children) {
        var transportationPrice = parseFloat(transportation.price);
        return transportationPrice * (adults + children);
    }

    function calculateTotalTravelers(roomType) {
        var adults = parseInt(document.getElementById('adults_' + roomType).value) || 0;
        var children = parseInt(document.getElementById('children_' + roomType).value) || 0;
        return adults + children;
    }

    function updateTotalTravelers(roomType) {
        var roomTypes = ['single_rooms', 'double_rooms', 'family_rooms', 'suite_rooms'];
        var travelers = 0;

        roomTypes.forEach(function (roomType) {
            travelers += calculateTotalTravelers(roomType);
        });

        var travelerElement = document.getElementById('travelers');
        if (travelerElement) {
            travelerElement.textContent = 'Celkem cestujících: ' + totalTravelers;
            saveDataToSession('travelers', totalTravelers);
        }
    }

    function saveDataToSession(key, value) {
        try {
            var existingData = JSON.parse(sessionStorage.getItem(key)) || {};

            existingData[key] = value;

            sessionStorage.setItem(key, JSON.stringify(existingData));

        } catch (error) {
            console.error('Chyba při ukládání do sessionStorage:', error);
        }
    }

    function updateTotalPrice() {
        var roomTypes = ['single_rooms', 'double_rooms', 'family_rooms', 'suite_rooms'];
        var pricesRoomTypes = ['price_single_room', 'price_double_room', 'price_family_room', 'price_suite'];

        var selectedRoomType = null;
        var totalNumberOfRooms = 0;
        var travelers = 0;
        var totalPrice = 0;


        for (var i = 0; i < roomTypes.length; i++) {
            var numberOfRooms = parseInt(document.getElementById(roomTypes[i]).value);
            if (numberOfRooms > 0) {
                selectedRoomType = roomTypes[i];
                selectedPricesRoomType = pricesRoomTypes[i];
                totalNumberOfRooms += numberOfRooms;

                if (!selectedRoomType || totalNumberOfRooms === 0) {
                    console.error('No room type selected or total number of rooms is zero.');
                    return;
                }

                var adults = parseInt(document.getElementById('adults_' + selectedRoomType).value);
                var children = parseInt(document.getElementById('children_' + selectedRoomType).value);
                var maxCapacity = getMaxCapacityForRoomType(selectedRoomType);

                var travelers = travelers + adults + children;

                var currentUrl = window.location.href;
                var hotelId = currentUrl.split('/hotel/')[1].split('/')[0];

                if (!selectedRoomType) {
                    console.error('No room type selected.');
                    return;
                }

                var price;
                function processPrices(prices) {
                    console.log(prices);
                }

                 var startDate = document.getElementById('arrival_date').value;
                 var endDate = document.getElementById('departure_date').value;

                 if (selectedRoomType) {
                     price = calculateTotalPrice(prices, selectedRoomType, selectedPricesRoomType, numberOfRooms, startDate, endDate);

                    totalPrice += price;

                 } else {
                    console.error('No room type selected.')
                 }

                var errorMessageElement = document.getElementById('error_adults_' + selectedRoomType);
                if (errorMessageElement) {
                    var errorMessage = checkRoomCapacity(adults, children, numberOfRooms, maxCapacity);
                    errorMessageElement.innerText = errorMessage;
                    if (errorMessage) {
                        console.error(errorMessage);
                        return;
                    }
                }
            }
        }

        var travelerElement = document.getElementById('travelers');
        if (travelerElement) {
                travelerElement.textContent = 'Celkem cestujících: ' + travelers;
        }

                var currentUrl = window.location.href;
                var hotelId = currentUrl.split('/hotel/')[1].split('/')[0];

                fetch('http://127.0.0.1:8000/api/prices_api/' + hotelId + '/')
                    .then(response => response.json())
                    .then(prices => {
                        var startDate = document.getElementById('arrival_date').value;
                        var endDate = document.getElementById('departure_date').value;

                        if (adults > 0 || children > 0) {
                            var mealPlanId = document.getElementById('meal_plan').value;
                            fetch('http://127.0.0.1:8000/api/meal_plan_api/' + mealPlanId + '/')
                                .then(response => response.json())
                                .then(mealPlan => {
                                    var stayDuration = (new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24);

                                    var mealPlanPrice = calculateMealPlanPrice(mealPlan, adults, children, stayDuration);

                                    var transportationId = document.getElementById('transportation').value;

                                    // Kontrola, zda je vybrána doprava
                                    var transportationPrice = 0;
                                    if (transportationId !== 'no_transport') {
                                        fetch('http://127.0.0.1:8000/api/transportation_api/' + transportationId + '/')
                                            .then(response => response.json())
                                            .then(transportation => {
                                                transportationPrice = parseFloat(transportation.price);

                                                var transportationPrice = calculateTransportationPrice(transportation, adults, children);
                                                var totalTotalPriceWithTransportation = totalPrice + mealPlanPrice + transportationPrice;

                                                var totalPriceElement = document.getElementById('total_price');
                                                if (totalPriceElement) {
                                                    totalPriceElement.textContent = 'Celková cena: ' + totalTotalPriceWithTransportation.toFixed(2) + ' Kč';

                                                }
                                            })
                                            .catch(error => console.error('Error fetching Transportation API:', error));
                                    } else {
                                        var totalTotalPriceWithoutTransportation = totalPrice + mealPlanPrice;

                                        var totalPriceElement = document.getElementById('total_price');
                                        if (totalPriceElement) {
                                            totalPriceElement.textContent = 'Celková cena: ' + totalTotalPriceWithoutTransportation.toFixed(2) + ' Kč';
                                        }
                                    }
                                })
                                .catch(error => console.error('Error fetching Meal Plan API:', error));
                            } else {
                                var meal_plan = 0;
                            }
                    })
                    .catch(error => console.error('Error fetching Prices API:', error));


    }

    function getMaxCapacityForRoomType(roomType) {
        switch (roomType) {
            case 'single_rooms':
                return 1;
            case 'double_rooms':
                return 2;
            case 'family_rooms':
                return 4;
            case 'suite_rooms':
                return 6;
            default:
                console.error('Unknown room type: ' + roomType);
                return 0;
        }
    }

    function checkRoomCapacity(adults, children, numberOfSelectedRooms, maxCapacity) {
        var totalCapacity = numberOfSelectedRooms * maxCapacity;

        if ((adults + children) > totalCapacity) {
            return 'Překročena maximální kapacita pro vybraný počet pokojů.';
        }

        return '';
    }

    document.getElementById('arrival_date').addEventListener('change', () => {
        const arrivalDate = document.getElementById('arrival_date').value;
        const departureDate = document.getElementById('departure_date').value;
        updateAvailableRoomsCount(hotelId, arrivalDate, departureDate);
    });

    document.getElementById('departure_date').addEventListener('change', () => {
        const arrivalDate = document.getElementById('arrival_date').value;
        const departureDate = document.getElementById('departure_date').value;
        updateAvailableRoomsCount(hotelId, arrivalDate, departureDate);
    });


    var formFields = ['single_rooms', 'adults_single_rooms', 'children_single_rooms',
        'double_rooms', 'adults_double_rooms', 'children_double_rooms',
        'family_rooms', 'adults_family_rooms', 'children_family_rooms',
        'suite_rooms', 'adults_suite_rooms', 'children_suite_rooms',
        'meal_plan', 'transportation', 'arrival_date', 'departure_date', 'travelers'];

    formFields.forEach(function (field) {
        var inputElement = document.getElementById(field);
        if (inputElement) {
            inputElement.addEventListener('input', updateTotalPrice);
        }
    });

    var totalTotalPriceElement = document.getElementById('totalPrice');
    if (totalTotalPriceElement) {
        totalTotalPriceElement.addEventListener('change', totalTotalPrice);
    }

    var travelersValue = document.getElementById('travelers').textContent.trim();
    var totalPriceValue = document.getElementById('total_price').textContent.trim();

    const currentUrl = window.location.href;
    const hotelId = currentUrl.split('/hotel/')[1].split('/')[0];
    const arrivalDate = document.getElementById('arrival_date').value;
    const departureDate = document.getElementById('departure_date').value;
    updateAvailableRoomsCount(hotelId, arrivalDate, departureDate);

    updateTotalPrice();
});

// time and date update

function updateTime() {
    var dateTimeElement = document.getElementById("date-time");
    if (dateTimeElement) {
        var now = new Date();

        var options = {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
        };
        var formattedDateTime = " " + "Dnes je " + now.toLocaleDateString('cs-CZ', options);

        dateTimeElement.textContent = formattedDateTime;
    }
}

setInterval(updateTime, 1000);
updateTime();

// offer box
if (window.location.pathname.endsWith("/")) {

    var destinations = [
        {
            image: "static/offer/Albánie.jpg",
            link: "http://127.0.0.1:8000/country/20/",
            name: "Albánie"
        },
        {
            image: "static/offer/Aruba.jpg",
            link: "http://127.0.0.1:8000/country/52/",
            name: "Aruba"
        },
        {
            image: "static/offer/Česká Republika.jpg",
            link: "http://127.0.0.1:8000/country/3/",
            name: "Česká Republika"
        },
        {
            image: "static/offer/Egypt.jpg",
            link: "http://127.0.0.1:8000/country/27/",
            name: "Egypt"
        },
        {
            image: "static/offer/Filipíny.jpg",
            link: "http://127.0.0.1:8000/country/43/",
            name: "Filipíny"
        },
        {
            image: "static/offer/Florida.jpg",
            link: "http://127.0.0.1:8000/country/48/",
            name: "Florida"
        },
    ];

    var currentDestination = 0;

    function showNextDestination() {
        currentDestination++;
        if (currentDestination >= destinations.length) {
            currentDestination = 0;
        }
        updateDestination();
    }

    function showPreviousDestination() {
        currentDestination--;
        if (currentDestination < 0) {
            currentDestination = destinations.length - 1;
        }
        updateDestination();
    }

    function updateDestination() {
        var destinationBox = document.getElementById('destinationBox');
        var imageContainer = document.querySelector('.image-container');

        var newImage = document.createElement('img');
        newImage.src = destinations[currentDestination].image;
        newImage.classList.add('destination-image');

        var destinationLink = document.createElement('a');
        destinationLink.href = destinations[currentDestination].link;
        destinationLink.appendChild(newImage);

        var destinationName = document.createElement('div');
        destinationName.innerText = destinations[currentDestination].name;
        destinationName.classList.add('destination-name');

        var arrowLeft = document.querySelector('.arrow.left');
        var arrowRight = document.querySelector('.arrow.right');

        arrowLeft.classList.add('highlighted-arrow');
        arrowRight.classList.add('highlighted-arrow');

        var oldImage = imageContainer.querySelector('a');
        if (oldImage) {
            imageContainer.replaceChild(destinationLink, oldImage);
        } else {
            imageContainer.appendChild(destinationLink);
        }

        var oldName = imageContainer.querySelector('.destination-name');
        if (oldName) {
            imageContainer.replaceChild(destinationName, oldName);
        } else {
            imageContainer.appendChild(destinationName);
        }
    }

    updateDestination();
}



function copyToInput() {
    var spanValue = document.getElementById('total_price').textContent;

    var numberMatch = spanValue.match(/\d+/);

    var numberValue = numberMatch ? parseInt(numberMatch[0]) : 0;

    var inputElement = document.getElementById('total_price_v');
    inputElement.value = numberValue;
}

function copyTravelersToInput() {
    var travelersValue = document.getElementById('travelers').textContent;

    var numberMatch = travelersValue.match(/\d+/);

    var numberValue = numberMatch ? parseInt(numberMatch[0]) : 0;

    var inputElement = document.getElementById('travelers_input');
    inputElement.value = numberValue;
}

var spanElementTravelers = document.getElementById('travelers');
spanElementTravelers.addEventListener('DOMSubtreeModified', function() {
    copyTravelersToInput();
});

var spanElementTravelers = document.getElementById('travelers');
spanElementTravelers.addEventListener('DOMSubtreeModified', function() {
    copyTravelersToInput();
});

function handleReservationClick() {
    copyToInput();
    copyTravelersToInput();
}

var currentUrl = window.location.href;
var hotelId = currentUrl.split('/hotel/')[1].split('/')[0];

function getAvailableRooms(hotelId, arrivalDate, departureDate) {
    fetch(`/api/hotel_custom_api/${hotelId}/?arrival_date=${arrivalDate}&departure_date=${departureDate}`)
        .then(response => response.json())
        .then(data => {
            // Zpracování dat z API
            const availableRooms = data.available_rooms;
            // Vytvořte objekt s klíči pro typy pokojů a s hodnotami počtu dostupných pokojů
            const responseObject = {
                single_rooms: availableRooms.single_rooms,
                double_rooms: availableRooms.double_rooms,
                family_rooms: availableRooms.family_rooms,
                suite_rooms: availableRooms.suite_rooms
            };
            return responseObject;
        })
        .catch(error => console.error('Error fetching available rooms:', error));
}

document.getElementById('arrival_date').addEventListener('change', () => {
    const arrivalDate = document.getElementById('arrival_date').value;
    const departureDate = document.getElementById('departure_date').value;
    getAvailableRooms(hotelId, arrivalDate, departureDate).then(data => {
        const availableRoomsSingleElement = document.getElementById('available_rooms_single');
        if (availableRoomsSingleElement) {
            availableRoomsSingleElement.textContent = data.single_rooms;
        }
        const availableRoomsDoubleElement = document.getElementById('available_rooms_double');
        if (availableRoomsDoubleElement) {
            availableRoomsDoubleElement.textContent = data.double_rooms;
        }
        const availableRoomsFamilyElement = document.getElementById('available_rooms_family');
        if (availableRoomsFamilyElement) {
            availableRoomsFamilyElement.textContent = data.family_rooms;
        }
        const availableRoomsSuiteElement = document.getElementById('available_rooms_suite');
        if (availableRoomsSuiteElement) {
            availableRoomsSuiteElement.textContent = data.suite_rooms;
        }
    });
});

document.getElementById('departure_date').addEventListener('change', () => {
    const arrivalDate = document.getElementById('arrival_date').value;
    const departureDate = document.getElementById('departure_date').value;
    getAvailableRooms(hotelId, arrivalDate, departureDate).then(data => {
        const availableRoomsSingleElement = document.getElementById('available_rooms_single');
        if (availableRoomsSingleElement) {
            availableRoomsSingleElement.textContent = data.single_rooms;
        }
        const availableRoomsDoubleElement = document.getElementById('available_rooms_double');
        if (availableRoomsDoubleElement) {
            availableRoomsDoubleElement.textContent = data.double_rooms;
        }
        const availableRoomsFamilyElement = document.getElementById('available_rooms_family');
        if (availableRoomsFamilyElement) {
            availableRoomsFamilyElement.textContent = data.family_rooms;
        }
        const availableRoomsSuiteElement = document.getElementById('available_rooms_suite');
        if (availableRoomsSuiteElement) {
            availableRoomsSuiteElement.textContent = data.suite_rooms;
        }
    });
});
