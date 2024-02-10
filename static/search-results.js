
const ratingButtons = document.querySelectorAll('.user-rating');
for (const button of ratingButtons ) {
    button.addEventListener('click', (evt) => {
        const buttontext = evt.target.innerText

        const buttonFetchBodyJson = {
        button_value : buttontext,
        animal_id : evt.target.id
        }

        fetch('/store-user-rating', {
            method: 'POST',
            body: JSON.stringify(buttonFetchBodyJson),
            headers: {
                'Content-Type': 'application/json',
            },
            })
            .then((response) => response.json())

    });
};

