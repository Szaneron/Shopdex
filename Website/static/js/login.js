const form = document.querySelector("form");
const usernameInput = form.querySelector("[name='username']");
const passwordInput = form.querySelector("[name='password']");

// Listens for the 'submit' event on the form and prevents its default action.
// Calls the 'checkInputs()' function, which validates the entered data.
form.addEventListener('submit', e => {
    e.preventDefault();

    checkInputs();
});


// Function that checks the validity of the form data.
function checkInputs() {
    // trim to remove the whitespaces
    const usernameValue = usernameInput.value.trim();
    const passwordValue = passwordInput.value.trim();

    let isValid = true;

    if (usernameValue === '') {
        setErrorFor(usernameInput, 'Login nie może być pusty');
        isValid = false;
    } else {
        setSuccessFor(usernameInput);
    }

    if (passwordValue === '') {
        setErrorFor(passwordInput, 'Hasło nie może być puste');
        isValid = false;
    } else {
        setSuccessFor(passwordInput);
    }

    if (isValid) {
        form.submit();
    }
}


// Sets an error state for the input field.
function setErrorFor(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = 'form-group error';
    small.innerText = message;
}

// Sets a success state for the input field.
function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-group';
}

const message = document.getElementById('alert-message-content');
const closeBtn = document.getElementById('close-alert');

closeBtn.addEventListener('click', () => {
    message.style.display = 'none';
});