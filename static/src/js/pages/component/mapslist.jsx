import React, { Component } from "react";
import ReactDOM from "react-dom";

import { io } from "socket.io-client";

function imgEl(src, key){

    var clickEvent = () => {
        
        var l = window.location.href;
        l = l.split('/');
        var hex = l[l.length - 1]

        fetch(
            '/ajax/map/bg',
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    'hex': hex,
                    'src': src
                })
            })
            .then(data=>data.json())
            .then((json)=>{
                if(json.succ){
                    var sock = io();
                    sock.emit('flash')
                }
            })
    }

    return(
        <span 
            key={key}
            className='asset'
            style={{backgroundImage: 'url(' + src + ')'}}
            onClick={clickEvent}
        >
        </span>
    );
}

export default class MapList extends Component {
    constructor() {
        super();
        this.state = {
            'maps': []
        }
    }

    componentDidMount(){
        fetch(
            '/ajax/assets/maps', 
            {headers: {'Content-Type': 'application/json'}
        })
        .then(data => data.json())
        .then((json) => {
            if(json.succs){
                this.setState({'maps': json.data})
            }
        })
    }

    render() {

        var maps = []
        for(var i = 0; i<this.state.maps.length; i++){
            maps.push(imgEl(this.state.maps[i], i))
        }

        var tray_width = (this.state.maps.length * 100)

        return (
            <div className="maptray">
                <div className='title'> Maps </div>
                <div className='tray' style={{'width': tray_width}}>{maps}</div>
            </div>
        )
    }
}