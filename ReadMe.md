# Eden

## Database
- Continent
  - Name
- Country
  - name
  - FK continent
- City
  - Name
  - FK Country
- Hotel
  - Name
  - Number of stars
  - Arrival date
  - Departure date
  - Meals - No meal, B&B, half-board, full-board, all-inclusive
  - Price per person
  - Price per child
  - Description
  - City FK city
- Airport
  - Name
  - FK city
- Buying a tour
  - Tour
  - Details about customer
  
## Function

- Home page
  - Display of promoted tours
  - Display of upcoming tours(globally)
  - Display of upcoming tours(by country)
  - Display of just purchased tours
  - Display of discounted tours
- Administrator
  - create, edit and add tours
- Search for tours according to criteria
  - Form for filtering and sorting results
  - Sorting by price, departure date
- Buying a tour
  - select and purchase tour
  - specifying the number of adults and children
  - Check availability
  - The number of vacancies will be reduced
  - Calculate price for the trip based on the nr. of people
  - Purchased tours are present on the administrative page
  - Add special requirements for tour