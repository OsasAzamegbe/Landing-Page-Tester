const switchMode = document.querySelector(".switch");
const mainPage = document.querySelector(".main");

switchMode.addEventListener("click", function (e) {
    e.preventDefault();

    if (mainPage.classList.contains("light")) {
        mainPage.classList.remove("light");
        this.classList.remove("off");
    } else {
        mainPage.classList.add("light");
        this.classList.add("off");
    }
});
