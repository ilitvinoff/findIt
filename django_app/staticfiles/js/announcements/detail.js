function initSwipers() {
    let slidesPerView = 4;
    if (screen.width < 768) {
        slidesPerView = 2;
    }

    if (document.querySelector('.thumbs-swiper')) {
        const thumbSwiper = new Swiper(".thumbs-swiper", {
            slidesPerView: slidesPerView,
            slidesPerGroup: 1,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            multipleActiveThumbs: false,
            freeMode: true,
            watchSlidesProgress: true,
            spaceBetween: 10,
            // direction: "vertical",
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
    } else {
        const swiper = new Swiper('.main-swiper', {
            loop: false,
            allowTouchMove: false,
            effect: 'fade',
            fadeEffect: {
                crossFade: true,
            },
            lazyPreloadPrevNext: 1,
        });
    }
}


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
    initSwipers();
    const deleteBtn = $('#delete-btn');
    const deleteForm = $('#deleteForm');
    deleteBtn.on("click", function (e) {
        e.preventDefault()
        Swal.fire({
            title: "Delete Announcement",
            text: `Are you sure you want to delete announcement?`,
            showCancelButton: true,
            confirmButtonText: "Delete",
        }).then(function (result) {
            if (result.isConfirmed) {
                deleteForm.submit();
            }
        })
    });

    $('.main-swiper-slide').on('click', function (e) {
        let index = parseInt(this.attributes['data-index'].value);
        gallerySwiper.slideTo(index, 0, false);

        e.preventDefault();
        openModalPerformerMedia();
    });

    $('#closeGalleryBtn').on('click', function (e) {
        closeModalPerformerMedia();
    });
});

