import React from 'react';
import { AuthInput } from '../../common/AuthInput';


function ResetPassword(props) {

  return (
    <div className="flex items-center justify-center mt-40">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">

          <div className="mb-4">
            <AuthInput name="password" label="Password" type="password" placeholder="********" onChange={ e => props.onChange(e) }/>
          </div>
          <div className="mb-4">
            <AuthInput name="password2" label="Repeat password" type="password" placeholder="********" onChange={ e => props.onChange(e) }/>
          </div>

          { props.passwordMismatch ?
            <p className="text-red-500 text-s italic mb-4">Passwords does not match</p> : <p></p>
          }

          <div className="flex items-center justify-between">
            <button className="bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" 
                    onClick={ e => props.onSubmit() }>
              Save
            </button>
          </div>

        </form>
      </div>

    </div>
  )
}

export { ResetPassword };