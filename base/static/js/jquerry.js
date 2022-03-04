$(document).ready(function() {
    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        
        var product_id = $(this).closest('.product-info').find('.prod-id').val();
        var product_quantity = $(this).closest('.product-info').find('.qty').val();
        var product_name = $(this).closest('.product-info').find('.prod-name').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: '/add-to-cart',
            data: {
                'product_id': product_id,
                'product_name':product_name,
                'product_quantity': product_quantity,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {  
                console.log(response)
                alertify.success(response.status)
            }
        });
    });

    $('.edit-cart').click(function (e) {
        e.preventDefault();
        
        var product_id = $(this).closest('.product-info').find('.prod-id').val();
        var product_quantity = $(this).closest('.product-info').find('.qty').val();
        var product_name = $(this).closest('.product-info').find('.prod-name').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: '/edit-cart',
            data: {
                'product_id': product_id,
                'product_name':product_name,
                'product_quantity': product_quantity,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {  
                console.log(response)
                alertify.success(response.status)
            }
        });
    });

    $('.delete-item-cart').click(function () {

        
        var product_id = $(this).closest('.product-info').find('.prod-id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: '/delete-item-cart',
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {  
                $('.cartdata').load(location.href+" .cartdata")
                location.reload(true);
            }
        });

        
    });


});