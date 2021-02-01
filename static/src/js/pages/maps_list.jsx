import React, { Component } from "react";
import ReactDOM from "react-dom";
import MapListItem from "./component/map_list_item.jsx";

export default class MapsList extends Component {
    constructor() {
        super();
        this.state = {
            'hide': false,
            'maps': []
        }
        this.createMap = this.createMap.bind(this)
        this.getMaps = this.getMaps.bind(this)
    }

    componentDidMount(){
        this.getMaps();
    }

    getMaps(){
        var usr_token = localStorage.getItem('usr_token')
        if(usr_token == null){
            return;
        }
        if(usr_token.length != 128){
            return;
        }
        fetch('/ajax/maps', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            }
        })
        .then(data => data.json())
        .then((json) => {
            console.log(json)
            this.setState({
                'maps': json
            })

        })
    }

    

    createMap(event){

        var usr_token = localStorage.getItem('usr_token')
        if(usr_token == null){
            return;
        }
        if(usr_token.length != 128){
            return;
        }
        fetch('/ajax/maps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            }
        })
        .then(data => data.json())
        .then((json) => {
            console.log(json)
            alert('new map has been created')
            // TODO: script out reading maps
            this.getMaps()
        })

    }

    render() {
        
        var items = []
        for(var i = 0; i < this.state.maps.length; i++){
            var el = this.state.maps[i];
            items.push(<MapListItem key={i} hex={el.hex} title={el.title} map={el.map_source} soundtrack={el.map_soundtrack} />)

        }

        return (
            <div className="maps_diolog">
                {this.state.maps.length}
                <div className="tools">
                    <button onClick={this.createMap}>Create Map</button>
                </div>
                <div>
                    {items}
                </div>
            </div>
        )
    }
}