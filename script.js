const h = document.querySelector('h1');
const body = document.querySelector('body');
const input = document.querySelector('#number');
const removeBody = document.querySelector('#removeBody');
const errorElement = document.createElement('h6');
let totalTask;

h.onclick = event => {
    let num = Math.floor(Math.random() * 360);
    h.style.backgroundColor = `hsl(${num}, 50%, 50%)`;
};



function fetchEvent() {
    fetch('/getTask').then(res => res.text()).then(data => {
        totalTask = parseInt(data);
        errorElement.innerText = `Task number must in between 1 - ${totalTask}`;
    });
}

function clickSubmit() {
    let intValue = parseInt(input.value)
    if (intValue < 1 || intValue > totalTask || input.value === '') {
        document.querySelector('.form-field.remove').insertAdjacentElement('afterend', errorElement);
        return false;
    } else {
        errorElement.remove();
        return true;
    }
}

function validate() {
    let len = document.getElementById('title').value.length
    if (len > 100) {
        console.log("Too long")
        return false
    }
    return true
}

function removeInput() {}