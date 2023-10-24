import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import config from '../../config';
import BibliographClient from '../../src/client';
import FormInput from '../../components/FormInput/FormInput';
import FormButton from '../../components/Button/FormButton';
import {  } from '@nextui-org/react';
import ErrorMessage from '../../components/Alert';

const client = new BibliographClient(config);

function SignupForm() {
  const [error, setError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [registerForm, setRegisterForm] = useState({ username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onRegister = (e) => {
    // e.preventDefault();
    setLoading(true);
    setError(false);

    client.register(registerForm.username, registerForm.email, registerForm.password)
      .then(() => { navigate('/profile'); })
      .catch((err) => {
        setLoading(false);
        setError(true);
        setErrorMessage(err.message);
      });
  };

  return (
    <form>
      {error && <ErrorMessage message={errorMessage} />}
      <div>
        <FormInput
          isRequired
          key="username"
          type="text"
          label="Username"
          placeholder="Enter your username"
          onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })}
        />
        <div className="mt-6">
          <FormInput
            isRequired
            key="email"
            type="email"
            label="Email"
            placeholder="Enter your email"
            onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
          />
        </div>
        <div className="mt-6">
          <FormInput
            isRequired
            key="password"
            type="password"
            label="Password"
            placeholder="Enter your password"
            onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
          />
        </div>
        <div className="mt-6">
          <FormButton
            onPress={(e) => onRegister(e)}
            color="primary"
            isLoading={loading}
            text="Create Account"
          />
        </div>
      </div>
    </form>
  );
}

export default SignupForm;
