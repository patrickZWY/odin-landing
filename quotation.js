var quotations = [
    {quote: `"This is another quotation by some famous person."`, author: "Random Dude"},
    {quote: `"This is the third quotation by someone."`, author: "The Third One"},
    {quote: `"Some Quotation Here"`, author: "Author"}
];

var current = 0;

function changeQuotation() {
    var quotationElement = document.getElementById('quotation');
    current = (current + 1) % quotations.length;
    quotationElement.innerHTML = '<h3>' + quotations[current].quote + '</h3><h3>' + quotations[current].author + '</h3>';

    quotationElement.classList.add('opening');

    setTimeout(() => {
        quotationElement.classList.remove('opening');
    }, 2000);
}

document.getElementById('quotation').addEventListener('click', changeQuotation);