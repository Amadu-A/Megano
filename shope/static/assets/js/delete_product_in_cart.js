console.log("файл работает")

function product_delete(product_id){
// Функция отправляет запрос на удаление товара из корзины

var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
    url: '/cart/delete',
    type: 'POST',
    headers: {"X-CSRFToken": csrf},
    data: {'product': product_id},
    dataType: 'json',
    success: (data) => {
    $('.CartBlock-block').html(data.cart)
    $('.Cart-block.Cart-block_total').html(data.total_amount)
    $('.form.Cart').html(data.new_qs)
//    $('.Cart-product[id="' + product_id  + '"' ).remove()

    },
    error: (error) => {
    console.log(error)}
    });

};

$('.Cart-block.Cart-block_delete').on('click', 'a[class="Cart-delete"]', function(){
    // Обработка нажатия на кнопку удаления товаров из корзину

    var product_id = $(this).parents(".Cart-product").attr("id")

   product_delete(product_id)
})