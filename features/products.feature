Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

    Background:
        Given the following products
            | name   | category | description    | price | like |
            | iphone | apple    | This is iphone | 2000  | 5    |
            | ipad   | pad      | This is Ipad   | 3000  | 9    |
            | AK-47  | gun      | Good Luck      | 2500  | 222  |
            | AK-47  | toy      | Reloading      | 250   | 202  |

    Scenario: The server is running
        When I visit the "home page"
        Then I should see "Product Demo RESTful Service" in the title
        And I should not see "404 Not Found"


    Scenario: Create a Product
        When I visit the "home page"
        And I set the "Name for create" to "iphone"
        And I set the "Category for create" to "apple"
        And I set the "Description for create" to "This is iphone"
        And I set the "Price for create" to "2000"
        And I press the "Create" button
        Then I should see the message "SUCCESS"

    Scenario: Like a Product
        When I visit the "home page"
        And I set the "Name for create" to "Switch"
        And I set the "Category for create" to "Gamming"
        And I set the "Description for create" to "This is Switch"
        And I set the "Price for create" to "3999"
        And I press the "Create" button
        Then I should see the message "SUCCESS"
        When I copy the "Id Created" field
        And I press the "Clear" button
        Then the "Id Created" field should be empty
        And the "Name for create" field should be empty
        And the "Category for create" field should be empty
        And the "Description for create" field should be empty
        And the "Price for create" field should be empty
        When I paste the "ID for Like" field
        And I press the "Like" button
        Then I should see the message "Product like count increment by 1!"
        And I should see "1" in the results

    Scenario: List all products
        When I visit the "home page"
        And I press the "List All" button
        Then I should see the message "SUCCESS"
        And I should see "iphone" in the results
        And I should see "ipad" in the results
        And I should see "AK-47" in the results
        And I should not see "pig" in the results


    Scenario: List products by name
        When I visit the "home page"
        And I set the "Name for List" to "AK-47"
        And I press the "List By Name" button
        Then I should see the message "SUCCESS"
        And I should see "AK-47" in the results
        And I should see "AK-47" in the results
        And I should see "AK-47" in the results
        And I should not see "ipad" in the results

    Scenario: List products by category
        When I visit the "home page"
        And I set the "Category for List" to "apple"
        And I press the "List By Category" button
        Then I should see the message "SUCCESS"
        And I should see "iphone" in the results
        And I should not see "ipad" in the results
        And I should not see "AK-47" in the results
        And I should see "2000" in the results

    Scenario: List products by price range
        When I visit the "home page"
        And I set the "Price Upper Bound" to "10000"
        And I set the "Price Lower Bound" to "500"
        And I press the "List By Price" button
        Then I should see the message "SUCCESS"
        And I should see "ipad" in the results
        And I should see "AK-47" in the results
        And I should not see "toy" in the results


    Scenario: Update a Product
        When I visit the "Home Page"
        And I set the "Name for create" to "iphone"
        And I set the "Category for create" to "apple"
        And I set the "Description for create" to "This is iphone"
        And I set the "Price for create" to "2000"
        And I press the "Create" button
        Then I should see the message "SUCCESS"
        When I copy the "Id created" field
        And I paste the "Id for update" field
        And I press the "Retrieve" button
        Then I should see the message "SUCCESS"
        And I should see "iphone" in the "Name for Update" field
        When I change "Name for Update" to "ipad"
        And I press the "Update" button
        Then I should see the message "SUCCESS"
        When I press the "Retrieve" button
        Then I should see the message "SUCCESS"
        And I should see "ipad" in the "Name for Update" field

    Scenario: Delete a Product
        When I visit the "home page"
        And I set the "Name for create" to "coffee"
        And I set the "Category for create" to "drink"
        And I set the "Description for create" to "This is coffee"
        And I set the "Price for create" to "20"
        And I press the "Create" button
        Then I should see the message "SUCCESS"
        When I copy the "Id created" field
        And I press the "Clear" button
        Then the "Id Created" field should be empty
        And the "Name for create" field should be empty
        And the "Category for create" field should be empty
        And the "Description for create" field should be empty
        And the "Price for create" field should be empty
        When I press the "List all" button
        Then I should see the message "SUCCESS"
        And I should see "coffee" in the results
        When I paste the "ID for Delete" field
        And I press the "Delete" button
        Then I should see the message "Product has been Deleted!"
        When I press the "List all" button
        Then I should see the message "SUCCESS"
        And I should not see "coffee" in the results

    Scenario: List products by id
        When I visit the "home page"
        And I set the "Name for create" to "Switch"
        And I set the "Category for create" to "Gamming"
        And I set the "Description for create" to "This is Switch"
        And I set the "Price for create" to "3999"
        And I press the "Create" button
        Then I should see the message "SUCCESS"
        When I copy the "Id Created" field
        And I press the "Clear" button
        Then the "Id Created" field should be empty
        And the "Name for create" field should be empty
        And the "Category for create" field should be empty
        And the "Description for create" field should be empty
        And the "Price for create" field should be empty
        When I paste the "ID for List" field
        And I press the "List By ID" button
        Then I should see the message "SUCCESS"
        And I should see "Switch" in the results