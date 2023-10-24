import { Button } from '@nextui-org/react';
import React from 'react';

export default function FormButton({
  onPress, color, isLoading, text
}) {
  return (
    <Button
      className="w-full px-4 py-2 tracking-wide duration-200 transform rounded-md focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-50"
      onPress={onPress}
      color={color}
      isLoading={isLoading}
    >
      {text}
    </Button>
  );
}
