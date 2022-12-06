$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id_for_update").val(res.id);
        $("#product_name_for_update").val(res.name);
        $("#product_category_for_update").val(res.category);
        $("#product_description_for_update").val(res.description);
        $("#product_price_for_update").val(res.price);
        
        $("#product_like_for_update").val(0);
        
    }
    function update_form_data_for_create(res) {
        $("#product_id_created").val(res.id);
        
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_description").val("");
        $("#product_price").val("");
        $("#product_like").val("");

        $("#product_name_for_create").val("");
        $("#product_category_for_create").val("");
        $("#product_description_for_create").val("");
        $("#product_price_for_create").val("");
        $("#product_id_created").val("");

        $("#product_id_for_delete").val("");

        $("#product_id_for_update").val("");
        $("#product_name_for_update").val("");
        $("#product_category_for_update").val("");
        $("#product_description_for_update").val("");
        $("#product_price_for_update").val("");


        $("#product_id_for_list").val("");
        $("#product_name_for_list").val("");
        $("#product_category_for_list").val("");
        $("product_price_upper_bound").val("");
        $("product_price_lower_bound").val("");

        $("#product_id_for_like").val("");




    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#product_name_for_create").val();
        let category = $("#product_category_for_create").val();
        let description = $("#product_description_for_create").val();
        let price = $("#product_price_for_create").val();
        let like = $("#product_like_for_create").val();

        let data = {
            "name": name,
            "category": category,
            "description": description,
            "price": price,
            "like": like
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data_for_create(res)
            flash_message("SUCCESS")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id_for_update").val();
        let name = $("#product_name_for_update").val();
        let category = $("#product_category_for_update").val();
        let description = $("#product_description_for_update").val();
        let price = $("#product_price_for_update").val();
        let like = $("#product_like_for_update").val();

        let data = {
            "name": name,
            "category": category,
            "description": description,
            "price": price,
            "like": like
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Pet
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id_for_update").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#like-btn").click(function () {

        let product_id = $("#product_id_for_like").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/products/${product_id}/like`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Description</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Like</th>'
            table += '</tr></thead><tbody>'
            for(let i = 0; i < 1; i++) {
                table +=  `<tr id="row_${i}"><td>${res.id}</td><td>${res.name}</td><td>${res.category}</td><td>${res.description}</td><td>${res.price}</td><td>${res.like}</td></tr>`;
                
            }
            // table += '<tr id="row_0"><td>${res[0].id}</td><td>${res[0].name}</td><td>${res[0].category}</td><td>${res[0].description}</td><td>${res[0].price}</td><td>${res[0].like}</td></tr>';         
            table += '</tbody></table>';
            $("#search_results").append(table);
            flash_message("Product like count increment by 1!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/pets?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstPet = "";
            for(let i = 0; i < res.length; i++) {
                let pet = res[i];
                table +=  `<tr id="row_${i}"><td>${pet.id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
                if (i == 0) {
                    firstPet = pet;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
