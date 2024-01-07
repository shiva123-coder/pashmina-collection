// sort option from the select box
$('#sort-selection').change(function() {
    let sort_selector = $(this);
    let currentUrl = new URL(window.location);
    let selectedVal = sort_selector.val();

    if (selectedVal != "reset") {
        let sort = selectedVal.split("_")[0];
        let direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.href = currentUrl.toString();
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.href = currentUrl.toString();
    }
});

// prevent submiting the page directly once plus(+) button clicked
$('.increase-qty').click(function(e) {
    e.preventDefault();
    var newInput = $(this).closest('.input-group').find('.qty_input');
    var newValue = parseInt($(newInput).val());
    // + button disable once input value reach 10
    if (newValue >= 10) {
        $('.increase-qty').disabled = true;
    } else {
        $(newInput).val(newValue + 1);
    }
});

// // prevent submiting the page directly once minus(-) button clicked
$('.decrease-qty').click(function(e) {
    e.preventDefault();
    var newInput = $(this).closest('.input-group').find('.qty_input');
    var newValue = parseInt($(newInput).val());
    // + button disable to restric user from iputting the quantity less than 1
    if (newValue <= 1) {
        $('decrease-qty').disabled = true;
    } else {
        $(newInput).val(newValue - 1);
    }
});