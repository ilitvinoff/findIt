const thumbSwiper = new Swiper(".thumbs-swiper", {
    slidesPerView: 5,
    slidesPerGroup: 5,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    multipleActiveThumbs: false,
    freeMode: true,
    watchSlidesProgress: true,
    spaceBetween: 10,
    direction: "vertical",
    lazyPreloadPrevNext: 1,
});

const swiper = new Swiper('.main-swiper', {
    loop: false,
    allowTouchMove: false,
    thumbs: {
        swiper: thumbSwiper,
    },
    effect: 'fade',
    fadeEffect: {
        crossFade: true,
    },
    lazyPreloadPrevNext: 1,
});

const gallerySwiper = new Swiper('.gallery-swiper', {
    navigation: {
        nextEl: '.gallery-button-next',
        prevEl: '.gallery-button-prev',
    },
    lazyPreloadPrevNext: 1,
    spaceBetween: 10,
    watchSlidesProgress: true,
});

function openModalPerformerMedia() {
    $("#galleryContainer").addClass("active");
}

function closeModalPerformerMedia() {
    $("#galleryContainer").removeClass("active");
}

document.addEventListener('DOMContentLoaded', function () {
    $('.main-swiper-slide').on('click', function (e) {
        let index = parseInt(this.attributes['data-index'].value);
        gallerySwiper.slideTo(index, 0, false);

        e.preventDefault();
        // $('.media-modal-image-block img').attr('src', img_src);
        openModalPerformerMedia();
    });

    $('#closeGalleryBtn').on('click', function (e) {
        closeModalPerformerMedia();
    });
});

