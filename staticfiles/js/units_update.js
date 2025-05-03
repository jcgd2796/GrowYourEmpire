document.addEventListener('DOMContentLoaded', function() {
    var costText = document.getElementById("cost");
    var units = document.getElementById("amount");
    
    if (costText && units) {
        units.addEventListener("change", () => {
            if(units.value > 0){
                costText.textContent = units.value * 2 + " alimento";
            } else {
                costText.textContent = "-";
            }
        });
        costText.textContent = "2 alimento";
    }
});
