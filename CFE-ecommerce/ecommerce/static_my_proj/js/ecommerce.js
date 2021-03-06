$(document).ready(function () {
    // Contact Form Handler
    let contactForm = $(".contact-form")
    let contactFormMethod = contactForm.attr("method")
    let contactFormEndPoint = contactForm.attr("action")

    function displaySubmitting(submitButton, defaultText, doSubmit){
        if(doSubmit){
            submitButton.addClass("disabled")
            submitButton.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        }else{
            submitButton.removeClass("disabled")
            submitButton.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()
        let contactFormData = contactForm.serialize()
        let thisForm = $(this)

        let contactFormSubmitButton = contactForm.find("[type='submit']")
        let contactFormSubmitButtonTxt = contactFormSubmitButton.text()

        displaySubmitting(contactFormSubmitButton, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndPoint,
            data: contactFormData,
            success: function(data){
                // Empty out the form
                thisForm[0].reset()
                $.alert({
                    "title" : "Success",
                    "content" : data.message,
                    "theme" : "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitButton, contactFormSubmitButtonTxt, false)
                }, 2000)
            },
            error: function(error){
                console.log(error.responseJSON)

                let jsonData = error.responseJSON
                let msg = ""

                // jsonData is a dictionary.
                // That is how you will iterate through
                // the dictionary
                $.each(jsonData, function(key, val){
                    msg += key + ": " + val[0].message + "<br/>"
                })
                $.alert({
                    "title" : "Alert",
                    "content" : msg,
                    "theme" : "modern",
                })

                setTimeout(function(){
                    displaySubmitting(contactFormSubmitButton, contactFormSubmitButtonTxt, false)
                }, 2000)
            }
        })
    })


        // Auto Search
        let searchForm = $(".search-from")
        let searchInput = searchForm.find("[name='q']")

        // Change the search button to teh loading icon
        let searchBtn = searchForm.find("[type='submit']")

        let typingTimer;
        let typingInterval = 500 // 0.5 seconds

        // When the key pressing comes up, key os released
        searchInput.keyup(function(event){
            clearTimeout(typingTimer)
            typingTimer = setTimeout(performSearch, typingInterval)
        })

        // When teh key os pressed at the very beginning
        searchInput.keydown(function(event){
            clearTimeout(typingTimer)
        })

        function displaySearching(){
            searchBtn.addClass("disabled")
            searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
        }

        function performSearch(){
            displaySearching()
            let query = searchInput.val()
            setTimeout(function(){
                window.location.href = "/search/?q=" + query
            }, 1000)

        }


        // Cart + Add Product
        let productForm = $(".form-product-ajax")
        productForm.submit(function(event){
            event.preventDefault();
            console.log("Form is not sending")

            // We want to know the URL the submit is going to
            // the method that is associated with it

            let thisForm = $(this)
            //let actionEndPoint = thisForm.attr("action");
            let actionEndPoint = thisForm.attr("data-endpoint")
            let httpMethod = thisForm.attr("method");
            let formData = thisForm.serialize();


            $.ajax({
                url: actionEndPoint,
                method : httpMethod,
                data : formData,
                success : function(data){
                    let submitSpan = thisForm.find(".submit-span")
                    if(data.added){
                        submitSpan.html("In cart<button type=\"submit\" class=\"btn btn-link\">Remove?</button>")
                    }
                    else{
                        submitSpan.html("<button class=\"btn btn-success\">Add to cart</button>")
                    }

                    // Update the count of items displayed on the cart icon
                    let navBarCount = $(".navbar-cart-count")
                    navBarCount.text(data.cartItemCount)

                    // Check the window location
                    if(window.location.href.indexOf("cart") -1){
                        refreshCart()
                    }
                },
                error: function(errorData){
                    // jQuery Confirm
                    $.alert({
                        title : "Alert",
                        content: "An error occurred",
                        theme: "Modern",
                    })
                    console.log("Error")
                    console.log(errorData)
                }
            })
        })

        function refreshCart(){
            // A helper function to make sure that the
            // cart page is updated when "Remove" is pressed upon

            let cartTable = $(".cart-table")
            let cartBody = cartTable.find(".cart-body")
            let currentUrl = window.location.href
            let productRows = cartBody.find(".cart-product")
            let refreshCartUrl = "/api/cart/"
            // Using the GET method to uodate the cart
            // Actually using the POST data to refresh the page
            let refreshCartMethod = "GET"

            $.ajax({
                url: refreshCartUrl,
                method: refreshCartMethod,
                data: {},
                success: function(data){
                    let hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                    if(data.products.length > 0){
                        productRows.html(" ")
                        i = data.products.length
                        $.each(data.products, function(index, value){
                            let newCartItemRemove = hiddenCartItemRemoveForm.clone()
                            newCartItemRemove.css("display", "block")

                            newCartItemRemove.find(".cart-item-product-id").val(value.id)
                            cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>"
                                + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                            i --
                        })

                        cartBody.find(".cart-subtotal").text(data.subtotal)
                        cartBody.find(".cart-total").text(data.total)
                    }else{
                        window.location.href = currentUrl
                    }
                },
                error: function(errorData){
                    $.alert({
                        title: "Alert",
                        content: "Refreshing Cart Failed",
                        theme: "modern",
                    })
                }
            })
        }
    })