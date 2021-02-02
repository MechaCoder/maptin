import React, { Component } from "react";
import ReactDOM from "react-dom";
import Youtube from './component/youtube.jsx';

export default class MapSingle extends Component {
    constructor() {
        super();
        this.state = {
            'hex': '',
            'title': '',
            'map': '',
            'soundtrack': ''
        }
        this.updateServer = this.updateServer.bind(this);
    }

    componentDidUpdate(){
        this.updateServer()
    }

    componentDidMount(){
        var l = window.location.href;
        l = l.split('/');
        var hex = l[l.length - 1]

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
            if(json.succs){
                this.setState({
                    'hex': json.data.hex,
                    'title': json.data.title,
                    'map': json.data.map_source,
                    'soundtrack': json.data.map_soundtrack
                })
            }

        })

    }

    updateServer(){
        fetch('/ajax/map', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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
        return (
            <div className="mapSingle" data-map={JSON.stringify(this.state)}>
                <div className="maps">
                    <img src={this.state.map} />
                </div>
                <div className="audio">
                    <Youtube url={this.state.soundtrack} />
                </div>
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
            </div>
        )
    }
}