// javascript logic to set up stripe
// taken from stripe Documentation and modified as per project requirement.

// slice method to remove quotation mark on the key
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontSize: '14px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle validation errors on card element
card.addEventListener('change', (event) => {
    let errorMsg = document.getElementById("card-errors");
    if (event.error) {
        let html = `
            <p class="text-danger mt-1">
            <i class="fas fa-exclamation" aria-hidden="true"></i>
            ${event.error.message}</p>`;
        errorMsg.innerHTML = html;
    } else {
        errorMsg.textContent = "";
    }
});

// Handle form submission
let form = document.getElementById('checkout-form');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    // eventlistener prevent the form from submitting once user click the button
    // disable card element and trigger loading overlay
    card.update({ "disabled": true });
    $('#checkout-btn').attr('disabled', true);
    $('#checkout-form').fadeToggle(500);
    $('.loading-overlay').fadeToggle(500);


    let btnSave = document.getElementById('save-info');
    let saveInfo = false;
    if (btnSave) {
        saveInfo = Boolean($('btnSave').attr('checked'));
    }

    // Form using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };

    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.contact_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address.value),
                        postal_code: $.trim(form.postal_code.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.contact_number.value),
                address: {
                    line1: $.trim(form.street_address.value),
                    postal_code: $.trim(form.postal_code.value),
                }
            },
        }).then(function(outcome) {
            if (outcome.error) {
                let errorMsg = document.getElementById("card-errors");
                let html = `
                    <p class="text-danger mt-1">
                    <i class="fas fa-exclamation" aria-hidden="true"></i>
                    ${outcome.error.message}</p>`;
                errorMsg.innerHTML = html;
                $('#checkout-form').fadeToggle(500);
                $('.loading-overlay').fadeToggle(500);
                // re-enable card-element and checkout button for user if there is an error
                card.update({ "disabled": false });
                $('#checkout-btn').attr('disabled', false);

            } else {
                if (outcome.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // reload the page
        location.reload();
    });
});