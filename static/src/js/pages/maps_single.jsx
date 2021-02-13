import React, { Component } from "react";
import ReactDOM from "react-dom";
import { io } from "socket.io-client";

import Vtoken from './component/vtoken.jsx';
import Youtube from './component/youtube.jsx';
import {getUserId, userIdExists, getMapHexFromURL} from './component/commons.jsx'
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
            'width': 1000,
            'tokens': [],
            'foggyOfWar': true
        }
    }

    componentDidMount(){

        fetch('/ajax/map', {
            headers: {
                'Content-Type': 'application/json',
                'map': getMapHexFromURL()
            }
        })
        .then(data=>data.json())
        .then((json) => {
            console.log(json);
            if(json.succs){
                this.setState({
                    'hex': getMapHexFromURL(),
                    'title': json.data.title,
                    'map': json.data.map_source,
                    'soundtrack': json.data.map_soundtrack,
                    'width': json.data.width,
                    'tokens': json.data.tokens,
                    'foggyOfWar': json.data.fog
                })
            }
        })
    }

    componentDidUpdate(){

        if(!userIdExists()){
            return
        }

        fetch('/ajax/map', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Userkey': getUserId()
            },
            body: JSON.stringify({
                'hex': getMapHexFromURL(),
                'title': this.state.title,
                'map': this.state.map,
                'soundtrack': this.state.soundtrack,
                'width': this.state.width,
                'fogOfWar': this.state.foggyOfWar
            })
        })
        .then(data=>data.json())
        .then((json) => {
            // console.log(json)
            if(!json.succs){
                alert(json.error);
            }
        })
    }

    render() {

        var dms_els = []
        var userExists = userIdExists()
        var foggy = {display: 'none'}
        if(userExists){
            dms_els.push(
                <div className="tools" key={1} >
                    <label htmlFor='mapTitle' >
                        <div>Title:</div> <input name='mapTitle' value={this.state.title} onChange={(event) => {this.setState({'title': event.target.value});}}  />
                    </label>
                    <label htmlFor='mapSoundtrack'>
                        <div>soundtrack:</div> <input name='mapSoundtrack' value={this.state.soundtrack} onChange={(event) => {this.setState({'soundtrack': event.target.value});}} />
                    </label>
                    <label htmlFor="mapWidth" >
                        <div>Fixed Map Width</div> <input name="mapWidth" type='number' min='1000' value={this.state.width} onChange={(event) => {this.setState({'width': event.target.value})}} />
                    </label>
                    <label htmlFor="fogOfWar" >
                        <div>Fog of War</div> <input name="fogOfWar" type='checkbox' checked={this.state.foggyOfWar} onChange={(event)=>{this.setState({'foggyOfWar': !this.state.foggyOfWar})}} />
                    </label>
                </div>
            )
            dms_els.push(
                <MapList key={2} />
            )
            foggy['opacity'] = '50%'
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

        if(this.state.foggyOfWar){
            foggy['display'] = 'block'
        }

        return (
            <div className="mapSingle" data-map={JSON.stringify(this.state)}>
                <div className="row_tokens">
                    {el_draggable}
                </div>
                <div className="maps">
                    <div class='fogOfWar' style={foggy}></div>
                    <img ref='image' src={this.state.map} style={{'width': this.state.width}} />
                    
                </div>
                <div className="audio">
                    <Youtube url={this.state.soundtrack} />
                </div>
                {dms_els}
            </div>
        )
    }
}