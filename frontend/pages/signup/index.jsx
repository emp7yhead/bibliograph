import React from 'react';
import SignupForm from './Signup';
import RegisterPic from './Picture';

export default function Registration() {
  return (
    <>
      <RegisterPic />
      <div className="flex items-center w-full max-w-md px-6 mx-auto lg:w-2/6">
        <div className="flex-1">
          <div className="text-center">
            <h2 className="text-6xl font-bold text-center text-gray-700 dark:text-white">bibliograph</h2>
            <p className="mt-3 text-gray-500 dark:text-gray-300">Sign in to access your account</p>
          </div>
          <div className="mt-8">
            <SignupForm />
          </div>
        </div>
      </div>
    </>
  );
}
