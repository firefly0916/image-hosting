// ====== Config custom_url ======
const custom_url = "http://127.0.0.1:8000";

document.getElementById("uploadBtn").addEventListener("click", async function (e) {
  e.preventDefault(); // Prevent default button behavior

  const form = document.getElementById("uploadForm");
  const formData = new FormData(form);
  const resultDiv = document.getElementById("result");

  // Clear previous results
  resultDiv.innerHTML = "";

  // Show loading indicator
  const loadingIndicator = document.createElement("p");
  loadingIndicator.textContent = "Uploading ...";
  resultDiv.appendChild(loadingIndicator);

  try {
    const response = await fetch(`${custom_url}/upload`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Network request failed");
    }

    const result = await response.json();

    if (result.url) {
      resultDiv.innerHTML = `<p>Upload successful! <a href="${result.url}" target="_blank">View Image</a></p>`;
      // Show original URL

      const originalUrlP = document.createElement("p");
      originalUrlP.innerHTML = `Original image URL: <a href="${result.url}" target="_blank">${result.url}</a>`;
      resultDiv.appendChild(originalUrlP);
      
      const imgPreview = document.createElement("img");
      imgPreview.src = result.url;
      imgPreview.alt = "Uploaded image preview";
      imgPreview.className = "preview";
      resultDiv.appendChild(imgPreview);
    } else {
      resultDiv.textContent = "Upload failed. Please try again.";
    }
  } catch (error) {
    resultDiv.textContent = `Error: ${error.message}`;
  } finally {
    loadingIndicator.remove();
  }
});

async function fetchFiles() {
  try {
    const response = await fetch(`${custom_url}/files`);
    if (!response.ok) {
      throw new Error("Failed to fetch files");
    }
    const files = await response.json();
    const tableBody = document.querySelector("#filesTable tbody");
    tableBody.innerHTML = ""; // Clear existing rows

    files.forEach(file => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${file.id}</td>
        <td>${file.filename}</td>
        <td><img src="${file.custom_url}" alt="preview" class="table-preview-img preview-clickable" data-full="${file.custom_url}"></td>
        <td>${file.year}</td>
        <td>${file.month}</td>
        <td>${file.day}</td>
        <td>${file.uuid}</td>
        <td>${file.custom_url}</td>
        <td>${file.upload_time}</td>
        <td><button class="delete-btn" data-id="${file.id}">Delete</button></td>
      `;
      tableBody.appendChild(row);
    });
    // Bind image click event to show full image in overlay
    document.querySelectorAll('.preview-clickable').forEach(img => {
      img.addEventListener('click', function() {
        const overlay = document.createElement('div');
        overlay.className = 'img-overlay';
        overlay.innerHTML = `<div class='img-overlay-bg'></div><img src='${this.dataset.full}' class='img-overlay-img'><span class='img-overlay-close'>&times;</span>`;
        document.body.appendChild(overlay);
        overlay.querySelector('.img-overlay-close').onclick = () => overlay.remove();
        overlay.querySelector('.img-overlay-bg').onclick = () => overlay.remove();
      });
    });
    // Bind delete event
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', async function() {
        const id = this.getAttribute('data-id');
        if (confirm('Are you sure you want to delete this file?')) {
          const res = await fetch(`${custom_url}/files/${id}`, { method: 'DELETE' });
          if (res.ok) fetchFiles();
          else alert('Delete failed');
        }
      });
    });
  } catch (error) {
    console.error("Error fetching files:", error);
  }
}

// Fetch files on page load
document.addEventListener("DOMContentLoaded", fetchFiles);

// File selection custom logic
const fileInput = document.getElementById("fileInput");
const fileSelectBox = document.getElementById("fileSelectBox");
const fileSelectBtn = document.getElementById("fileSelectBtn");
const uploadBtn = document.getElementById("uploadBtn");

fileSelectBtn.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  if (fileInput.files && fileInput.files.length > 0) {
    fileSelectBox.textContent = fileInput.files[0].name;
    fileSelectBox.classList.remove("file-unselected");
    fileSelectBox.classList.add("file-selected");
    uploadBtn.classList.add("active");
  } else {
    fileSelectBox.textContent = "No file selected";
    fileSelectBox.classList.remove("file-selected");
    fileSelectBox.classList.add("file-unselected");
    uploadBtn.classList.remove("active");
  }
});

// Dragging over dropZone should also sync fileSelectBox
const dropZone = document.getElementById("dropZone");
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = "copy";
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    fileInput.files = e.dataTransfer.files;
    // Trigger change event to update UI
    const event = new Event('change', { bubbles: true });
    fileInput.dispatchEvent(event);
  }
});

console.log("app.js loaded");
