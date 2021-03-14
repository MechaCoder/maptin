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
            'foggyOfWar': true,
            'changed': false
        }
        this.saveInfo = this.saveInfo.bind(this);
    }

    componentDidMount(){
        // keyboard shortcuts

        this.socket = io();

        this.socket.on('map:update:tokens', (_data) => {
            // when the map tokens are updated then update them in the clients
            // EVENTS
                // create token
            // this.setState({'tokens': _data.tokens})
            if(_data.succ == false){
                return;
            }

            if(_data.data.mapHex != this.state.hex){
                return;
            }

            this.setState({'tokens': _data.data.tokens})
        })

        this.socket.on('map:updated', (json) => {

          if(!json.succ){
            alert(json.err);
            return;
          }

          if(json.data.map.hex != this.state.hex){
              return;
          }

          this.setState({'map': json.data.map.map_background})

        })


        fetch('/ajax/map', {
            headers: {
                'Content-Type': 'application/json',
                'map': getMapHexFromURL()
            }
        })
        .then(data=>data.json())
        .then((json) => {
            if(json.succ){
                document.title = json.data.map.title;

                this.setState({
                    'hex': json.data.map.hex,
                    'title': json.data.map.title,
                    'map': json.data.map.map_background,
                    'soundtrack': json.data.map.map_soundtrack,
                    'width': json.data.map.map_width,
                    'foggyOfWar': json.data.map.map_fog,
                    'tokens': json.data.map.tokens
                })
            }
        })

    }

    saveInfo(event){
        if(event != undefined){
            event.preventDefault()
        }


        var body = this.state;
        body.fogOfWar = this.state.foggyOfWar


        fetch('/ajax/map', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Userkey': getUserId(),
            },
            body: JSON.stringify(body)
        })
        .then(http=>http.json())
        .then((json)=>{
            console.log(json)
            if(!json.succ){
                alert(json.err)
                return;
            }
        });               
        document.title = this.state.title;
        this.setState({'changed': false})

    }

    render() {

        var dms_els = [] // adds user elerments to the page
        var userExists = userIdExists() // the users session key

        var foggy = {display: 'none'} // the css the fog of war

        if(userExists){

            dms_els.push(
                <div className="tools" key={1} >
                    
                    <label htmlFor='mapTitle' >
                        <div>Title:</div> <input name='mapTitle' value={this.state.title} onChange={(event) => {this.setState({'title': event.target.value, 'changed': true});}}  />
                    </label>
                    <label htmlFor='mapSoundtrack'>
                        <div>soundtrack:</div> <input name='mapSoundtrack' value={this.state.soundtrack} onChange={(event) => {this.setState({'soundtrack': event.target.value, 'changed': true});}} />
                    </label>
                    <label htmlFor="mapWidth" >
                        <div>Fixed Map Width</div> <input name="mapWidth" type='number' min='1000' value={this.state.width} onChange={(event) => {this.setState({'width': event.target.value, 'changed': true})}} />
                    </label>
                    <label htmlFor="fogOfWar" >
                        <div>Fog of War</div> <input name="fogOfWar" type='checkbox' checked={this.state.foggyOfWar} onChange={(event)=>{this.setState({'foggyOfWar': !this.state.foggyOfWar, 'changed': true})}} />
                    </label>
                    <label><div></div> <button disabled={!this.state.changed} onClick={this.saveInfo}> Save </button></label>
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
            console.log(this.state.tokens[i]);
            el_draggable.push(
                <Vtoken
                    key={i}
                    hex={this.state.tokens[i].hex}
                    pic={this.state.tokens[i].token_source}
                    x={this.state.tokens[i].x}
                    y={this.state.tokens[i].y}
                    conseal={this.state.tokens[i].conseal}
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
                    <div className='fogOfWar' style={foggy}></div>
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
