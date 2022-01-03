import React from 'react';
import { AuthInput } from '../../common/AuthInput';


function ForgotPassword(props) {

  return (
    <div className="flex items-center justify-center mt-40">
      <div className="w-full max-w-xs">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div className="mb-4 text-center font-bold text-gray-700">Password recovery</div>
          <div className="mb-4">
            <AuthInput name="email" label="Email" type="text" placeholder="your@email.com" onChange={ e => props.onChange(e) }/>
          </div>
          <div className="flex items-center justify-between">
            <button className="bg-indigo-500 hover:bg-indigo-600 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" 
                    onClick={ e => props.onSubmit() }>
              Send a reset link
            </button>
          </div>
        </form>
      </div>

    </div>
  )
}

export { ForgotPassword };