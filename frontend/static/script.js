document.addEventListener("DOMContentLoaded", function () {
  // Add simple hover effect for buttons
  const buttons = document.querySelectorAll("button");
  buttons.forEach(button => {
      button.addEventListener("mouseover", function () {
          button.style.opacity = "0.8";
      });
      button.addEventListener("mouseout", function () {
          button.style.opacity = "1";
      });
  });
});
