export default function DropDown(props) {
  let optionList = props.options;

  return (
    <select onChange={(e) => props.onChange(e.target.value)}>
      {optionList.map((option) => {
        return (
          <option
            key={option}
            className="option"
            value={option.toLowerCase()}
            id={option.toLowerCase()}
          >
            {option}
          </option>
        );
      })}
    </select>
  );
}
