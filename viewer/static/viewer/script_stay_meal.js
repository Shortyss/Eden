document.addEventListener('DOMContentLoaded', function () {
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
        return mealPlanPrice * (adults + children) * stayDuration;
    }

    function updateTotalPrice() {
        var roomTypes = ['single_rooms', 'double_rooms', 'family_rooms', 'suite_rooms'];
        var pricesRoomTypes = ['price_single_room', 'price_double_room', 'price_family_room', 'price_suite'];

        var selectedRoomType = null;
        var totalNumberOfRooms = 0;

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

                var errorMessageElement = document.getElementById('error_adults_' + selectedRoomType);
                if (errorMessageElement) {
                    var errorMessage = checkRoomCapacity(adults, children, totalNumberOfRooms, maxCapacity);
                    errorMessageElement.innerText = errorMessage;
                    if (errorMessage) {
                        console.error(errorMessage);
                        return;
                    }
                }

                var currentUrl = window.location.href;
                var hotelId = currentUrl.split('/hotel/')[1].split('/')[0];

                fetch('http://127.0.0.1:8000/api/prices_api/' + hotelId + '/')
                    .then(response => response.json())
                    .then(prices => {
                        var startDate = document.getElementById('arrival_date').value;
                        var endDate = document.getElementById('departure_date').value;

                        var totalPrice = calculateTotalPrice(prices, selectedRoomType, selectedPricesRoomType, numberOfRooms, startDate, endDate);

                        console.log('Room Type:', selectedRoomType);
                        console.log('Prices:', prices);
                        console.log('Total Price (Accommodation):', totalPrice);

                        var mealPlanId = document.getElementById('meal_plan').value;
                        fetch('http://127.0.0.1:8000/api/meal_plan_api/' + mealPlanId + '/')
                            .then(response => response.json())
                            .then(mealPlan => {
                                var stayDuration = (new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24);
                                var mealPlanPrice = calculateMealPlanPrice(mealPlan, adults, children, stayDuration);

                                console.log('Meal Plan:', mealPlan);
                                console.log('Meal Plan Price:', mealPlanPrice);

                                var totalTotalPrice = totalPrice * totalNumberOfRooms + mealPlanPrice;

                                var totalPriceElement = document.getElementById('total_price');
                                if (totalPriceElement) {
                                    totalPriceElement.textContent = 'Celková cena: ' + totalTotalPrice.toFixed(2) + ' Kč';
                                }
                            })
                            .catch(error => console.error('Error fetching Meal Plan API:', error));
                    })
                    .catch(error => console.error('Error fetching Prices API:', error));
            }
        }
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

    function checkRoomCapacity(adults, children, numberOfRooms, maxCapacity) {
        var totalCapacity = numberOfRooms * maxCapacity;

        if ((adults + children) > totalCapacity) {
            return 'Překročena maximální kapacita pro vybraný počet pokojů.';
        }

        return '';
    }

    var formFields = ['single_rooms', 'adults_single_rooms', 'children_single_rooms',
        'double_rooms', 'adults_double_rooms', 'children_double_rooms',
        'family_rooms', 'adults_family_rooms', 'children_family_rooms',
        'suite_rooms', 'adults_suite_rooms', 'children_suite_rooms',
        'meal_plan', 'transport', 'arrival_date', 'departure_date'];

    formFields.forEach(function (field) {
        document.getElementById(field).addEventListener('change', updateTotalPrice);
    });

    updateTotalPrice();
});