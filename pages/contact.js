document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    // giving the button an id is easier
    const submitButton = form.querySelector('button[type="submit"]');
    const formMessageDiv = document.getElementById('form-message');

    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    // input validation
    if (!name) {
        formMessageDiv.textContent="Invalid input! Please enter a name.";
        formMessageDiv.style.color="black";
        submitButton.disabled = false;
        submitButton.textContent = "Submit";
        return;
    }
    if (!email.includes('@')) {
        formMessageDiv.textContent='Invalid input! Please enter a valid email address.';
        formMessageDiv.style.color = "black";
        submitButton.disabled = false;
        submitButton.textContent = "Submit";
        return;
    }
    if (!message) {
        formMessageDiv.textContent="Invalid input! Please enter a valid message.";
        formMessageDiv.style.color = "black";
        submitButton.disabled = false;
        submitButton.textContent = "Submit";
        return;
    }

    const data = {name, email, message};
    
    fetch('http://127.0.0.1:5000/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Error message returned');
        }
    })
    .then(response => {
        formMessageDiv.textContent = 'Success!';
        formMessageDiv.style.color = 'pink';
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        formMessageDiv.textContent = 'Oops! A mistake is made. Please try again.'
        formMessageDiv.style.color = 'Black';
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit';
    });
});