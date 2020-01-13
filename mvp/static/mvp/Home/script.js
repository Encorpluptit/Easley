var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    $("#toHide").css("top", "15px");
    $("#header").css("top", "0px");
  } else {
    $("#toHide").css("top", "-65px");
    $("#header").css("top", "-80px");

  }
  prevScrollpos = currentScrollPos;
}
