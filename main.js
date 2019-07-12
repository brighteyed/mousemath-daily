const swiper = require('swiper');

const main = {
    run: () => {
        window.addEventListener('load', () => {
            const fullscreenView = document.querySelector('.fullscreen-view');
            let swiper = null;

            fullscreenView.addEventListener('click', e => {
                const closeButton = e.target.closest('.close');
                if (closeButton) {
                    fullscreenView.style.opacity = 0;
                    setTimeout(() => {
                        fullscreenView.innerHTML = "";
                        fullscreenView.style.display = "none";
                        if (swiper) {
                            swiper.keyboard.enable();
                        }
                    }, 300);
                }
            });

            document.addEventListener('click', e => {
                const photo = e.target.closest('.photos div');
                if (photo) {
                    const fullscreen = `
                            <button class="close">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#fff" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
                            </button>
                
                            <div style='background-image: ${photo.style.backgroundImage};'>
                            </div>`;
                    
                    fullscreenView.innerHTML = fullscreen;
                    fullscreenView.style.display = "block";
                    fullscreenView.style.opacity = 1;
                }
            });

            document.addEventListener('keyup', e => {
                if (e.key == 'Escape') {
                    fullscreenView.style.opacity = 0;
                    setTimeout(() => {
                        fullscreenView.innerHTML = "";
                        fullscreenView.style.display = "none";
                        if (swiper) {
                            swiper.keyboard.enable();
                        }
                    }, 300);
                }
            });

            if (document.querySelector('.swiper-container')) {
                swiper = new Swiper('.swiper-container', {
                    grabCursor: true,
                    keyboard: {
                        enabled: true,
                    },
                    pagination: {
                        el: '.swiper-pagination',
                        clickable: true,
                    },
                    spaceBetween: 10,
                });

                swiper.on('click', (e) => {
                    fullscreenView.style.opacity = 0;
                    fullscreenView.style.display = "block";

                    const fullscreen = `
                            <div class="swiper-fullscreen">
                                <button class="close">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#fff" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
                                </button>

                                <div class="swiper-wrapper">
                                    ${e.target.parentNode.innerHTML}
                                </div>
                            </div>`;
                    
                    fullscreenView.innerHTML = fullscreen;
                    const fullscreenSwiper = new Swiper('.swiper-fullscreen', {
                        initialSlide: swiper.activeIndex,

                        keyboard: {
                            enabled: true,
                        },

                        spaceBetween: 10,
                    });

                    fullscreenView.style.opacity = 1;
                    swiper.keyboard.disable();
                });
            }
        });
    }
};

main.run();