import { useState } from "react";
import "./App.css";
import InputBoxes from "./components/InputBoxes.jsx";
import Button from "./components/Button.jsx";
import DropDown from "./components/DropDown.jsx";

function App() {
  const [fromLang, setFromLang] = useState("select");
  const [toLang, setToLang] = useState("select");
  const [uploadType, setUploadType] = useState("input-box");
  const [file, setFile] = useState(null);
  function handleFileChange(e) {
    setFile(e.target.files[0]);
  }
  return (
    <>
      <h1>Progress ABL ↔ Python Converter</h1>
      <hr></hr>

      <div className="header-box">
        <div id="from-language" className="header">
          <h2>From Language:</h2>
          <DropDown
            options={["Select", "Progress"]} //Add Python here in future
            onChange={(value) => {
              setFromLang(value);
            }}
          />
        </div>
        <div id="to-language" className="header">
          <h2>To Language:</h2>
          <DropDown
            options={["Select", "Python"]} //Add Progress ABL here in future
            onChange={(value) => {
              setToLang(value);
            }}
          />
        </div>
      </div>
      <div id="choice-box">
        <input
          type="radio"
          name="input"
          id="input-checkbox"
          value="input-box"
          checked={uploadType === "input-box"}
          onChange={(e) => setUploadType(e.target.value)}
        />
        <label for="input-checkbox">Input Code</label>
        <input
          type="radio"
          name="input"
          id="upload-code"
          value="upload-code"
          checked={uploadType === "upload-code"}
          onChange={(e) => setUploadType(e.target.value)}
        />
        <label for="upload-code">Upload Code</label>
      </div>
      <div className="input-output">
        {fromLang !== "select" &&
          (uploadType === "input-box" ? (
            <InputBoxes
              type="input"
              heading={fromLang}
              id={`${fromLang}-input`}
            />
          ) : (
            <div className="big-box">
              <h2 className={`${fromLang}-heading`}>Upload {fromLang} File</h2>
              <div className="box">
                <input
                  id="input-box"
                  type="file"
                  accept=".py,.p,.cls,.w"
                  onChange={handleFileChange}
                />
              </div>
            </div>
          ))}
        {toLang !== "select" &&
        fromLang !== "select" &&
        uploadType === "input-box" ? (
          <div className="button-cont">
            <Button
              class="convert-button"
              label="Translate!"
              func="convert"
              fromLang={fromLang}
              toLang={toLang}
            />
            <Button
              class="download-button hidden"
              label="Download"
              func="download"
            />
            <Button
              class="copy-button hidden"
              label="Copy to Clipboard"
              func="copyToClipboard"
            />
          </div>
        ) : (
          toLang !== "select" &&
          fromLang !== "select" && (
            <div className="button-cont">
              <Button
                class="convert-button"
                label="Translate!"
                func="upload"
                fromLang={fromLang}
                toLang={toLang}
                file={file}
              />
              <Button
                class="download-button hidden"
                label="Download"
                func="download"
              />
              <Button
                class="copy-button hidden"
                label="Copy to Clipboard"
                func="copyToClipboard"
              />
            </div>
          )
        )}
        {toLang !== "select" && (
          <InputBoxes type="output" heading={toLang} id={`${toLang}-input`} />
        )}
      </div>
    </>
  );
}

export default App;
