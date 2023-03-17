/* Toggle between showing and hiding the side navigation bar */
function toggleNav() {
  var sidenav = document.querySelector(".sidenav");
  var main = document.querySelector(".main");
  if (sidenav.style.width === "200px") {
    sidenav.style.width = "0";
    main.style.marginLeft = "0";
  } else {
    sidenav.style.width = "200px";
    main.style.marginLeft = "200px";
  }
}
