import React, { Component } from "react";
import ReactDOM from "react-dom";
import {userIdExists} from './commons.jsx'

export default class SiteHeader extends Component {
    constructor() {
        super();
        this.logout = this.logout.bind(this)
    }

    logout(event){
        event.preventDefault();
        localStorage.removeItem('usr_token');
        window.location.href = '/'
    }

    render() {

        var links = []
        if( userIdExists() ){
            links.push(<div onClick={this.logout}> Logout </div>)
        }

        return (
            <header>
                <div className="siteTitle">
                    <h1>Map Tin</h1>
                </div>
                <div className="links">
                    {links}
                </div>
            </header>
        )
    }
}