import React, { Component } from "react";
import ReactDOM from "react-dom";
// import Test from './component/test.jsx';
import Userlogin from './pages/user_login.jsx';

class App extends Component {
    render(){
        return (
            <div>
                <Userlogin />
            </div>
        )
    }
}

ReactDOM.render(
    <App />,
    document.getElementById("App")
)