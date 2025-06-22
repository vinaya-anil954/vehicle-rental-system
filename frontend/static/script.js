document.addEventListener("DOMContentLoaded", function() {
  // Enhanced button interactions
  const buttons = document.querySelectorAll(".btn");
  buttons.forEach(button => {
    button.addEventListener("mouseenter", function() {
      this.style.transform = "translateY(-2px)";
    });
    button.addEventListener("mouseleave", function() {
      this.style.transform = "translateY(0)";
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach(form => {
    form.addEventListener("submit", function(e) {
      const submitBtn = this.querySelector("[type='submit']");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
      }
      
      // Add your form validation logic here
      // Example: check required fields
      const requiredFields = this.querySelectorAll("[required]");
      let isValid = true;
      
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = "var(--danger-color)";
        }
      });
      
      if (!isValid) {
        e.preventDefault();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Submit";
        }
      }
    });
  });

  // Confirmation for destructive actions
  const destructiveLinks = document.querySelectorAll("a[href*='delete'], a[href*='cancel']");
  destructiveLinks.forEach(link => {
    link.addEventListener("click", function(e) {
      if (!confirm("Are you sure you want to perform this action?")) {
        e.preventDefault();
      }
    });
  });

  // Simulate vehicle images (can be replaced with real images from backend)
  const vehicleCards = document.querySelectorAll(".vehicle-card");
  const imageUrls = [
    "url('/static/CarImages/1.jpeg')",
    "url('/static/CarImages/2.jpeg')",
    "url('/static/CarImages/3.jpeg')",
    "url('/static/CarImages/4.jpeg')",
    "url('/static/CarImages/5.jpeg')",
    "url('/static/CarImages/6.jpeg')",
    "url('/static/CarImages/7.jpeg')",
    "url('/static/CarImages/8.jpeg')",
    "url('/static/CarImages/9.jpeg')",
    "url('/static/CarImages/10.jpeg')",
    "url('/static/CarImages/11.jpeg')",
    "url('/static/CarImages/12.jpeg')",
    "url('/static/CarImages/13.jpeg')",
    "url('/static/CarImages/14.jpeg')",
    "url('/static/CarImages/15.jpeg')",
    "url('/static/CarImages/16.jpeg')"
  ];
  
  vehicleCards.forEach((card, index) => {
    const imgPlaceholder = card.querySelector(".vehicle-img");
    imgPlaceholder.style.backgroundImage = imageUrls[index % imageUrls.length];
    imgPlaceholder.style.backgroundSize = "cover";
    imgPlaceholder.style.backgroundPosition = "center";
  });
  
});