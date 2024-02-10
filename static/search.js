

fetch('/animal-types')
    .then((response) => response.json())
    .then((responseData) => {

        const animalSelectElement = document.querySelector('#species-select'); // species select
        animalSelectElement.addEventListener('change', (evt) => {
        evt.preventDefault();

        document.querySelector('#animalGenderOptions').innerHTML = ""
        document.querySelector('#animalCoatContainer').innerHTML = ""
        document.querySelector('#animalColorOptions').innerHTML = ""


        for (const animalType of responseData.types){
                if (animalType.name === animalSelectElement.value){
                    for (const color of animalType.colors) {
                    document.querySelector('#animalColorOptions').insertAdjacentHTML('beforeend', `<option value="${color}">`);
                    } 
                    for (const gender of animalType.genders) {
                        document.querySelector('#animalGenderOptions').insertAdjacentHTML('beforeend', `<option value="${gender}">`);
                    }
                    if (animalType.coats.length > 0) {
                            document.querySelector('#animalCoatContainer').insertAdjacentHTML('beforeend', `
                            <label for="animalCoatList" class="form-label">Coat type:</label>
                            <input class="form-control" name="animal-coat" list="animalCoatOptions" id="animalCoatList" placeholder="Type or Click to view options">
                            <datalist id="animalCoatOptions">
                            </datalist>
                            `);
                            for (const coat of animalType.coats) {
                            document.querySelector('#animalCoatOptions').insertAdjacentHTML('beforeend', `<option value="${coat}">`);
                            }
                    }
                }
        }  
        })
    })


