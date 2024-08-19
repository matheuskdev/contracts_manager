document.addEventListener("DOMContentLoaded", function() {
    // Obtém a URL atual
    var currentPath = window.location.pathname;
    
    // Obtém todos os links do menu
    var menuLinks = document.querySelectorAll("#menu a.nav-link");

    // Itera sobre os links para encontrar o correspondente à URL atual
    menuLinks.forEach(function(link) {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
      }
    });
  });
