$(document).ready(function () {
    $("#loadMore").on('click', function () {
        var _currentProducts = $(".product").length;
        var _limit = $(this).attr('data-limit');
        var _total = $(this).attr('data-total');
        // Start Ajax
        $.ajax({
            url: '/load-more-data',
            data: {
                limit: _limit,
                offset: _currentProducts
            },
            dataType: 'json',
            beforeSend: function () {
                $("#loadMore").attr('disabled', true);
            },
            success: function (res) {
                $("#filteredProducts").append(res.data);
                $("#loadMore").attr('disabled', false);

                var _totalShowing = $(".product").length;
                if (_totalShowing == _total) {
                    $("#loadMore").remove();
                }
            }
        });
        // End
    });

    // Product Variation
    $("input[type='radio']").click(function () {
        $('.product-price-money').text($(this).val());
    });

    // add to cart
    $(document).on('click', ".add-to-cart", function () {
        var _vm = $(this);
        var _index = _vm.attr('data-index');
        var _qty = $(".product-qty-" + _index).val();
        var _productId = $(".product-id-" + _index).val();
        var _productImage = $(".product-image-" + _index).val();
        var _productTitle = $(".product-title-" + _index).val();
        var _productPrice = $(".product-price-" + _index).text();
        // Ajax
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': _productId,
                'image': _productImage,
                'qty': _qty,
                'title': _productTitle,
                'price': _productPrice
            },
            dataType: 'json',
            beforeSend: function () {
                _vm.attr('disabled', true);
            },
            success: function (res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
            }
        });
        // End
    });

    // Delete item from cart
    $(document).on('click', '.delete-item', function () {
        var _pId = $(this).attr('data-item');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': _pId,
            },
            dataType: 'json',
            beforeSend: function () {
                _vm.attr('disabled', true);
            },
            success: function (res) {
                $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartList").html(res.data);
            }
        });
        // End
    });

    // Update item from cart
    $(document).on('click', '.update-item', function () {
        var _pId = $(this).attr('data-item');
        var _pQty = $(".product-qty-" + _pId).val();
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/update-cart',
            data: {
                'id': _pId,
                'qty': _pQty
            },
            dataType: 'json',
            beforeSend: function () {
                _vm.attr('disabled', true);
            },
            success: function (res) {
                // $(".cart-list").text(res.totalitems);
                _vm.attr('disabled', false);
                $("#cartList").html(res.data);
            }
        });
        // End
    });

    // Add wishlist
    $(document).on('click', ".add-wishlist", function () {
        var _pid = $(this).attr('data-product');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: "/add-wishlist",
            data: {
                product: _pid
            },
            dataType: 'json',
            success: function (res) {
                if (res.bool == true) {
                    _vm.addClass('disabled').removeClass('add-wishlist');
                }
            }
        });
        // EndAjax


    });
    // End

    // Activate selected address
    $(document).on('click', '.activate-address', function () {
        var _aId = $(this).attr('data-address');
        var _vm = $(this);
        // Ajax
        $.ajax({
            url: '/activate-address',
            data: {
                'id': _aId,
            },
            dataType: 'json',
            success: function (res) {
                if(res.bool==true){
                	$(".check").hide();
                	$(".wrong").show();
                    $(".addressbook-item-status-text").html("Status - Inactive");
                	$(".actbtn").show();

                	$(".check"+_aId).show();
                	$(".wrong"+_aId).hide();
                	$(".addressbook-item-status-text"+_aId).html("Status - Active");
                	$(".btn"+_aId).hide();
                }
            }
        });
        // End
    });
});
// End Document.Ready

// Product Review Save
$("#addForm").submit(function (e) {
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function (res) {
            if (res.bool == true) {
                $(".ajaxRes").html('Your review has been added.');
                $("#reset").trigger('click');
                // Hide Button
                $("#reviewModel-trigger").hide();
                // End
                // create data for review
                var _html = '<div class="product-review-card">';
                _html += '<div class="product-review-user"><h1 class="product-review-user-name">' + res.data.user + '</h1></div>';
                _html += '<div class="product-review-content"><p class="product-review">' + res.data.review_text + '</p></div>';
                _html += '<div class="product-review-stars-container">';
                for (var i = 1; i <= res.data.review_rating; i++) {
                    _html += '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke-width="2"  stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"> </polygon> </svg>';
                }
                _html += '</div>';
                _html += '</div>';

                // Prepend Data
                $(".product-review-cards-container").prepend(_html);

                // Hide Modal
                $("#productReview").modal('hide');

                // AVg Rating
                $(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
            }
        }
    });
    e.preventDefault();
});
// End