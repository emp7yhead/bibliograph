import { createBrowserRouter, Outlet } from 'react-router-dom';
// import { ErrorBoundary } from 'react-error-boundary';
import React from 'react';
import App from './App';
// // import ErrorPage from './routes/ErrorPage';

// function ErrorBoundaryLayout() {
//   return (
//     <ErrorBoundary FallbackComponent={GlobalError}>
//       <Outlet />
//     </ErrorBoundary>
//   );
// }

const AppRoutes = createBrowserRouter([
  // {
  //   element: <ErrorBoundaryLayout />,
  //   children: [
      {
        path: '/',
        element: <App />,
      },
      // {
      //   path: '/login',
      //   element: <Login />,
      // },
      {
        path: 'profile',
        element: <App />,
      },
      // {
      //   path: '*',
      //   element: <ErrorPage />,
      // },
    ],
  // },
);

export default AppRoutes;
