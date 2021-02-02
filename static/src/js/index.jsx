import React, { Component } from "react";
import ReactDOM from "react-dom";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

// import Test from './component/test.jsx';
import Userlogin from './pages/user_login.jsx';
import MapsList from './pages/maps_list.jsx';
import MapSingle from './pages/maps_single.jsx';

class App extends Component {
    render(){
        return (
            <div>
                <Router>
                    <Switch>
                        <Route path='/map/'>
                            <MapSingle />
                        </Route>
                        <Route path='/' >
                            <Userlogin />
                            <MapsList />
                        </Route>
                    </Switch>
                </Router>
            </div>
        )
    }
}

ReactDOM.render(
    <App />,
    document.getElementById("App")
)