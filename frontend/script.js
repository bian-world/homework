document.getElementById("file").addEventListener("change", function() {
  var fileName = this.files[0].name;
  document.getElementById("file-name").textContent = fileName;
  document.getElementById("upload-btn").textContent = "重新上传";
});

document.getElementById("translate-btn").addEventListener("click", function() {
  var file = document.getElementById("file").files[0];
  var fileFormat = document.getElementById("file-format").value;
  var targetLanguage = document.getElementById("target-language").value;

  var formData = new FormData();
  formData.append("file", file);
  formData.append("file_format", fileFormat);
  formData.append("target_language", targetLanguage);

  showLoadingSpinner();

  fetch(apiConfig., {
    method: "POST",
    body: formData
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    hideLoadingSpinner();
    displayTranslationResult(data);
  })
  .catch(function(error) {
    hideLoadingSpinner();
    alert("翻译请求失败：" + error.message);
  });
});

function showLoadingSpinner() {
  document.getElementById("loading-spinner").style.visibility = "visible";
}

function hideLoadingSpinner() {
  document.getElementById("loading-spinner").style.visibility = "hidden";
}

function displayTranslationResult(result) {
  var resultList = document.getElementById("result-list");
  resultList.innerHTML = "";

  var originalFileName = result.originalFileName;
  var translatedFileName = result.translatedFileName;
  var fileFormat = result.fileFormat;
  var targetLanguage = result.targetLanguage;
  var downloadUrl = result.downloadUrl;

  var fileItem = document.createElement("li");
  fileItem.textContent = "原文件名： " + originalFileName;
  resultList.appendChild(fileItem);

  fileItem = document.createElement("li");
  fileItem.textContent = "结果文件名： " + translatedFileName;
  resultList.appendChild(fileItem);

  fileItem = document.createElement("li");
  fileItem.textContent = "目标文件格式： " + fileFormat;
  resultList.appendChild(fileItem);

  fileItem = document.createElement("li");
  fileItem.textContent = "目标语言： " + targetLanguage;
  resultList.appendChild(fileItem);

  fileItem = document.createElement("li");
  var downloadLink = document.createElement("a");
  downloadLink.href = downloadUrl;
  downloadLink.textContent = "下载结果文件";
  fileItem.appendChild(downloadLink);
  resultList.appendChild(fileItem);

  document.getElementById("result-section").classList.remove("hidden");
}