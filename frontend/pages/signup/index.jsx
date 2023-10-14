import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input } from '@nextui-org/react';
import config from '../../config';
import BibliographClient from '../../src/client';

const client = new BibliographClient(config);

function Registration() {
  const [error, setError] = useState(false);
  const [registerForm, setRegisterForm] = useState({ username: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onRegister = (e) => {
    // e.preventDefault();
    setLoading(true);
    setError(false);

    client.register(registerForm.username, registerForm.email, registerForm.password)
      .then(() => {
        navigate('login');
      })
      .catch((err) => {
        setLoading(false);
        setError(true);
        alert(err);
      });
  };

  return (
    <form className="flex flex-col gap-4">
      <div className="flex w-full flex-wrap md:flex-nowrap mb-6 md:mb-0 gap-4">
        <Input
          isRequired
          key="username"
          type="username"
          label="Username"
          labelPlacement="inside"
          placeholder="Enter your username"
          onChange={(e) => setRegisterForm({ ...registerForm, username: e.target.value })}
        />
        <Input
          isRequired
          key="email"
          type="email"
          label="Email"
          labelPlacement="inside"
          placeholder="Enter your email"
          onChange={(e) => setRegisterForm({ ...registerForm, email: e.target.value })}
        />
        <Input
          isRequired
          key="password"
          type="password"
          label="Password"
          labelPlacement="inside"
          placeholder="Enter your password"
          onChange={(e) => setRegisterForm({ ...registerForm, password: e.target.value })}
        />
      </div>
      <Button
        onPress={(e) => onRegister(e)}
        color="primary"
        isLoading={loading}
      >
        Create Account
      </Button>
    </form>
  );
}

export default Registration;
