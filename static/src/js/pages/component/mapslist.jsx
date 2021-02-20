import React, { Component } from "react";
import ReactDOM from "react-dom";

import { io } from "socket.io-client";

function imgEl(src, key){

    var clickEvent = () => {

        var sure = confirm('Are you sure you want to change the background map');
        if(!sure){
            return;
        }
        
        
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
            'mapsAll': [],
            'mapPop': [],
            'expand': false
        }
    }

    componentDidMount(){
        fetch(
            '/ajax/assets/maps', 
            {headers: {'Content-Type': 'application/json'}
        })
        .then(data => data.json())
        .then((json) => {
            if(!json.succs){
                alert(json.error)
            }
            if(json.succs){


                this.setState({
                    'mapsAll': json.data.all,
                    'mapPop': json.data.popular
                })
            }
        })
    }

    render() {

        var maps = []
        var mapspop = []
        for(var i = 0; i<this.state.mapsAll.length; i++){
            maps.push(imgEl(this.state.mapsAll[i], i))
        }

        for(var i = 0; i<this.state.mapPop.length; i++){
            mapspop.push(imgEl(this.state.mapsAll[i], i))
        }

        // var tray_width = (this.state.maps.length * 100)

        var classExpand = 'maptray'
        if(this.state.expand){
            classExpand += ' expand';
        }

        return (
            <div className={classExpand}>
                <div className='title' onClick={(e)=>{ this.setState({'expand': !this.state.expand}) }}> Maps <a onClick={(e)=>{ this.setState({'expand': !this.state.expand})}} >x</a> </div>
                <div className='popularity tray'>
                    {mapspop}
                </div>
                <div className='all tray'>
                    {maps}
                </div>
            </div>
        )
    }
}