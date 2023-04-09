
function stepper(btn, inputId) {
    var myInput = document.getElementById(inputId);
    let id = btn.getAttribute("id");
    let min = myInput.getAttribute("min");
    let max = myInput.getAttribute("max");
    let step = myInput.getAttribute("step");
    let val = myInput.getAttribute("value");
    let calStep = (id == "increment") ? (step*1) : (step*-1);
    let newValue = parseInt(val) + calStep;
    
    if(newValue >= min && newValue <= max) {
        myInput.setAttribute("value", newValue)
    }
}

