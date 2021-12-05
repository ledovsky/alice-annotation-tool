function CheckboxField( props ) {
  return (
        <div className="flex mt-6 custom-tooltip">
            <label className="flex items-center">
              <input type="checkbox" className="form-checkbox" name={props.name} onChange={props.onChange} 
               checked={props.checked}/>
              <span className={"ml-2 " + (props.disabled ? 'opacity-50' : '')}>{props.children}</span>
            </label>
            { props.tooltip ? 
                <div className="custom-tooltip-text text-sm max-w-2xl p-2 bg-gray-900 text-white rounded">{props.tooltip}</div>
              : null 
            }
            
        </div>
  )
}

export default CheckboxField;