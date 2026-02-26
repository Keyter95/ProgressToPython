export async function convertProgressPrepare(fromLang, toLang) {
  let input = document.getElementById("input-box").value;
  let Output = document.getElementById("result-box");
  let downloadBtn = document.querySelector(".download-button");
  let copyBtn = document.querySelector(".copy-button");
  console.log("bernadette 1--->", copyBtn);
  try {
    const result = await convertProgress(input, fromLang, toLang);
    Output.value = result;
    downloadBtn.classList.remove("hidden");
    copyBtn.classList.remove("hidden");
  } catch (err) {
    console.error(err);
    Output.value = "Conversion failed";
  }
}

export async function convertProgress(inputCode, fromLang, toLang) {
  const response = await fetch("http://127.0.0.1:8000/api/convert", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code: inputCode,
      from: fromLang,
      to: toLang,
    }),
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  const data = await response.json();
  return data.converted_code;
}
export function downloadFile(toLang) {
  if (toLang.toLower() == "python") {
    fileName = "converted_code.py";
  } else {
    fileName = "converted_code.p";
  }
  let convertedCode = document.getElementById("result-box").value;
  /*Create a blob to be downloaded here*/
  const blob = new Blob([convertedCode], { type: "text/plain" });
  //temporary website url for temporary link creation
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;

  document.body.appendChild(link);
  link.click();
  //Clean up here
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

export async function uploadFile(fromLang, toLang, file) {
  if (!file) return;
  const fileContent = await file.text();
  let downloadBtn = document.querySelector(".download-button");
  let copyBtn = document.querySelector(".copy-button");
  let Output = document.getElementById("result-box");
  try {
    const result = await convertProgress(fileContent, fromLang, toLang);
    Output.value = result;
    downloadBtn.classList.remove("hidden");
    copyBtn.classList.remove("hidden");
  } catch (err) {
    console.error(err);
    Output.value = "Conversion failed";
  }
}

export function copyToClipboard() {
  const copyText = document.getElementById("result-box").value;
  navigator.clipboard
    .writeText(copyText)
    .then(() => {
      const copybtn = document.querySelector(".copy-button");
      copybtn.innerText = "Copied!";

      setTimeout(() => {
        copybtn.innerText = "Copy to Clipboard";
      }, 2000);
    })
    .catch((err) => {
      console.error("Failed to copy: ", err);
    });
}
