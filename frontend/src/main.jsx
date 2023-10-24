import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { NextUIProvider, Spinner } from '@nextui-org/react';
import AppRoutes from './Router';
import './index.css';

const domNode = document.getElementById('root');
const root = createRoot(domNode);
root.render(
  <NextUIProvider>
    <RouterProvider
      router={AppRoutes}
      fallbackElement={<Spinner />}
    />
  </NextUIProvider>,
);
