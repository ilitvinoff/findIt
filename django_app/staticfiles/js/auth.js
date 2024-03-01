const passwordTypeIcons = new Map();
passwordTypeIcons.set("text", "eye-slashed.svg")
passwordTypeIcons.set("password", "eye.svg")

function passwordVisibilityListeners() {
    let togglePasswordVisibilityButtons = document.querySelectorAll(".togglePasswordVisibility:not(.click-listen)");
    togglePasswordVisibilityButtons.forEach((el) => {
        el.addEventListener("click", function () {
            let password = document.querySelector(`#${this.dataset.inputId}`);
            // toggle the type attribute
            let type = password.getAttribute("type") === "password" ? "text" : "password";
            password.setAttribute("type", type);
            // toggle the eye icon
            let pathSplit = this.src.split("/")
            pathSplit[pathSplit.length -1] = passwordTypeIcons.get(type)
            this.src = pathSplit.join("/")
        });
        el.classList.add('click-listen');
    });
}

function equalEvery(curValue, index, arr){
    return curValue===arr[0]
}

function passwordMatchingListener() {
    let passwordInputs = document.querySelectorAll('#signup-form .password:not(.change-listen)');

    passwordInputs.forEach((p) => {
        p.addEventListener("input", function(event) {
            let values = Array.from(passwordInputs, (v) => v.value);
            let errorEl = document.querySelector("#prMismatchPasswordError")
            let submitBtn = document.querySelector("#id_submit_signup")

            if (!values.every(equalEvery)) {
                errorEl.classList.add('show');
                submitBtn.setAttribute("disabled","")
            } else {
                errorEl.classList.remove('show');
                submitBtn.removeAttribute("disabled")
            }
        });
        p.classList.add('change-listen');
    });
}

document.body.addEventListener('htmx:load', function (evt) {
    passwordVisibilityListeners();
    passwordMatchingListener();
});

document.addEventListener('DOMContentLoaded', function () {
    passwordVisibilityListeners();
});

