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
      if (result.original_url) {
      const originalUrlP = document.createElement("p");
      originalUrlP.innerHTML = `原始图片地址：<a href="${result.original_url}" target="_blank">${result.original_url}</a>`;
      resultDiv.appendChild(originalUrlP);
      }
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

console.log("app.js 已加载");
