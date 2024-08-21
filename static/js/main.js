$(function() {
    // Create the button element
    
  //Addition Code
    // Check if Cookie Not There
    if (!getCookie("username")) {
      $(".logout").addClass("none");
      $(".login").addClass("active");      
    }
  });
 
  $(document).on('click', '.logout', function(e) {
    deleteCookie("username");
    deleteCookie("session");
    location.reload();
    // location = "/login";
});

  

  //Operations on cookies
  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }
  
  function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }
  


  // Add In Cart 
  let Cart_ccount = document.querySelector(".cart_count");


  const clickedCarts = document.querySelectorAll(".product_cart");


  // Loops in Carts
  clickedCarts.forEach(cart => {
    cart.addEventListener('click', () => {
      const currentValue = parseInt(Cart_ccount.innerHTML, 10); //Conver to Integer
      Cart_ccount.innerHTML = (currentValue + 1).toString(); // Convert to String
    });
  });