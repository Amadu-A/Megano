console.log("файл работает")

function cart_edit(product_id, count, seller){
// Функция отправляет запрос на изменение кол-ва товаров в корзине

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/change',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id, 'count': count, 'seller': seller},
    dataType: 'json',
    success: (data) => {

    $('.CartBlock-block').html(data.cart)
    $('.form.Cart').html(data.new_qs)
    $('.Cart-block.Cart-block_total').html(data.total_amount)
    },
    error: (error) => {

    }
    });

};

$('div[name="amount-cart"]').on('click', 'button[class="Amount-add"]', function(){
    // Обработка нажатия на кнопку добавления кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) + 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = true
    var seller = $(this).attr('name')

    cart_edit(product_id, count, seller)
})

$('div[name="amount-cart"]').on('click', 'button[class="Amount-remove"]', function(){
    // Обработка нажатия на кнопку уменьшения кол-ва товаров в корзине
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) - 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    var product_id = $(this).parents(".Cart-product").attr("id")
    var count = false
    var seller = $(this).parent('.Amount').children('.Amount-add').attr('name')

    if(count_product == 0){
        product_delete(product_id)
    }
    else{
        cart_edit(product_id, count, seller)
    }
})
