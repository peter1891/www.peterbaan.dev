document.addEventListener("DOMContentLoaded", () => {
  // ------------------
  // Animation navigation buttons
  // ------------------

  const navLinks = document.querySelectorAll(".nav-link");

  // Adding a permanent 100% width to the ::after by clicking
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.forEach((link) => link.classList.remove("active"));
      link.classList.add("active");
    });
  });

  const navLinkAbout = document.getElementById("nav-link-about");
  const navLinkProjects = document.getElementById("nav-link-projects");
  const navLinkContact = document.getElementById("nav-link-contact");
  const viewHeight = window.innerHeight;

  // Adding a permanent 100% width to the ::after based on location on the page
  window.addEventListener("scroll", () => {
    if (window.scrollY < viewHeight / 2) {
      navLinks.forEach((link) => link.classList.remove("active"));
    } else if (window.scrollY < viewHeight * 1.5) {
      navLinks.forEach((link) => link.classList.remove("active"));
      navLinkAbout.classList.add("active");
    } else if (window.scrollY < viewHeight * 2.5) {
      navLinks.forEach((link) => link.classList.remove("active"));
      navLinkProjects.classList.add("active");
    } else {
      navLinks.forEach((link) => link.classList.remove("active"));
      navLinkContact.classList.add("active");
    }
  });

  // ------------------
  // On screen animation about bulletpoints
  // ------------------

  const aboutList = document.getElementById("about-list");
  const aboutListObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("onscreen");
        aboutListObserver.unobserve(entry.target);
      }
    });
  });

  aboutListObserver.observe(aboutList);

  // ------------------
  // Open close projects dialog
  // ------------------

  const projectModal = document.getElementById("project-modal");

  // Open the dialog element
  const openProjectModal = document.querySelectorAll(".project-btn-open");
  openProjectModal.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      projectModal.showModal();

      // Get the image width when opening the dialog element
      const imageWidth = images[0].getBoundingClientRect().width;
      SetImagePosition(imageWidth);
    });
  });

  // Close the dialog element
  const closeProjectModal = document.querySelector(".project-btn-close");
  closeProjectModal.addEventListener("click", function (event) {
    event.preventDefault();
    projectModal.close();

    // Reset to first image in slider
    const currentImage = imageSlider.querySelector(".image-slider-current");
    const firstImage = images[0];
    const currentNavBtn = imageSliderNav.querySelector(".image-slider-current");
    const firstNavBtn = imageSliderNav.querySelector("button");
    const firstIndex = 0;
    MoveToImage(imageSlider, currentImage, firstImage);
    UpdateNavBtn(currentNavBtn, firstNavBtn);
    HideBtn(images, prevBtn, nextBtn, firstIndex);
  });

  // For closing the dialog by clicking outside the element
  projectModal.addEventListener("click", (e) => {
    const projectModalDimensions = projectModal.getBoundingClientRect();
    if (
      e.clientX < projectModalDimensions.left ||
      e.clientX > projectModalDimensions.right ||
      e.clientY < projectModalDimensions.top ||
      e.clientY > projectModalDimensions.bottom
    ) {
      projectModal.close();
    }
  });

  // ------------------
  // IMAGE SLIDER
  // ------------------

  const imageSlider = document.querySelector(".image-slider-list");
  const images = Array.from(imageSlider.children);
  const nextBtn = document.querySelector(".image-slider-btn-right");
  const prevBtn = document.querySelector(".image-slider-btn-left");
  const imageSliderNav = document.querySelector(".image-slider-nav");
  const navBtns = Array.from(imageSliderNav.children);

  // Set image positions in slider
  const SetImagePosition = (imageWidth) => {
    for (let i = 0; i < images.length; i++) {
      images[i].style.left = i * imageWidth + "px";
    }
  };

  // Move to image position in slide
  const MoveToImage = (imageSlider, currentImage, targetImage) => {
    imageSlider.style.transform = "translateX(-" + targetImage.style.left + ")";
    currentImage.classList.remove("image-slider-current");
    targetImage.classList.add("image-slider-current");
  };

  // Change the navigation btn
  const UpdateNavBtn = (currentBtn, targetBtn) => {
    currentBtn.classList.remove("image-slider-current");
    targetBtn.classList.add("image-slider-current");
  };

  // Hide nav buttons
  const HideBtn = (images, prevBtn, nextBtn, targetIndex) => {
    if (targetIndex === 0) {
      prevBtn.classList.add("image-slider-btn-hidden");
      nextBtn.classList.remove("image-slider-btn-hidden");
    } else if (targetIndex === images.length - 1) {
      prevBtn.classList.remove("image-slider-btn-hidden");
      nextBtn.classList.add("image-slider-btn-hidden");
    } else {
      prevBtn.classList.remove("image-slider-btn-hidden");
      nextBtn.classList.remove("image-slider-btn-hidden");
    }
  };

  // Left button for chaning slide
  prevBtn.addEventListener("click", (e) => {
    const currentImage = imageSlider.querySelector(".image-slider-current");
    const prevImage = currentImage.previousElementSibling;
    const currentNavBtn = imageSliderNav.querySelector(".image-slider-current");
    const prevNavBtn = currentNavBtn.previousElementSibling;
    const prevIndex = images.findIndex((image) => image === prevImage);

    MoveToImage(imageSlider, currentImage, prevImage);
    UpdateNavBtn(currentNavBtn, prevNavBtn);
    HideBtn(images, prevBtn, nextBtn, prevIndex);
  });

  // Right button for changing slide
  nextBtn.addEventListener("click", (e) => {
    const currentImage = imageSlider.querySelector(".image-slider-current");
    const nextImage = currentImage.nextElementSibling;
    const currentNavBtn = imageSliderNav.querySelector(".image-slider-current");
    const nextNavBtn = currentNavBtn.nextElementSibling;
    const nextIndex = images.findIndex((image) => image === nextImage);

    MoveToImage(imageSlider, currentImage, nextImage);
    UpdateNavBtn(currentNavBtn, nextNavBtn);
    HideBtn(images, prevBtn, nextBtn, nextIndex);
  });

  // Navigation indicators at the bottom
  imageSliderNav.addEventListener("click", (e) => {
    const targetNavBtn = e.target.closest("button");

    if (!targetNavBtn) return;

    const currentImage = imageSlider.querySelector(".image-slider-current");
    const currentNavBtn = imageSliderNav.querySelector(".image-slider-current");
    const targetNavIndex = navBtns.findIndex((btn) => btn === targetNavBtn);
    const targetImage = images[targetNavIndex];

    MoveToImage(imageSlider, currentImage, targetImage);
    UpdateNavBtn(currentNavBtn, targetNavBtn);
    HideBtn(images, prevBtn, nextBtn, targetNavIndex);
  });
});
