const posterContainer = $('.poster-container');
const imagesTotalFormsInput = $('#id_images-TOTAL_FORMS');
const imagesFormsMaxNum = parseInt($('#id_images-MAX_NUM_FORMS').val());

function show(element) {
    element.removeClass('d-none');
    element.addClass('d-flex');
}

function hide(element) {
    element.removeClass('d-flex');
    element.addClass('d-none');
}

function getImageInput(parent) {
    return parent.find('input[type="file"]');
}

function getImagePreviewContainer(parent) {
    return parent.find('.preview-container');
}

function getImagePreviewEl(parent) {
    return parent.find('img');
}

function getImageContainerLabel(parent) {
    return parent.find('label');
}

function getImageContainerRemoveBtn(parent) {
    return parent.find('.remove-button');
}

function getImageContainerEditBtn(parent) {
    return parent.find('.edit-button');
}

function posterChangeHandler(posterContainer) {
    let label = getImageContainerLabel(posterContainer);
    let input = getImageInput(posterContainer);
    let previewContainer = getImagePreviewContainer(posterContainer);
    let previewImgEl = getImagePreviewEl(previewContainer);
    let removeBtn = getImageContainerRemoveBtn(previewContainer);
    let editBtn = getImageContainerEditBtn(previewContainer);

    input.on('change', function () {
        let file = input[0].files[0];
        hide(label);
        previewImgEl[0].src = URL.createObjectURL(file);
        show(previewContainer);
    });

    removeBtn.on('click', function (e) {
        hide(previewContainer);
        show(label);
        previewImgEl[0].src = "";
    });

    editBtn.on('click', function (e) {
        input.click();
    });
}

function setIdIndexToFormsetInputs(imageContainer, idIndex) {
    let imageInput = getImageInput(imageContainer);
    let label = getImageContainerLabel(imageContainer);

    imageInput.attr('id', `id_images-${idIndex}-file`);
    imageInput.attr('name', `images-${idIndex}-file`);
    label.attr('for', `id_images-${idIndex}-file`);
}

function offsetIdIndexToFormsetInputs(imageContainer, offset) {
    let imageInput = getImageInput(imageContainer);
    let label = getImageContainerLabel(imageContainer);

    let idIndex = parseInt(imageInput.attr('id').split('-')[1]) + offset;
    imageInput.attr('id', `id_images-${idIndex}-file`);
    imageInput.attr('name', `images-${idIndex}-file`);
    label.attr('for', `id_images-${idIndex}-file`);
}

function additionalImageAddHandler(templateContainer) {
    let input = getImageInput(templateContainer);
    let previewContainer = getImagePreviewContainer(templateContainer);
    let previewImgEl = getImagePreviewEl(previewContainer);
    let removeBtn = getImageContainerRemoveBtn(previewContainer);
    let templateClone = templateContainer.clone();

    input.on('change', function () {
        let cloneInput = getImageInput(templateClone);
        cloneInput.val('');

        previewImgEl[0].src = URL.createObjectURL(input[0].files[0]);
        templateContainer.removeClass('image-form-template');
        templateContainer.addClass('instantiated-image');

        let currentIdIndex = parseInt(imagesTotalFormsInput.val());
        imagesTotalFormsInput.val(currentIdIndex + 1);
        if (parseInt(imagesTotalFormsInput.val()) >= imagesFormsMaxNum) {
            templateClone.addClass('d-none');
        }

        setIdIndexToFormsetInputs(templateContainer, currentIdIndex);
        templateClone.insertAfter(templateContainer);
        additionalImageAddHandler(templateClone);
    });

    removeBtn.on('click', function (e) {
        let formsToResetId = templateContainer.nextAll('.instantiated-image');
        templateContainer.remove();
        formsToResetId.each(function (index, form) {
            offsetIdIndexToFormsetInputs($(form), -1);
        });

        let currentIdIndex = parseInt(imagesTotalFormsInput.val());
        imagesTotalFormsInput.val(currentIdIndex -1);

        if (templateClone.hasClass('d-none')) {
            templateClone.removeClass('d-none');
            templateClone.addClass('d-block');
        }
    });
}

$(document).ready(function () {
    posterChangeHandler(posterContainer);
    additionalImageAddHandler($('.image-form-template'));
});

