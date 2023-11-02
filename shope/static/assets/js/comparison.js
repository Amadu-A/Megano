(() => {
  window.onload = function() {
    $('.comparison-add').on('click', 'button[type="submit"]', function (e) {
      e.preventDefault();
      var data = {};
      data.product_id = product_id = $(this).attr('data-product_id');
      var csrf_token = $('meta[name="csrf-token"]').attr('content');
      console.log(csrf_token);
      var url = $(this).parents('.comparison-add').attr('action')
      console.log(url);
      data["csrfmiddlewaretoken"] = csrf_token;
      $.ajax({
        url: url,
        type: 'POST',
        data: data,
        cache: true,
        success: function (data) {
          console.log('OK');
          Swal.fire({title: data.message, confirmButtonColor: '#0041c2'})
        },
        error: function () {
          console.log("error")
          swal("error")
        }
      })
    })
  }
})();