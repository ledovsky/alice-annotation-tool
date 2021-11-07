function CheckboxField( props ) {
  return (
        <div className="flex mt-6">
            <label className="flex items-center">
              <input type="checkbox" className="form-checkbox" name={props.name} onChange={props.onChange} 
               checked={props.checked}/>
                <span className={"ml-2 " + (props.disabled ? 'opacity-50' : '')}>{props.children}</span>
            </label>
        </div>
  )
}

export default CheckboxField;