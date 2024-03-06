const sourceImageFileInput = document.getElementById("id_image_src_input");
const cropDataFormInput = document.getElementById("id_crop_data_form_input");
const avatarRepresentation = document.getElementById("id_avatar_representation");
const imageCropperElement = document.getElementById("idOriginalImage");
const acceptCropImageButton = document.getElementById("idAcceptCropImageButton");
const imageCropperModalContainer = document.getElementById('idImageCropperModal');
const imageCropperBootstrapModalInstance = new bootstrap.Modal(imageCropperModalContainer);
const IMAGE_MAX_SIDE_LENGTH = 800;
let cropper, scaleFactor;

function imageCropperHandler() {
    prepareUploadedImage();
    cropModalWindowHandlers();
    acceptCropHandler();
}

function acceptCropHandler() {
    acceptCropImageButton.addEventListener("click", (e) => {
        let containerData = cropper.getContainerData();
        cropper.setCropBoxData({
            left: 0,
            top: 0,
            width: containerData.width,
            height: containerData.height,
        });
        cropper.crop();

        let cropData = cropper.getData();
        avatarRepresentation.src = cropImage(imageCropperElement, cropData);
        cropDataFormInput.value = JSON.stringify({
            "x_offset": cropData.x / scaleFactor,
            "y_offset": cropData.y / scaleFactor,
            "width": cropData.width / scaleFactor,
            "height": cropData.height / scaleFactor,
        })

        sourceImageFileInput.setAttribute("name", "image")
        imageCropperBootstrapModalInstance.hide();
    });
}

function cropModalWindowHandlers() {
    imageCropperModalContainer.addEventListener("shown.bs.modal", () => {
        cropper = new Cropper(imageCropperElement, {
            aspectRatio: 1,
            viewMode: 3,
            dragMode: 'move',
            autoCrop: false,
            guides: false,
            cropBoxMovable: false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
            minContainerWidth: 300,
            minContainerHeight: 300,
            minCanvasWidth: 300,
            minCanvasHeight: 300,
            minCropBoxWidth: 300,
            minCropBoxHeight: 300,
            autoCropArea: 1,
        });
    });

    imageCropperModalContainer.addEventListener("hidden.bs.modal", (e) => {
        cropper.destroy();
        cropper = null;
    });
}

// Resize the image if necessary, as there are issues with overly large images when cropping on iOS devices.
function prepareUploadedImage() {
    sourceImageFileInput.addEventListener("input", async function (e) {
        let [file] = sourceImageFileInput.files;

        const imgToResize = document.createElement('img');
        imgToResize.src = await fileToDataUri(file);
        await new Promise((resolve) => {
            imgToResize.onload = resolve;
        });

        scaleFactor = calculateScaleFactor(imgToResize.width, imgToResize.height)
        if (scaleFactor < 1) {
            imageCropperElement.src = resizeImage(imgToResize, scaleFactor);
        } else {
            imageCropperElement.src = imgToResize.src;
        }

        imageCropperBootstrapModalInstance.show();
    });
}

function fileToDataUri(file) {
    return new Promise((resolve) => {
        let reader = new FileReader();
        reader.addEventListener("load", () => {
            resolve(reader.result);
        });
        reader.readAsDataURL(file);
    });
}

function calculateScaleFactor(width, height) {
    let scaleFactor = 1;
    if (width > height) {
        if (width > IMAGE_MAX_SIDE_LENGTH) {
            scaleFactor = IMAGE_MAX_SIDE_LENGTH / width;
        }
    } else {
        if (height > IMAGE_MAX_SIDE_LENGTH) {
            scaleFactor = IMAGE_MAX_SIDE_LENGTH / height;
        }
    }

    return scaleFactor
}

function resizeImage(imgToResize, scaleFactor = 0.5) {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const canvasWidth = imgToResize.width * scaleFactor;
    const canvasHeight = imgToResize.height * scaleFactor;

    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    context.drawImage(imgToResize, 0, 0, canvasWidth, canvasHeight);

    return canvas.toDataURL();
}

function cropImage(image, cropData) {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = cropData.width;
    canvas.height = cropData.height;

    context.drawImage(image, cropData.x, cropData.y, cropData.width, cropData.height, 0, 0, cropData.width, cropData.height);

    return canvas.toDataURL();
}

document.addEventListener('DOMContentLoaded', function () {
    imageCropperHandler();

});