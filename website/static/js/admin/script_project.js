document.addEventListener("DOMContentLoaded", () => {
  // Used consts
  const formProject = document.getElementById("form-project");

  const previewImageDiv = document.getElementById("preview-images-div");
  const previewImageInput = document.getElementById("preview-images-input");
  const previewImageIcon = document.getElementById("preview-image-icon");
  const previewImageText = document.getElementById("preview-image-text");

  const previewImagesDiv = document.querySelectorAll(
    ".admin-project-preview-div"
  );

  let previewImageWrapper;
  let previewImageAdd;

  if (document.getElementById("preview-images-wrapper")) {
    previewImageWrapper = document.getElementById("preview-images-wrapper");
    previewImageAdd = document.getElementById("preview-image-add");
  } else {
    previewImageWrapper = document.createElement("div");
    previewImageWrapper.classList.add("admin-project-preview-wrapper");
    previewImageWrapper.id = "preview-images-wrapper";

    previewImageAdd = document.createElement("div");
    previewImageAdd.classList.add("admin-project-preview-add");
  }

  // Open Preview Image Input selection
  previewImageDiv.addEventListener("click", function () {
    previewImageInput.click();
  });

  // Display selecten Preview Images
  previewImageInput.onchange = function () {
    let previewImages = previewImageInput.files;

    if (document.getElementById("preview-image-text")) {
      previewImageText.remove();
    }

    for (const previewImg of previewImages) {
      // Create the div
      newPreviewImageDiv = document.createElement("div");
      newPreviewImageDiv.classList.add("admin-project-preview-div");

      // Create the remove button
      newPreviewImageRemove = document.createElement("div");
      newPreviewImageRemove.classList.add("admin-project-preview-remove");

      newPreviewImageRemoveBtn = document.createElement("a");
      newPreviewImageRemoveBtn.classList.add("admin-project-preview-btn");

      newPreviewImageRemoveIcon = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg"
      );
      newPreviewImageRemoveIcon.setAttribute(
        "xmlns",
        "http://www.w3.org/2000/svg"
      );
      newPreviewImageRemoveIcon.classList.add(
        "admin-project-preview-remove-icon"
      );
      newPreviewImageRemoveIcon.setAttribute("viewBox", "0 0 256 256");

      newPreviewImageRemoveIconPath = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "path"
      );
      newPreviewImageRemoveIconPath.setAttribute(
        "d",
        "M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"
      );

      newPreviewImageRemoveIcon.appendChild(newPreviewImageRemoveIconPath);
      newPreviewImageRemoveBtn.appendChild(newPreviewImageRemoveIcon);
      newPreviewImageRemove.appendChild(newPreviewImageRemoveBtn);

      // Create the hidden input
      newPreviewImageInput = document.createElement("input");
      newPreviewImageInput.id = "image_id";
      newPreviewImageInput.name = "image_id";
      newPreviewImageInput.type = "hidden";

      // Create the img
      newPreviewImageImg = document.createElement("img");
      newPreviewImageImg.classList.add("admin-project-preview-img");
      newPreviewImageImg.src = URL.createObjectURL(previewImg);
      newPreviewImageImg.alt = previewImg.name;

      // Combine the elements
      newPreviewImageDiv.appendChild(newPreviewImageRemove);
      newPreviewImageDiv.appendChild(newPreviewImageInput);
      newPreviewImageDiv.appendChild(newPreviewImageImg);

      previewImageAdd.appendChild(previewImageIcon);

      previewImageWrapper.appendChild(newPreviewImageDiv);
    }

    previewImageWrapper.appendChild(previewImageAdd);
    previewImageDiv.appendChild(previewImageWrapper);
  };

  // Remove Preview Image from selection
  previewImagesDiv.forEach(function (container) {
    container.addEventListener("click", function (event) {
      event.stopPropagation();
      container.remove();
      console.log("Preview image removed");
    });
  });

  // Submit Preview Images
  formProject.addEventListener("submit", async function (event) {
    event.preventDefault();

    const projectFormData = new FormData(this);

    for (const div of previewImageWrapper.querySelectorAll(
      "div.admin-project-preview-div"
    )) {
      const img = div.querySelector("img");
      const response = await fetch(img.src);
      const blob = await response.blob();

      const id = div.querySelector("input").value;

      if (id) {
        projectFormData.append(`current_preview_images`, id);
      } else {
        projectFormData.append(`new_preview_images`, blob, img.alt);
      }
    }

    fetch(event.target.action, {
      method: "POST",
      body: projectFormData,
    })
      .then((response) => response.json())
      .then((data) => {
        window.location.href = data.redirect;
      });
  });
});
