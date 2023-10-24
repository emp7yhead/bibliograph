import React from 'react';
import { Input } from '@nextui-org/react';

export default function FormInput({ isRequired, newKey, type, label, placeholder, onChange }) {
  return (
    <Input
      className="w-full rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"
      labelPlacement="inside"
      key={newKey}
      type={type}
      label={label}
      placeholder={placeholder}
      isRequired={isRequired}
      onChange={onChange}
    />
  );
}
