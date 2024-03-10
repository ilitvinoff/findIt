const posterContainer = $('.poster-container');
const imagesTotalFormsInput = $('#id_images-TOTAL_FORMS');
const imagesFormsMaxNum = parseInt($('#id_images-MAX_NUM_FORMS').val());
const initialRemoveButtons = $('.remove-button.initial');
const removedImagesCount = {value: 0};
const currentEmptyFormTemplateEl = {value: $('.image-form-template')};

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

function getImageDeleteInput(parent) {
    return parent.find('input[type="checkbox"]');
}

function getImageHiddenInputs(parent) {
    return parent.find('input[type="hidden"]');
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
    let deleteInput = getImageDeleteInput(posterContainer);
    let previewContainer = getImagePreviewContainer(posterContainer);
    let previewImgEl = getImagePreviewEl(previewContainer);
    let removeBtn = getImageContainerRemoveBtn(previewContainer);
    let editBtn = getImageContainerEditBtn(previewContainer);

    input.on('change', function () {
        let file = input[0].files[0];
        hide(label);
        previewImgEl[0].src = URL.createObjectURL(file);
        show(previewContainer);
        deleteInput.removeAttr('checked');
    });

    removeBtn.on('click', function (e) {
        hide(previewContainer);
        show(label);
        previewImgEl[0].src = "";
        deleteInput.attr('checked', 'checked');
    });

    editBtn.on('click', function (e) {
        input.click();
    });
}

function setIdIndexToFormsetInputs(imageContainer, idIndex) {
    let imageInput = getImageInput(imageContainer);
    let imageLabel = getImageContainerLabel(imageContainer);
    let imageDeleteCheckbox = getImageDeleteInput(imageContainer);
    let formsetHiddenInputs = getImageHiddenInputs(imageContainer);

    imageInput.attr('id', `id_images-${idIndex}-file`);
    imageInput.attr('name', `images-${idIndex}-file`);
    imageLabel.attr('for', `id_images-${idIndex}-file`);
    imageDeleteCheckbox.attr('id', `id_images-${idIndex}-DELETE`);
    formsetHiddenInputs.each(function (index, input) {
        let $input = $(input);
        $input.attr('id', `id_images-${idIndex}-${$input.attr('id').split('-')[2]}`);
        $input.attr('name', `id_images-${idIndex}-${$input.attr('name').split('-')[2]}`);
    });
}

function offsetIdIndexToFormsetInputs(imageContainer, offset) {
    let imageInput = getImageInput(imageContainer);
    let idIndex = parseInt(imageInput.attr('id').split('-')[1]) + offset;
    setIdIndexToFormsetInputs(imageContainer, idIndex);
}

function additionalImageAddHandler(templateContainer) {
    let input = getImageInput(templateContainer);
    let previewContainer = getImagePreviewContainer(templateContainer);
    let previewImgEl = getImagePreviewEl(previewContainer);
    let removeBtn = getImageContainerRemoveBtn(previewContainer);

    input.on('change', function () {
        let templateClone = templateContainer.clone();
        currentEmptyFormTemplateEl.value = templateClone;
        let cloneInput = getImageInput(currentEmptyFormTemplateEl.value);
        cloneInput.val('');

        previewImgEl[0].src = URL.createObjectURL(input[0].files[0]);
        templateContainer.removeClass('image-form-template');
        templateContainer.addClass('instantiated-image');

        let currentIdIndex = parseInt(imagesTotalFormsInput.val());
        imagesTotalFormsInput.val(currentIdIndex + 1);
        if (parseInt(imagesTotalFormsInput.val()) >= imagesFormsMaxNum + removedImagesCount.value) {
            currentEmptyFormTemplateEl.value.addClass('d-none');
        }

        setIdIndexToFormsetInputs(templateContainer, currentIdIndex);
        currentEmptyFormTemplateEl.value.insertAfter(templateContainer);
        additionalImageAddHandler(currentEmptyFormTemplateEl.value);
    });

    removeBtn.on('click', function (e) {
        let formsToResetId = templateContainer.nextAll('.instantiated-image');
        templateContainer.remove();
        formsToResetId.each(function (index, form) {
            offsetIdIndexToFormsetInputs($(form), -1);
        });

        let currentIdIndex = parseInt(imagesTotalFormsInput.val());
        imagesTotalFormsInput.val(currentIdIndex - 1);

        if (currentEmptyFormTemplateEl.value.hasClass('d-none')) {
            currentEmptyFormTemplateEl.value.removeClass('d-none');
            currentEmptyFormTemplateEl.value.addClass('d-block');
        }
    });
}

function initialImagesDeleteHandler() {
    initialRemoveButtons.on('click', function (e) {
        let checkbox = $(`#${$(this).attr('data-checkbox_id')}`);
        checkbox.attr('checked', 'checked');
        checkbox.parent().addClass('d-none');
        removedImagesCount.value += 1;

        if (currentEmptyFormTemplateEl.value.hasClass('d-none')) {
            currentEmptyFormTemplateEl.value.removeClass('d-none');
            currentEmptyFormTemplateEl.value.addClass('d-block');
        }
    });
}

$(document).ready(function () {
    initialImagesDeleteHandler();
    posterChangeHandler(posterContainer);
    additionalImageAddHandler($('.image-form-template'));
});

