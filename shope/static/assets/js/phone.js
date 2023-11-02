IMask(
    document.getElementById('phone'),
    {
        mask: '+{7}(000)000-00-00'
    }
)

const el_name = document.getElementById("name");
document.getElementById("user-name").textContent = el_name.value;
el_name.oninput = function () {
    document.getElementById("user-name").textContent = el_name.value;
};

const el_phone = document.getElementById("phone");
document.getElementById("user-phone").textContent = el_phone.value;
el_phone.oninput = function () {
    document.getElementById("user-phone").textContent = el_phone.value;
};

const el_email = document.getElementById("mail");
document.getElementById("user-email").textContent = el_email.value;


function payChange(src) {
    document.getElementById("order-pay").textContent = src.value
}

const el_city = document.getElementById("city");
el_city.oninput = function () {
    document.getElementById("order-city").textContent = el_city.value;
};

const el_address = document.getElementById("address");
el_address.oninput = function () {
    document.getElementById("order-address").textContent = el_address.value;
};


function deliveryChange(src) {
    document.getElementById("order-delivery").textContent = src.value
    var csrf = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
        // url: "{% url 'order_app:delivery-type' %}",
        url: "/order/delivery-type/",
        type: 'POST',
        headers: { "X-CSRFToken": csrf },
        data: { 'delivery_type': src.value },
        success: function (responce) {
            document.getElementById("order-cost-delivery").textContent = responce.cost_delivery
            document.getElementById("Cart-price").textContent = responce.total_amount
            document.getElementById("Total-amount-value").value = responce.total_amount
        },

        error: function (responce) {
            alert('error')
        }

    }
    )
}

