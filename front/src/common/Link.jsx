import { Link } from 'react-router-dom';


function CustomLink (props) {
  return <Link className="text-indigo-500 hover:text-indigo-600" to={props.href}>  { props.children } </Link>
}

export default CustomLink;