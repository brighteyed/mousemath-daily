const main = {
    run: () => {
        window.addEventListener('load', async () => {
            const item = document.querySelector('.item');
            const response = await fetch(`/attachments/${item.dataset.itemid}`);
            const text = await response.text();
            item.insertAdjacentHTML('beforeend', text);
        });
    }
};

main.run();