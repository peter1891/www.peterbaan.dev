document.addEventListener("DOMContentLoaded", () => {
  // Used consts
  const formProject = document.getElementById("form-project");

  const previewImageDiv = document.getElementById("preview-images-div");
  const previewImageInput = document.getElementById("preview-images-input");
  const previewImageIcon = document.getElementById("preview-image-icon");
  const previewImageText = document.getElementById("preview-image-text");

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
