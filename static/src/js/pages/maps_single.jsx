import React, { Component } from "react";
import ReactDOM from "react-dom";
import Vtoken from './component/vtoken.jsx';

import Youtube from './component/youtube.jsx';
import {getUserId, userIdExists} from './component/commons.jsx'
import AssertToken from './component/assertTray.jsx';


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
    }

    componentDidUpdate(){
        this.updateServer()
    }

    componentDidMount(){
        // getUserId()

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
    }

    render() {

        var dms_els = []
        var userExists = userIdExists()
        userExists = false
        if(userExists){
            dms_els.push(
                <div className="tools">
                    <label htmlFor='mapTitle' >
                        <div>Title:</div> <input name='mapTitle' value={this.state.title} onChange={(event) => {this.setState({'title': event.target.value});}}  />
                    </label>
                    <label htmlFor='mapMap'>
                        <div>Map:</div> <input name='mapMap' value={this.state.map} onChange={(event) => {this.setState({'map': event.target.value});}} />
                    </label>
                    <label htmlFor='mapSoundtrack'>
                        <div>soundtrack:</div> <input name='mapSoundtrack' value={this.state.soundtrack} onChange={(event) => {this.setState({'soundtrack': event.target.value});}} />
                    </label>
                </div>
            )
        }

        dms_els.push(
            <AssertToken subpath='tokens' />
        )
        
        var el_draggable = []
        
        for(var i = 0; i < this.state.tokens.length; i++){ 
            el_draggable.push(
                <Vtoken 
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