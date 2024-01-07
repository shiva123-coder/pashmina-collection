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




// Handle color and size
// only show available color for the sizes and hide all unavailable colors for the same size
var sizes = [];
var colorDropdown = $('#colorDropdown');
var sizeDropdown = $('#sizeDropdown');
var errorMessage = $('#errorMessage');


// Populate sizes array
sizeDropdown.find('option').each(function() {
    var size = $(this).val();
    if (size && sizes.indexOf(size) === -1) {
        sizes.push(size);
    }
});

// Disable color dropdown initially
colorDropdown.prop('disabled', true);

sizeDropdown.change(function() {
    var selectedSize = $(this).val();

    // Show colors related to the selected size, hide others
    colorDropdown.find('option').each(function() {
        var sizeForColor = $(this).data('size');
        if (sizeForColor === selectedSize || sizeForColor === undefined) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });

    // Enable color dropdown if a size is selected
    colorDropdown.prop('disabled', !selectedSize);

    // hide error message once size is selected
    errorMessage.hide();
});


// Update the color dropdown with unique sizes
sizeDropdown.html('<option value="" disabled selected>Select Size</option>');
sizes.forEach(function(size) {
    sizeDropdown.append('<option value="' + size + '">' + size + '</option>');
});



// Handle if Add to basket button clicked without selecting the color
$("#add-to-basket-form").submit(function(event) {
    // Check if color is selected
    let colorDropdown = $("#colorDropdown");
    let errorMessage = $("#errorMessage");

    if (colorDropdown.val() === "" || colorDropdown.val() === null) {
        event.preventDefault(); // Prevent form submission
        errorMessage.html("Please select a color.").show(); // Show the error message
    } else {
        errorMessage.hide(); // Hide the error message if color is selected
    }
});


// Handle click event on small thumbnails
$('.small-thumbnail').on('click', function() {
    var mainImage = $('.main-image');
    var selectedColor = $(this).attr('data-color');
    mainImage.attr('src', $(this).attr('src'));
    mainImage.attr('data-color', selectedColor);
});


// Update product images based on selected color
$('#colorDropdown').change(function() {
    var selectedColor = $(this).val(); // Assuming the color value is the option value in the dropdown
    var mainImage = $('.main-image');

    // Update main image source and data-color attribute
    $('.small-thumbnail').each(function() {
        if ($(this).data('color') === selectedColor) {
            mainImage.attr('src', $(this).attr('src'));
            mainImage.data('color', selectedColor);
            return false; // Break the loop once a matching color is found
        }
    });
});