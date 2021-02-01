import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class MapSingle extends Component {
    constructor() {
        super();
        this.state = {
            'hex': '',
            'title': '',
            'map': '',
            'soundtrack': ''
        }
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

    render() {
        return (
            <div className="mapSingle" data-map={JSON.stringify(this.state)}>
                <div className="tools">
                    <div className="mapTitle" >
                        <label htmlFor='mapTitle' >
                            Title: <input name='mapTitle' value={this.state.title} onChange={(event) => {this.setState({'title': event.target.value})}} />
                        </label>
                    </div>
                </div>
                <div className="maps"></div>
            </div>
        )
    }
}