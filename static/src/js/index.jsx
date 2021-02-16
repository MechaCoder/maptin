import React, { Component } from "react";
import ReactDOM from "react-dom";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

import Userlogin from './pages/user_login.jsx';
import MapsList from './pages/maps_list.jsx';
import MapSingle from './pages/maps_single.jsx';

import SiteHeader from './pages/component/header.jsx';
import '../scss/style.scss'; 

class App extends Component {
    render(){
        return (
            <div>
                <SiteHeader />
                <Router>
                    <Switch>
                        <Route path='/map/'>
                            <MapSingle />
                        </Route>
                        <Route path='/dashboard/'>
                            <MapsList />
                        </Route>
                        <Route path='/' >
                            <Userlogin />
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