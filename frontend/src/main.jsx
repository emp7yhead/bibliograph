import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { NextUIProvider } from '@nextui-org/react';
import App from './App';
// import ErrorPage from './routes/ErrorPage';
import './index.css';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    // errorElement: <ErrorPage />,
  },
]);

const domNode = document.getElementById('root');
const root = createRoot(domNode);
root.render(
  <NextUIProvider>
    <RouterProvider router={router} />
  </NextUIProvider>,
);
