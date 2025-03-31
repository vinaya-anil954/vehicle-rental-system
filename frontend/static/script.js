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
    vehicleCards.forEach((card, index) => {
      const imgPlaceholder = card.querySelector(".vehicle-img");
      const colors = ["#4cc9f0", "#4895ef", "#4361ee", "#3f37c9", "#3a0ca3"];
      imgPlaceholder.style.backgroundColor = colors[index % colors.length];
    });
  });