
import './App.css';
import React, {Suspense, lazy} from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";



const Login = lazy(() => import('./components/login/login'));
const Signup = lazy(() => import('./components/signup/signup'));
const Menu = lazy(() => import('./components/menu/menu'));
const PurchaseHistory = lazy(() => import('./components/purchased_orders/purchased_orders'));
const Cart = lazy(() => import('./components/cart/cart'));
const Receipt = lazy(() => import('./components/receipt/receipt'));

function App() {
  return (
    <Router>
      <Routes>
          <Route path='/' element={
              <Suspense fallback={<p>Loading...</p>}>
                <Login />
              </Suspense>
            }
          />
          <Route path='/register' element={
              <Suspense fallback={<p>Loading...</p>}>
                <Signup />
              </Suspense>
            }
          />
          <Route path='/menu' element={
              <Suspense fallback={<p>Loading...</p>}>
                <Menu />
              </Suspense>
            }
          />
          <Route path='/cart' element={
              <Suspense fallback={<p>Loading...</p>}>
                <Cart />
              </Suspense>
            }
          />
          <Route path='/history' element={
              <Suspense fallback={<p>Loading...</p>}>
                <PurchaseHistory />
              </Suspense>
            }
          />
          <Route path='/receipt' element={
              <Suspense fallback={<p>Loading...</p>}>
                <Receipt />
              </Suspense>
            }
          />
      </Routes>
    </Router>
  );
}

export default App;