/*
const btn = document.querySelector(`#firstlink`);
btn.addEventListener('click', () => {
    alert("No Link Inserted Yet!");
});
const btn2 = document.querySelector(`#secondlink`);
btn2.addEventListener('click', () => {
    alert("No Link Inserted Yet!");
});

const btn3 = document.querySelector(`#thirdlink`);
btn3.addEventListener('click', () => {
    alert("No Link Inserted Yet!");
});
*/
const buttons = document.querySelectorAll('#navibar');
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        alert("Link Not Inserted Yet!");
    });
});