import React, { Component } from "react";
import ReactDOM from "react-dom";
import Youtube from './component/youtube.jsx';
import {getUserId, userIdExists} from './component/commons.jsx'
import AssertToken from './component/assertTray.jsx';

import Draggable from 'react-draggable';

function updateLocation(hex, x, y){
    fetch(
        '/ajax/token',
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'hex': hex,
                'x': x,
                'y': y
            })
        }
    )
    .then(data => data.json())
    .then((json) => {
        console.log(json)
        if(json.succs){
            console.log('finish')
        }
    })
}

function draggableToken(obj){

    var onStartEvent = (e, data)=>{
        updateLocation(obj.hex, data.x, data.y)
    }
    // var onDragEvent = (e, data)=>{
    // }
    var onStopEvent = (e, data)=>{
        updateLocation(obj.hex, data.x, data.y)
    }

    return(
        <Draggable
            onStart={onStartEvent}
            // onDrag={onDragEvent}
            onStop={onStopEvent}
            defaultPosition={{
                x: obj.x,
                y: obj.y
            }}
        >  
            <div className='daggabletoken'>
                <img src={obj.source} width='15px' />
            </div>
        </Draggable>
    )

}

export default class MapSingle extends Component {
    constructor() {
        console.log('MapSingle')
        super();
        this.state = {
            'hex': '',
            'title': '',
            'map': '',
            'soundtrack': '',
            'tokens': []
        }
        // this.updateServer = this.updateServer.bind(this);
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

                console.log(json.data)

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
        console.log('update server')
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
        console.log(this.state.tokens)
        var el_draggable = []
        
        for(var i = 0; i < this.state.tokens.length; i++){
            el_draggable.push(
                draggableToken(this.state.tokens[i])
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