import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class MapListItem extends Component {
    constructor() {
        super();
        this.deleteSelf = this.deleteSelf.bind(this);
    }

    deleteSelf(){

        if(!confirm('are you sure')){
            return;
        }

        var usr_token = localStorage.getItem('usr_token')
        if(usr_token == null){
            return;
        }
        if(usr_token.length != 128){
            return;
        }
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
            console.log(json)
            alert('A map has been deleted')
            // TODO: script out reading maps
            location.reload()
        })

    }

    render() {
        var link = '/map/' + this.props.hex

        return (
            <div className="MapListItem" data-hex={this.props.hex}>
                <a href={link} onClick={(e) => {e.preventDefault()}} ><div> <img src={this.props.map} width='200px' /></div></a>
                    <div>{this.props.title} <button onClick={this.deleteSelf}>delete</button> </div>
                
            </div>
        )
    }
}