function checkGodBounds(){
    const village = document.getElementById("villageData");

    const storedFood = parseInt(village.dataset.storedFood);
    const storedWood = parseInt(village.dataset.storedWood);
    const storedStone = parseInt(village.dataset.storedStone);
    if (storedFood < 1000 || storedWood < 1000 || storedStone < 1000) {
        M.toast({html: 'No tienes recursos suficientes para construir el templo', classes: 'red'});
        return false;
    }
    return true;
}
