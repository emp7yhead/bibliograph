import React from 'react';
import { Card, CardBody } from '@nextui-org/react';

// TODO: add levels
export default function ErrorMessage({ message }) {
  return (
    <Card radius="sm" isBlurred>
      <CardBody>
        <p className="text-center">{message}</p>
      </CardBody>
    </Card>
  );
}
