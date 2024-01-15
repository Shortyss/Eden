function updateTime() {
    var dateTimeElement = document.getElementById("date-time");

    if (!dateTimeElement) {
        console.error('Element with id "date-time" not found.');
        return;
    }

    var now = new Date();

    var options = {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
    };
    var formattedDateTime = "Dnes je " + now.toLocaleDateString('cs-CZ', options);

    dateTimeElement.textContent = formattedDateTime;
}

updateTime();

document.addEventListener('DOMContentLoaded', function () {
    function checkRoomCapacity(adults, children, numberOfRooms, maxCapacity) {
        var totalCapacity = numberOfRooms * maxCapacity;

        if ((adults + children) > totalCapacity) {
            return 'Překročena maximální kapacita pro vybraný počet pokojů.';
        }

        return '';
    }

    function updateTotalPrice() {
        var maxCapacitySingleRooms = 1;
        var maxCapacityDoubleRooms = 2;
        var maxCapacityFamilyRooms = 4;
        var maxCapacitySuiteRooms = 6;

        var adultsSingleRooms = parseInt(document.getElementById('adults_single_rooms').value);
        var childrenSingleRooms = parseInt(document.getElementById('children_single_rooms').value);
        var numberOfSingleRooms = parseInt(document.getElementById('single_rooms').value);
        document.getElementById('error_adults_single_rooms').innerText = calculateRoomPrice(adultsSingleRooms, childrenSingleRooms, numberOfSingleRooms, maxCapacitySingleRooms);

        var adultsDoubleRooms = parseInt(document.getElementById('adults_double_rooms').value);
        var childrenDoubleRooms = parseInt(document.getElementById('children_double_rooms').value);
        var numberOfDoubleRooms = parseInt(document.getElementById('double_rooms').value);
        document.getElementById('error_adults_double_rooms').innerText = calculateRoomPrice(adultsDoubleRooms, childrenDoubleRooms, numberOfDoubleRooms, maxCapacityDoubleRooms);

        var adultsFamilyRooms = parseInt(document.getElementById('adults_family_rooms').value);
        var childrenFamilyRooms = parseInt(document.getElementById('children_family_rooms').value);
        var numberOfFamilyRooms = parseInt(document.getElementById('family_rooms').value);
        document.getElementById('error_adults_family_rooms').innerText = calculateRoomPrice(adultsFamilyRooms, childrenFamilyRooms, numberOfFamilyRooms, maxCapacityFamilyRooms);

        var adultsSuiteRooms = parseInt(document.getElementById('adults_suite_rooms').value);
        var childrenSuiteRooms = parseInt(document.getElementById('children_suite_rooms').value);
        var numberOfSuiteRooms = parseInt(document.getElementById('suite_rooms').value);
        document.getElementById('error_adults_suite_rooms').innerText = calculateRoomPrice(adultsSuiteRooms, childrenSuiteRooms, numberOfSuiteRooms, maxCapacitySuiteRooms);



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
