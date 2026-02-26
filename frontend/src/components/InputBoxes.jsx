import "../App.css";

function InputBoxes(props) {
  const heading = props.heading;
  const id = props.id;
  const type = props.type;
  const value = props.value;
  const onChange = props.onChange;

  return (
    <div className="big-box">
      <h2 className={`${heading}-heading`}>{heading}</h2>
      <div className={"box " + id}>
        <h4>
          {type == "input"
            ? `Paste your ${heading} code here...`
            : `Your ${heading} output will be generated here...`}
        </h4>
        <textarea
          className={
            type == "input" ? "raw" : type == "file" ? "file-upload" : "result"
          }
          id={type == "input" ? "input-box" : "result-box"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={`Enter ${heading} code here...`}
        ></textarea>
      </div>
    </div>
  );
}

export default InputBoxes;
