document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    
    const menuLinks = document.querySelectorAll("#menu a.nav-link");

    menuLinks.forEach(function(link) {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
      }
    });
  });
