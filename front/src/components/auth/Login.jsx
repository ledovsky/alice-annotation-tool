import React from 'react';
import { Link } from 'react-router-dom';
import { AuthInput } from '../../common/AuthInput';


function Login(props) {

  return (
    <div className="flex items-center justify-center mt-40">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div className="mb-4 text-center font-bold text-gray-700">Log in</div>

          <div className="mb-4">
            <AuthInput name="username" label="Username" type="text" placeholder="Username" onChange={ e => props.onChange(e) }/>
          </div>
          <div className="mb-4">
            <AuthInput name="password" label="Password" type="password" placeholder="********" onChange={ e => props.onChange(e) }/>
          </div>

          { props.wrongCredentials ?
            <p className="text-red-500 text-s italic mb-4">Wrong username or password</p> : <p></p>
          }
          <div className="flex items-center justify-between">
            <button className="bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" 
                    onClick={ e => props.onSubmit(e) }>
              Log In
            </button>
            <Link className="inline-block align-baseline font-bold text-sm text-indigo-500 hover:text-indigo-600" to="/forgot-password">
              Forgot Password?
            </Link>
          </div>
        </form>
      </div>

    </div>
  )
}

export { Login };