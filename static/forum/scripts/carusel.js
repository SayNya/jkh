
const carusel = document.querySelector(".news__overflow");
const firstNews = document.querySelector(".news__main_1")
const arrowLeft  = document.querySelector(".button__left");
const arrowRight  = document.querySelector(".button__right");

//так можно добавить стиль элемену через js
carusel.style.cursor = "pointer";

const dragging = (e) => {

    // pageX является свойством объекта события (event) в JavaScript. 
    // Оно представляет горизонтальную координату (относительно левого края страницы) 
    // указателя мыши в момент возникновения события.

    console.log(e.pageX);
    carusel.scrollLeft = e.pageX;
}
carusel.addEventListener("mousemove", dragging);

arrowLeft.addEventListener("click", () => {
    console.log(arrowLeft);
});

arrowRight.addEventListener("click", () => {
    console.log(arrowRight);
});
