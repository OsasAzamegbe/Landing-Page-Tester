const switchMode = document.querySelector(".switch");
const mainPage = document.querySelector(".main");
const footer = document.querySelector("footer");

switchMode.addEventListener("click", function (e) {
    e.preventDefault();

    if (mainPage.classList.contains("light")) {
        mainPage.classList.remove("light");
        this.classList.remove("off");
        footer.classList.remove("light")
    } else {
        mainPage.classList.add("light");
        this.classList.add("off");
        footer.classList.add("light")
    }
});
