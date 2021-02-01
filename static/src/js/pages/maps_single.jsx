import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class MapSingle extends Component {
    constructor() {
        super();
    }

    componentDidMount(){
        var l = window.location.href;
        l = l.split('/');
        var hex = l[l.length - 1]
        
        console.log(hex);

        var usr_token = localStorage.getItem('usr_token')
        if(usr_token == null){
            return;
        }
        if(usr_token.length != 128){
            return;
        }

        
        fetch('/ajax/map', {
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token,
                'map': hex
            },
        })
        .then(data => data.json())
        .then((json) => {
            console.log(json)
            // alert('new map has been created')
            // TODO: script out reading maps
        })



    }

    render() {
        return (
            <div>client</div>
        )
    }
}