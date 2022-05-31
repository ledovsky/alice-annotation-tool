export function DocsTitle (props) {
  return (
    <p className="text-4xl mb-6"> { props.children } </p>
  )
}

export function DocsHeader (props) {
  return (
    <p className="mt-6 font-bold"> { props.children } </p>
  )
}

export function DocsParagraph (props) {
  return (
        <p className="mt-3"> { props.children } </p>
  )
}