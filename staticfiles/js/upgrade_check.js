document.addEventListener('DOMContentLoaded', function() {
    const indexInput = document.getElementById("selectedIndex");
    const costText = document.getElementById("cost");
    const building = document.getElementById("building");

    const village = document.getElementById("villageData");

    function checkBounds() {
        const index = parseInt(indexInput.value);
        if (index === 0) {
            M.toast({ html: 'Selecciona un edificio para mejorar', classes: 'red' });
            return false;
        }
    
        const levels = JSON.parse(village.dataset.levels);
        const resources = JSON.parse(village.dataset.resources);
    
        let insufficient = false;
        switch (index) {
            case 1: insufficient = levels.food * 7 > resources.wood || levels.food * 3 > resources.stone; break;
            case 2: insufficient = levels.wood * 7 > resources.wood || levels.wood * 3 > resources.stone; break;
            case 3: insufficient = levels.stone * 7 > resources.wood || levels.stone * 3 > resources.stone; break;
            case 4: insufficient = levels.wall * 5 > resources.wood || levels.wall * 10 > resources.stone; break;
            case 5: insufficient = levels.storage * 3 > resources.wood || levels.storage * 2 > resources.stone; break;
        }
    
        if (insufficient) {
            M.toast({ html: 'No tienes suficientes recursos para esta mejora', classes: 'red' });
            return false;
        }
    
        return true;
    }

    window.checkBounds = checkBounds;

    building.addEventListener("change", () => {
        const value = building.value;
        let wood = 0, stone = 0;
        const levels = JSON.parse(village.dataset.levels);
        if (value.includes("Granja")) {
            wood = levels.food * 7; stone = levels.food * 3; indexInput.value = 1;
        } else if (value.includes("Aserradero")) {
            wood = levels.wood * 7; stone = levels.wood * 3; indexInput.value = 2;
        } else if (value.includes("Cantera")) {
            wood = levels.stone * 7; stone = levels.stone * 3; indexInput.value = 3;
        } else if (value.includes("Muralla")) {
            wood = levels.wall * 10; stone = levels.wall * 20; indexInput.value = 4;
        } else if (value.includes("Almacenamiento")) {
            wood = levels.storage * 20; stone = levels.storage * 10; indexInput.value = 5;
        }

        if (wood || stone) {
            costText.innerHTML = `
                <div class="cost-item"><i class="material-icons tiny resource-icon">park</i>${wood} madera</div>
                <div class="cost-item"><i class="material-icons tiny resource-icon">landscape</i>${stone} piedra</div>`;
        } else {
            costText.textContent = "-";
        }
    });

    M.FormSelect.init(document.querySelectorAll('select'));
});
