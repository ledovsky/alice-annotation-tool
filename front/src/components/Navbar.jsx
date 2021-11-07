import React, { Component } from 'react';
import { Link } from 'react-router-dom';


function NavbarItemMain(props) {
  return (
    <li className="ml-6">
      <Link className="text-indigo-500 hover:text-indigo-600 font-bold" to="/">{props.children}</Link>
    </li>
  )
}
function NavbarItem(props) {
  return (
    <li className={`mr-6 ${props.margin ? 'ml-auto' : ''}`}>
      <Link className="text-gray-700 hover:text-gray-900" to={`${props.to}`} onClick={props.onClick}>{props.children}</Link>
    </li>
  )
}

NavbarItem.defaultProps = {
  color: 'gray',
  bold: false
};

function Navbar(props) {
  return (
    <React.Fragment>
      <div className="py-5 px-2">
        <ul className="flex">
          <NavbarItemMain>ALICE Project</NavbarItemMain>
          <NavbarItem to="/" margin></NavbarItem>
          <NavbarItem to="/datasets">Explore datasets</NavbarItem>
          <NavbarItem to="/docs">Documentation</NavbarItem>
          <NavbarItem to="/downloads">Downloads</NavbarItem>
          { props.loggedIn ?
            <NavbarItem key="logout" href="#" onClick={props.handleLogout}>{props.fullName}: Logout</NavbarItem>
            :
            <NavbarItem key="login" to="/login">Login To Annotation Tool</NavbarItem>
          }
        </ul>
      </div>
      <hr className="mb-5"/>

    </React.Fragment>
  );
}
  
  export default Navbar;