        
function Button (props) {
  return (
    <button className="bg-indigo-500 disabled:opacity-50 hover:bg-indigo-600 text-white 
                       font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity:50" 
      type="button"
      onClick={props.onClick} 
      disabled={props.disabled}
    >
      {props.children}
    </button>
  )
}
        
export default Button;