let starForm = document.querySelector("star-form");

const storeKey = () => {
    const keyField = document.getElementById("key");

    if (localStorage.getItem("auth_key") == null) {
        localStorage.setItem("auth_key", keyField.value);
    }
}

const forgetKey = () => {
    localStorage.removeItem("auth_key");
}

const loadKey = () => {
    const storedKey = localStorage.getItem("auth_key");
    const keyField = document.getElementById("key");

    if (storedKey != null) {
        keyField.value = storedKey;

        let forgetButton = document.createElement("a");
        
        forgetButton.className = "nav-item";
        forgetButton.innerText = "Forget Key";
        forgetButton.attributes["role"] = "button";
        forgetButton.href = "#";

        forgetButton.addEventListener("click", event => {
            event.preventDefault();
            forgetKey();
            forgetButton.remove();
        });

        document.querySelector("nav > .alt").appendChild(forgetButton);
    }
}

loadKey();

starForm.addEventListener("submit", event => {
    storeKey();
});
