import React, { Component } from "react";
import ReactDOM from "react-dom";
import {getUserId} from './commons.jsx'

export default class MapListItem extends Component {
    constructor() {
        super();
        this.deleteSelf = this.deleteSelf.bind(this);
    }

    deleteSelf(){

        if(!confirm('are you sure')){
            return;
        }

        var usr_token = getUserId();
        fetch('/ajax/maps', {
            method: 'DELETE',
            body: JSON.stringify({'map': this.props.hex}),
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            }
        })
        .then(data => data.json())
        .then((json) => {
            alert('A map has been deleted')
            // TODO: script out reading maps
            location.reload()
        })

    }

    render() {
        var link = '/map/' + this.props.hex

        return (
            <div className="MapListItem" data-hex={this.props.hex}>
                <a href={link} >
                    <div className="coverImg" style={{backgroundImage: 'url(' + this.props.map + ')'}} > 
                        {/* <img src={this.props.map} width='200px' /> */}
                    </div>
                </a>
                <div>{this.props.title} <button onClick={this.deleteSelf}>delete</button> </div>
            </div> 
        )
    }
}