function ExternalLink (props) {
  return <a className="text-indigo-500 hover:text-indigo-600 font-bold" href={props.href}>  { props.children } </a>
}

export default ExternalLink;