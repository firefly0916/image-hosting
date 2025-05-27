document.getElementById("uploadBtn").addEventListener("click", async function (e) {
  e.preventDefault(); // 阻止按钮的默认行为

  const form = document.getElementById("uploadForm");
  const formData = new FormData(form);
  const resultDiv = document.getElementById("result");

  // 清除之前的结果
  resultDiv.innerHTML = "";

  // 显示加载指示器
  const loadingIndicator = document.createElement("p");
  loadingIndicator.textContent = "上传中...";
  resultDiv.appendChild(loadingIndicator);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("网络请求失败");
    }

    const result = await response.json();

    if (result.url) {
      resultDiv.innerHTML = `<p>上传成功！ <a href="${result.url}" target="_blank">查看图片</a></p>`;
      // 展示原始 URL
      
      const originalUrlP = document.createElement("p");
      originalUrlP.innerHTML = `原始图片地址：<a href="${result.url}" target="_blank">${result.url}</a>`;
      resultDiv.appendChild(originalUrlP);
      
      const imgPreview = document.createElement("img");
      imgPreview.src = result.url;
      imgPreview.alt = "上传图片预览";
      imgPreview.className = "preview";
      resultDiv.appendChild(imgPreview);
    } else {
      resultDiv.textContent = "上传失败。请再试一次。";
    }
  } catch (error) {
    resultDiv.textContent = `错误: ${error.message}`;
  } finally {
    loadingIndicator.remove();
  }
});

async function fetchFiles() {
  try {
    const response = await fetch("http://127.0.0.1:8000/files");
    if (!response.ok) {
      throw new Error("Failed to fetch files");
    }
    const files = await response.json();
    const tableBody = document.querySelector("#filesTable tbody");
    tableBody.innerHTML = ""; // Clear existing rows

    files.forEach(file => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${file[0]}</td>
        <td>${file[1]}</td>
        <td><a href="${file[2]}" target="_blank">${file[2]}</a></td>
        <td>${file[3]}</td>
        <td>${file[4]}</td>
        <td>${file[5]}</td>
        <td>${file[6]}</td>
        <td>${file[7]}</td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching files:", error);
  }
}

// Fetch files on page load
document.addEventListener("DOMContentLoaded", fetchFiles);

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");

  if (e.dataTransfer.files.length) {
    fileInput.files = e.dataTransfer.files;
  }
});

console.log("app.js 已加载");
