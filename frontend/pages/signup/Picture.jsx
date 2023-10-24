import React from 'react';
import { Image } from '@nextui-org/react';

export default function RegisterPic() {
  return (
    <div className="w-1/2 h-screen lg:block">
      <Image
        src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2670&q=80"
        alt="Books"
        isBlurred
        radius="none"
        className="hidden bg-cover w-full h-full"
      />
    </div>
  );
}
