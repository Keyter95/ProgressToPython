import "../App.css";
import {
  convertProgressPrepare,
  downloadFile,
  uploadFile,
  copyToClipboard,
} from "../javascript/functions.js";

function Button(props) {
  let classN = props.class;
  let label = props.label;
  return (
    <div
      className={classN}
      onClick={() => {
        {
          props.func == "convert"
            ? convertProgressPrepare(props.fromLang, props.toLang)
            : props.func == "download"
              ? downloadFile(props.toLang)
              : props.func == "copyToClipboard"
                ? copyToClipboard()
                : uploadFile(props.fromLang, props.toLang, props.file);
        }
      }}
    >
      {label}
    </div>
  );
}

export default Button;
