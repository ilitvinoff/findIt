const posterInput = $('#poster-input');
const posterInputLabel = $('.poster-input-label');

posterInput.on('change', function () {
    let image_element = $('#poster-preview');
    let image_container = $('.poster-preview-container');
    let file = posterInput[0].files[0];
    if (file === undefined) {
        image_container.hide();
        posterInputLabel.addClass('d-flex');
        posterInputLabel.removeClass('d-none');
        image_element[0].src = "";
    } else {
        image_container.show();
        posterInputLabel.removeClass('d-flex');
        posterInputLabel.addClass('d-none');
        image_element[0].src = URL.createObjectURL(file)
    }
});