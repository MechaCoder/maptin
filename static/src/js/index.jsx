import React, { Component } from "react";
import ReactDOM from "react-dom";
// import Test from './component/test.jsx';
import Userlogin from './pages/user_login.jsx';
import MapsList from './pages/maps_list.jsx';

class App extends Component {
    render(){
        return (
            <div>
                <Userlogin />
                <MapsList />
            </div>
        )
    }
}

ReactDOM.render(
    <App />,
    document.getElementById("App")
)