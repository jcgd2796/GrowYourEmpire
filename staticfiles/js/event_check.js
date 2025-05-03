function checkEventBounds() {
    const form = document.getElementById("eventForm");

    const foodRequired = parseInt(form.dataset.foodRequired);
    const woodRequired = parseInt(form.dataset.woodRequired);
    const stoneRequired = parseInt(form.dataset.stoneRequired);
    const soldiersRequired = parseInt(form.dataset.soldiersRequired);

    const getValue = (id) => {
        const el = document.getElementById(id);
        return el ? parseInt(el.value) : 0;
    };

    const food = getValue("foodDonated");
    const wood = getValue("woodDonated");
    const stone = getValue("stoneDonated");
    const soldiers = getValue("soldiersDonated");

    if (food > foodRequired) {
        M.toast({html: 'Estás intentando donar más comida de la necesaria', classes: 'red'});
        return false;
    }
    if (wood > woodRequired ) {
        M.toast({html: 'Estás intentando donar más madera de la necesaria', classes: 'red'});
        return false;
    }
    if (stone > stoneRequired) {
        M.toast({html: 'Estás intentando donar más piedra de la necesaria', classes: 'red'});
        return false;
    }
    if (soldiers > soldiersRequired) {
        M.toast({html: 'Estás intentando donar más soldados de los necesarios', classes: 'red'});
        return false;
    }

    return true;
}