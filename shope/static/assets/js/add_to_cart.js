console.log("файл работает")

function cart_add(product_id, product_name, image, product_count, amount, seller){
// Функция отправляет запрос на добавление товара в корзину

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/add',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id,
           'product_name': product_name,
           'image': image,
           'count': product_count,
           'amount': amount,
           'seller': seller},

    dataType: 'json',
    success: (data) => {

    $('.CartBlock-block').html(data.result)
    Swal.fire({title: data.message, confirmButtonColor: '#0041c2',

})
    },
    error: (error) => {
    console.log(error)}
    });

};

$('.Card-hover').on('click', 'a[class="Card-btn cart-btn"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на главной странице

    var product_id = $(this).parents('.Card').data('product')
    var product_count = 1
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $(this).parents('.Card').children('form').children('.Card-picture').data('name')

    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('.Product').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на детальной странице продукта

    var product_id = $('.Product').attr('id')
    var product_count = $('.Amount-input.form-input').attr('value')
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $('.ProductCard-pict').attr('href')

    cart_add(product_id, product_name, image, product_count, amount, seller)

})

$('#cart-add').on('click', 'a[class="btn btn_primary"]', function(){
   // Обработка нажатия на кнопку добавления товара в корзину на странице сравнения

    var product_id = $(this).data('product')
    var product_count = 1
    var amount = $(this).data('value')
    var seller = $(this).data('seller')
    var product_name = $(this).data('name')
    var image = $(this).data('image')

    cart_add(product_id, product_name, image, product_count, amount, seller)
})

$('.Amount').on('click', 'button[class="Amount-add"]', function(){

    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) + 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

})


$('.Amount').on('click', 'button[class="Amount-remove"]', function(){

    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')
    $(this).parent('.Amount').children('.Amount-input.form-input').attr('value', parseInt(count_product) - 1)
    var count_product = $(this).parent('.Amount').children('.Amount-input.form-input').attr('value')

})

