document.getElementById("uploadBtn").addEventListener("click", async function (e) {
  e.preventDefault(); // 阻止按钮的默认行为

  const form = document.getElementById("uploadForm");
  const formData = new FormData(form);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("网络请求失败");
    }

    const result = await response.json();

    const resultDiv = document.getElementById("result");
    if (result.url) {
      resultDiv.innerHTML = `
        <p>上传成功！文件地址：</p>
        <a href="${result.url}" target="_blank">${result.url}</a>
        <br />
        <img src="${result.url}" alt="上传图片预览" style="max-width: 300px; margin-top: 10px;" />
      `;
    } else {
      resultDiv.textContent = "上传成功，但未返回 URL。";
    }
  } catch (error) {
    console.error("上传失败:", error);
    document.getElementById("result").textContent = "请求失败: " + error.message;
  }
});

console.log("app.js 已加载");
