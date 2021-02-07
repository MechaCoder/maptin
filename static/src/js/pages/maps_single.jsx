import React, { Component } from "react";
import ReactDOM from "react-dom";
import { io } from "socket.io-client";

import Vtoken from './component/vtoken.jsx';
import Youtube from './component/youtube.jsx';
import {getUserId, userIdExists} from './component/commons.jsx'
import AssertToken from './component/assertTray.jsx';
import MapList from './component/mapslist.jsx';


export default class MapSingle extends Component {
    constructor() {
        super();
        this.state = {
            'hex': '',
            'title': '',
            'map': '',
            'soundtrack': '',
            'tokens': []
        }

        this.getMapData = this.getMapData.bind(this);
    }

    getMapData(){

        var l = window.location.href;
        l = l.split('/');
        var hex = l[l.length - 1]
        
        fetch('/ajax/map', {
            headers: {
                'Content-Type': 'application/json',
                'map': hex
            },
        })
        .then(data => data.json())
        .then((json) => {
            if(json.succs){

                this.setState({
                    'hex': json.data.hex,
                    'title': json.data.title,
                    'map': json.data.map_source,
                    'soundtrack': json.data.map_soundtrack,
                    'tokens': json.data.tokens
                })
            }

        })

    }

    componentDidUpdate(){
        this.updateServer()
    }

    componentDidMount(){
        // getUserId()
        this.socket = io();

        this.socket.on('flash', ()=>{
            // this.forceUpdate()
            this.getMapData()
        })
        this.getMapData()
    }

    updateServer(){
        if(userIdExists() === false){
            return;
        }
        var usr_token = getUserId()

        fetch('/ajax/map', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            },
            body: JSON.stringify({
                'hex': this.state.hex,
                'title': this.state.title,
                'map': this.state.map,
                'soundtrack': this.state.soundtrack
            })
        })
        .then(data=>data.json())
        .then((json)=>{
            if(json.succs){
                console.log(json.data)
            }
            else{
                alert(json.error)
            }
        })
    }

    render() {

        var dms_els = []
        var userExists = userIdExists()
        if(userExists){
            dms_els.push(
                <div className="tools" key={1} >
                    <label htmlFor='mapTitle' >
                        <div>Title:</div> <input name='mapTitle' value={this.state.title} onChange={(event) => {this.setState({'title': event.target.value});}}  />
                    </label>
                    <label htmlFor='mapSoundtrack'>
                        <div>soundtrack:</div> <input name='mapSoundtrack' value={this.state.soundtrack} onChange={(event) => {this.setState({'soundtrack': event.target.value});}} />
                    </label>
                    
                </div>
            )
            dms_els.push(
                <MapList key={2} />
            )
        }

        dms_els.push(
            <AssertToken key={3} subpath='tokens' />
        )
        
        var el_draggable = []
        
        for(var i = 0; i < this.state.tokens.length; i++){ 
            el_draggable.push(
                <Vtoken
                    key={i}
                    hex={this.state.tokens[i].hex}
                    pic={this.state.tokens[i].source}
                    x={this.state.tokens[i].x}
                    y={this.state.tokens[i].y}
                />
            )
        }

        return (
            <div className="mapSingle" data-map={JSON.stringify(this.state)}>
                <div className="row_tokens">
                    {el_draggable}
                </div>
                <div className="maps">
                    <img src={this.state.map} />
                </div>
                <div className="audio">
                    <Youtube url={this.state.soundtrack} />
                </div>
                {dms_els}
            </div>
        )
    }
}