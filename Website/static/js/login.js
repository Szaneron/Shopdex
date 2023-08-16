const form = document.querySelector("form");
const usernameInput = form.querySelector("[name='username']");
const passwordInput = form.querySelector("[name='password']");


form.addEventListener('submit', e => {
    e.preventDefault();

    checkInputs();
});

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

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = 'form-group error';
    small.innerText = message;
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-group';
}

const message = document.getElementById('alert-message-content');
const closeBtn = document.getElementById('close-alert');

closeBtn.addEventListener('click', () => {
    message.style.display = 'none';
});