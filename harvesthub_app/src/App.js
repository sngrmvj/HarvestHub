import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <Fragment>


      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"

        style={{zIndex:"1000000"}}
      />
      <br/><br/>
    </Fragment>
  );
}

export default App;
